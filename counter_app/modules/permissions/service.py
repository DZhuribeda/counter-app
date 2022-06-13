import asyncio
from counter_app.modules.permissions.model import (
    Entities,
    ENTITY_PERMISSIONS,
)

from authzed.api.v1 import (
    Client,
    ObjectReference,
    Relationship,
    RelationshipUpdate,
    SubjectReference,
    WriteRelationshipsRequest,
    CheckPermissionRequest,
    CheckPermissionResponse,
    Consistency,
    ReadRelationshipsRequest,
    RelationshipFilter,
    LookupResourcesRequest,
)


class PermissionsService:
    def __init__(
        self,
        spicedb_client: Client,
    ):
        self.spicedb_client = spicedb_client

    async def _persist_tuples(self, updates: list[RelationshipUpdate]):
        await self.spicedb_client.WriteRelationships(
            WriteRelationshipsRequest(updates=updates)
        )

    async def _check_role(
        self, entity: Entities, entity_id: str, user_id: str, role: str
    ):
        resp = await self.spicedb_client.CheckPermission(
            CheckPermissionRequest(
                consistency=Consistency(fully_consistent=1),
                resource=ObjectReference(object_type=entity.value, object_id=entity_id),
                permission=role,
                subject=SubjectReference(
                    object=ObjectReference(
                        object_type="user",
                        object_id=user_id,
                    )
                ),
            )
        )
        return (
            role,
            resp.permissionship
            == CheckPermissionResponse.PERMISSIONSHIP_HAS_PERMISSION,
        )

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
            RelationshipUpdate(
                operation=RelationshipUpdate.Operation.OPERATION_CREATE,
                relationship=Relationship(
                    resource=ObjectReference(
                        object_type=entity.value, object_id=entity_id
                    ),
                    relation=role,
                    subject=SubjectReference(
                        object=ObjectReference(
                            object_type="user",
                            object_id=user_id,
                        )
                    ),
                ),
            ),
        ]
        if user_role:
            actions.append(
                RelationshipUpdate(
                    operation=RelationshipUpdate.Operation.OPERATION_DELETE,
                    relationship=Relationship(
                        resource=ObjectReference(
                            object_type=entity.value, object_id=entity_id
                        ),
                        relation=user_role,
                        subject=SubjectReference(
                            object=ObjectReference(
                                object_type="user",
                                object_id=user_id,
                            )
                        ),
                    ),
                )
            )
        await self._persist_tuples(actions)

    async def delete_role(self, entity: Entities, entity_id: str, user_id: str):
        user_role = await self.get_user_role(entity, entity_id, user_id)
        if not user_role:
            return
        actions = [
            RelationshipUpdate(
                operation=RelationshipUpdate.Operation.OPERATION_DELETE,
                relationship=Relationship(
                    resource=ObjectReference(
                        object_type=entity.value, object_id=entity_id
                    ),
                    relation=user_role,
                    subject=SubjectReference(
                        object=ObjectReference(
                            object_type="user",
                            object_id=user_id,
                        )
                    ),
                ),
            )
        ]
        await self._persist_tuples(actions)

    async def check_permission(
        self, entity: Entities, entity_id: str, permission: str, user_id: str
    ):
        resp = await self.spicedb_client.CheckPermission(
            CheckPermissionRequest(
                consistency=Consistency(fully_consistent=1),
                resource=ObjectReference(object_type=entity.value, object_id=entity_id),
                permission=permission,
                subject=SubjectReference(
                    object=ObjectReference(
                        object_type="user",
                        object_id=user_id,
                    )
                ),
            )
        )
        return (
            resp.permissionship == CheckPermissionResponse.PERMISSIONSHIP_HAS_PERMISSION
        )

    async def get_users_with_access(
        self,
        entity: Entities,
        entity_id: str,
    ):
        user_role = []
        async for resp in self.spicedb_client.ReadRelationships(
            ReadRelationshipsRequest(
                consistency=Consistency(fully_consistent=1),
                relationship_filter=RelationshipFilter(
                    resource_type=entity.value,
                    optional_resource_id=entity_id,
                ),
            )
        ):
            user_role.append(
                {
                    "role": resp.relationship.relation,
                    "user": resp.relationship.subject.object.object_id,
                }
            )

        return user_role

    async def get_user_object_ids_permission(
        self,
        entity: Entities,
        user_id: str,
        permission: str,
    ):
        object_ids = []
        async for resp in self.spicedb_client.LookupResources(
            LookupResourcesRequest(
                consistency=Consistency(fully_consistent=1),
                resource_object_type=entity.value,
                permission=permission,
                subject=SubjectReference(
                    object=ObjectReference(
                        object_type="user",
                        object_id=user_id,
                    )
                ),
            )
        ):
            object_ids.append(resp.resource_object_id)
        return object_ids
