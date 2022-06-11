import asyncio
from counter_app.modules.permissions.model import (
    ENTITY_BASE_ROLE,
    Entities,
    ENTITY_PERMISSIONS,
)
from counter_app.ory.keto.acl.v1alpha1.expand_service_pb2 import ExpandRequest
from counter_app.ory.keto.acl.v1alpha1.expand_service_pb2_grpc import ExpandServiceStub
from counter_app.ory.keto.acl.v1alpha1.read_service_pb2_grpc import ReadServiceStub
from counter_app.ory.keto.acl.v1alpha1.write_service_pb2 import (
    RelationTupleDelta,
    TransactRelationTuplesRequest,
)
from counter_app.ory.keto.acl.v1alpha1.acl_pb2 import RelationTuple, SubjectSet, Subject
from counter_app.ory.keto.acl.v1alpha1.write_service_pb2_grpc import WriteServiceStub
from counter_app.ory.keto.acl.v1alpha1.check_service_pb2_grpc import CheckServiceStub
from counter_app.ory.keto.acl.v1alpha1.check_service_pb2 import CheckRequest


class PermissionsService:
    def __init__(
        self,
        keto_write_service: WriteServiceStub,
        keto_check_service: CheckServiceStub,
        keto_read_service: ReadServiceStub,
        keto_expand_service: ExpandServiceStub,
    ):
        self.keto_write_service = keto_write_service
        self.keto_check_service = keto_check_service
        self.keto_read_service = keto_read_service
        self.keto_expand_service = keto_expand_service

    def _create_role_permission_action(
        self, entity: Entities, entity_id: str, role: str, permission: str
    ) -> RelationTupleDelta:
        return RelationTupleDelta(
            action=RelationTupleDelta.Action.INSERT,
            relation_tuple=RelationTuple(
                namespace=entity.value,
                object=entity_id,
                relation=permission,
                subject=Subject(
                    set=SubjectSet(
                        namespace=f"{entity.value}_roles",
                        object=f"{entity_id}_{role}",
                        relation="member",
                    )
                ),
            ),
        )

    async def persist_tuples(self, actions: RelationTupleDelta):
        await self.keto_write_service.TransactRelationTuples(
            TransactRelationTuplesRequest(relation_tuple_deltas=actions)
        )

    async def setup_roles(self, entity: Entities, entity_id: str):
        actions = []
        for role, permissions in ENTITY_PERMISSIONS[entity].items():
            for permission in permissions:
                actions.append(
                    self._create_role_permission_action(
                        entity, entity_id, role, permission
                    )
                )
        await self.persist_tuples(actions)

    async def _check_role(
        self, entity: Entities, entity_id: str, user_id: str, role: str
    ):
        response = await self.keto_check_service.Check(
            CheckRequest(
                namespace=f"{entity.value}_roles",
                object=f"{entity_id}_{role}",
                relation="member",
                subject=Subject(
                    id=user_id,
                ),
            )
        )
        return role, response.allowed

    async def get_user_role(self, entity: Entities, entity_id: str, user_id: str):
        tasks = []
        for role in ENTITY_PERMISSIONS[entity].keys():
            tasks.append(self._check_role(entity, entity_id, user_id, role))
        results = await asyncio.gather(*tasks)
        for role, allowed in results:
            if allowed:
                return role
        return None

    async def assign_role(
        self, entity: Entities, entity_id: str, role: str, user_id: str
    ):
        user_role = await self.get_user_role(entity, entity_id, user_id)
        if user_role == role:
            return
        actions = [
            RelationTupleDelta(
                action=RelationTupleDelta.Action.INSERT,
                relation_tuple=RelationTuple(
                    namespace=f"{entity.value}_roles",
                    object=f"{entity_id}_{role}",
                    relation="member",
                    subject=Subject(
                        id=user_id,
                    ),
                ),
            )
        ]
        if user_role:
            actions.append(
                RelationTupleDelta(
                    action=RelationTupleDelta.Action.DELETE,
                    relation_tuple=RelationTuple(
                        namespace=f"{entity.value}_roles",
                        object=f"{entity_id}_{user_role}",
                        relation="member",
                        subject=Subject(
                            id=user_id,
                        ),
                    ),
                )
            )
        await self.persist_tuples(actions)

    async def delete_role(self, entity: Entities, entity_id: str, user_id: str):
        user_role = await self.get_user_role(entity, entity_id, user_id)
        if not user_role:
            return
        actions = [
            RelationTupleDelta(
                action=RelationTupleDelta.Action.DELETE,
                relation_tuple=RelationTuple(
                    namespace=f"{entity.value}_roles",
                    object=f"{entity_id}_{user_role}",
                    relation="member",
                    subject=Subject(
                        id=user_id,
                    ),
                ),
            )
        ]
        await self.persist_tuples(actions)

    async def check_permission(
        self, entity: Entities, entity_id: str, permission: str, user_id: str
    ):
        response = await self.keto_check_service.Check(
            CheckRequest(
                namespace=entity.value,
                object=entity_id,
                relation=permission,
                subject=Subject(
                    id=user_id,
                ),
            )
        )
        return response.allowed

    async def get_users_with_access(
        self,
        entity: Entities,
        entity_id: str,
    ):
        response = await self.keto_expand_service.Expand(
            ExpandRequest(
                max_depth=3,
                subject=Subject(
                    set=SubjectSet(
                        namespace=entity.value,
                        object=entity_id,
                        relation=ENTITY_BASE_ROLE[entity],
                    )
                ),
            )
        )
        user_role = []
        for role_binding in response.tree.children:
            parsed_role = role_binding.subject.set.object.split("_")[-1]
            for user in role_binding.children:
                user_role.append(
                    {
                        "role": parsed_role,
                        "user": user.subject.id,
                    }
                )

        return user_role
