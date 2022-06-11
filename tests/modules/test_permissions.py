from uuid import uuid4
import pytest
from counter_app.modules.permissions.model import (
    Entities,
    CounterRoles,
    CounterPermissions,
)


@pytest.fixture
def counter_id():
    return uuid4().hex


async def test_setup_roles(app, counter_id):
    user_id = "user_id"

    service = await app.container.permissions.permissions_service()
    await service.setup_roles(Entities.COUNTER, counter_id)

    await service.assign_role(
        Entities.COUNTER, counter_id, CounterRoles.WRITER, user_id
    )
    assert await service.check_permission(
        Entities.COUNTER, counter_id, CounterPermissions.READ, user_id
    )
    assert not await service.check_permission(
        Entities.COUNTER, counter_id, CounterPermissions.DELETE, user_id
    )


async def test_edit_user_roles(app, counter_id):
    user_id = "user_id"

    service = await app.container.permissions.permissions_service()
    await service.setup_roles(Entities.COUNTER, counter_id)

    await service.assign_role(
        Entities.COUNTER, counter_id, CounterRoles.WRITER, user_id
    )
    assert await service.check_permission(
        Entities.COUNTER, counter_id, CounterPermissions.READ, user_id
    )
    assert await service.check_permission(
        Entities.COUNTER, counter_id, CounterPermissions.INCREMENT, user_id
    )
    assert not await service.check_permission(
        Entities.COUNTER, counter_id, CounterPermissions.DELETE, user_id
    )

    await service.assign_role(
        Entities.COUNTER, counter_id, CounterRoles.READER, user_id
    )
    assert await service.check_permission(
        Entities.COUNTER, counter_id, CounterPermissions.READ, user_id
    )
    assert not await service.check_permission(
        Entities.COUNTER, counter_id, CounterPermissions.INCREMENT, user_id
    )
    assert not await service.check_permission(
        Entities.COUNTER, counter_id, CounterPermissions.DELETE, user_id
    )


async def test_get_users_with_access(app, counter_id):
    user_id = "user_id"
    another_user_id = "another_user_id"

    service = await app.container.permissions.permissions_service()
    await service.setup_roles(Entities.COUNTER, counter_id)

    await service.assign_role(
        Entities.COUNTER, counter_id, CounterRoles.WRITER, user_id
    )
    await service.assign_role(
        Entities.COUNTER, counter_id, CounterRoles.READER, another_user_id
    )
    users_with_access = await service.get_users_with_access(
        Entities.COUNTER, counter_id
    )
    assert len(users_with_access) == 2
