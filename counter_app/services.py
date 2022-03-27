from aioredis import Redis


class Service:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def increment(self, key: str) -> int:
        return await self._redis.incr(key)

    async def set_value(self, key: str, value: int = 0) -> None:
        await self._redis.set(key, value)

    async def get_value(self, key: str) -> int:
        value = await self._redis.get(key)
        if not value:
            return 0
        return int(value)
