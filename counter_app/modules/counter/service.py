from aioredis import Redis

from opentelemetry import trace
from counter_app.metric import COUNTER_INCREMENT, COUNTER_RESET, COUNTER_READ


tracer = trace.get_tracer(__name__)

class CounterService:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def increment(self, key: str) -> int:

        with tracer.start_as_current_span("redis_incr"):
            value = await self._redis.incr(key)
        COUNTER_INCREMENT.labels(counter_name=key).inc()
        return value

    async def set_value(self, key: str, value: int = 0) -> None:
        COUNTER_RESET.labels(counter_name=key).inc()
        with tracer.start_as_current_span("redis_set"):
            await self._redis.set(key, value)

    async def get_value(self, key: str) -> int:
        with tracer.start_as_current_span("redis_get"):
            value = await self._redis.get(key)
        COUNTER_READ.labels(counter_name=key).inc()
        if not value:
            return 0
        return int(value)
