import uuid

import structlog
from counter_app.modules.counter.model import AccessModeEnum
from counter_app.modules.counter.repository import CounterRepository

logger = structlog.get_logger()


class CounterService:
    def __init__(self, counter_repository: CounterRepository) -> None:
        self._counter_repository = counter_repository

    async def create(
        self,
        name: str,
        owner_id: str,
        access_mode: AccessModeEnum,
        initial_value: int | None = None,
    ) -> str:
        counter_id = await self._counter_repository.insert(name, owner_id, access_mode)
        if initial_value:
            await self._counter_repository.set_value(counter_id, initial_value)
        logger.info("Counter created", counter_id=counter_id, counter_name=name)
        return counter_id

    async def update(
        self,
        counter_id: str,
        name: str,
        access_mode: AccessModeEnum,
    ) -> None:
        await self._counter_repository.update(counter_id, name, access_mode)
        logger.info("Counter updated", counter_id=counter_id, counter_name=name)

    async def delete(self, counter_id: str) -> None:
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
