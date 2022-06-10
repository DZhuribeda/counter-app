from dependency_injector.wiring import inject, Provide
from fastapi import Depends, HTTPException
from starlette.status import HTTP_403_FORBIDDEN

from counter_app.containers import Container
from counter_app.modules.auth.model import User
from counter_app.modules.auth.dependencies import get_required_user
from counter_app.modules.permissions.model import CounterPermissions, Entities
from counter_app.modules.permissions.service import PermissionsService


class CounterPermissionChecker:
    def __init__(self, permission: str):
        self.permission = permission

    @inject
    async def __call__(
        self,
        counter_id: str,
        service: PermissionsService = Depends(
            Provide[Container.permissions.permissions_service]
        ),
        current_user: User = Depends(get_required_user),
    ):
        allowed = await service.check_permission(
            Entities.COUNTER, counter_id, self.permission, current_user.id
        )
        if not allowed:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Not allowed",
            )


CounterReadPermission = Depends(CounterPermissionChecker(CounterPermissions.READ))
CounterDeletePermission = Depends(CounterPermissionChecker(CounterPermissions.DELETE))
CounterEditPermission = Depends(CounterPermissionChecker(CounterPermissions.EDIT))
CounterIncrementPermission = Depends(
    CounterPermissionChecker(CounterPermissions.INCREMENT)
)
