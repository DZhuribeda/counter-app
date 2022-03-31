from aioredis import Redis

from counter_app.metric import COUNTER_INCREMENT, COUNTER_RESET, COUNTER_READ


class Service:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def increment(self, key: str) -> int:
        value = await self._redis.incr(key)
        COUNTER_INCREMENT.labels(counter_name=key).inc()
        return value

    async def set_value(self, key: str, value: int = 0) -> None:
        COUNTER_RESET.labels(counter_name=key).inc()
        await self._redis.set(key, value)

    async def get_value(self, key: str) -> int:
        value = await self._redis.get(key)
        COUNTER_READ.labels(counter_name=key).inc()
        if not value:
            return 0
        return int(value)
