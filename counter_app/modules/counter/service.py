import structlog
from counter_app.modules.counter.repository import CounterRepository
from counter_app.modules.permissions.model import CounterRoles, Entities
from counter_app.modules.permissions.service import PermissionsService

logger = structlog.get_logger()


class CounterService:
    def __init__(
        self,
        counter_repository: CounterRepository,
        permissions_service: PermissionsService,
    ) -> None:
        self._counter_repository = counter_repository
        self._permissions_service = permissions_service

    async def create(
        self,
        name: str,
        owner_id: str,
        initial_value: int | None = None,
    ) -> str:
        counter_id = await self._counter_repository.insert(name, owner_id)
        await self._permissions_service.assign_role(
            Entities.COUNTER, counter_id, CounterRoles.ADMIN, owner_id
        )
        if initial_value:
            await self._counter_repository.set_value(counter_id, initial_value)
        logger.info("Counter created", counter_id=counter_id, counter_name=name)
        return counter_id

    async def update(
        self,
        counter_id: str,
        name: str,
    ) -> None:
        await self._counter_repository.update(counter_id, name)
        logger.info("Counter updated", counter_id=counter_id, counter_name=name)

    async def delete(self, counter_id: str) -> None:
        # TODO: delete permissions
        await self._counter_repository.delete(counter_id)

    async def increment(self, counter_id: str) -> int:
        return await self._counter_repository.increment(counter_id)

    async def set_value(self, counter_id: str, value: int = 0) -> None:
        await self._counter_repository.set_value(counter_id, value)

    async def get_value(self, counter_id: str) -> int:
        value = await self._counter_repository.get_value(counter_id)
        if not value:
            return 0
        return int(value)
