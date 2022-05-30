import uuid
from aioredis import Redis
from edgedb import AsyncIOClient
from opentelemetry import trace

from counter_app.modules.counter.model import AccessModeEnum

tracer = trace.get_tracer(__name__)


class CounterRepository:
    prefix = "counter:"

    def __init__(self, redis: Redis, edgedb: AsyncIOClient) -> None:
        self._redis = redis
        self._edgedb = edgedb

    def _get_key(self, counter_id: str) -> str:
        return f"{self.prefix}{counter_id}"

    async def insert(
        self, name: str, owner_id: str, access_mode: AccessModeEnum
    ) -> str:

        with tracer.start_as_current_span("insert_counter"):
            inserted = await self._edgedb.query_single(
                """
                INSERT Counter {
                    name := <str>$name,
                    access_mode := <default::AccessMode>$access_mode,
                    owner_id := <str>$owner_id
                }
                """,
                name=name,
                access_mode=access_mode.value,
                owner_id=owner_id,
            )
        return str(inserted.id)

    async def delete(self, id_: str) -> None:
        with tracer.start_as_current_span("delete_counter"):
            await self._edgedb.query_single(
                """
                delete Counter
                FILTER .id = <uuid>$id
                """,
                id=id_,
            )

    async def update(self, id_: str, name: str, access_mode: AccessModeEnum) -> None:
        with tracer.start_as_current_span("update_counter"):
            await self._edgedb.query_single(
                """
                UPDATE Counter
                FILTER .id = <uuid>$id
                SET {
                    name := <str>$name,
                    access_mode := <default::AccessMode>$access_mode,
                }
                """,
                id=id_,
                name=name,
                access_mode=access_mode.value,
            )

    async def increment(self, counter_id: str) -> int:
        with tracer.start_as_current_span("redis_incr"):
            return await self._redis.incr(self._get_key(counter_id))

    async def set_value(self, counter_id: str, value: int = 0) -> None:
        with tracer.start_as_current_span("redis_set"):
            await self._redis.set(self._get_key(counter_id), value)

    async def get_value(self, counter_id: str) -> None:
        with tracer.start_as_current_span("redis_get"):
            return await self._redis.get(self._get_key(counter_id))
