from counter_app.modules.permissions.model import (
    Entities,
    CounterRoles,
    CounterPermissions,
)


async def test_setup_roles(app):
    user_id = "user_id"
    counter_id = "1"

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


async def test_edit_user_roles(app):
    user_id = "user_id"
    counter_id = "1"

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
