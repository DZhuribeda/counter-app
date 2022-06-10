from typing import AsyncIterator

import aioredis
import edgedb
import grpc

from counter_app.ory.keto.acl.v1alpha1.write_service_pb2_grpc import WriteServiceStub


async def init_redis_pool(
    redis_dsn: str, max_connections: int
) -> AsyncIterator[aioredis.Redis]:
    pool = aioredis.ConnectionPool.from_url(redis_dsn, max_connections=max_connections)
    redis = aioredis.Redis(connection_pool=pool)
    yield redis
    await redis.close()


async def init_edgedb_client() -> AsyncIterator[edgedb.AsyncIOClient]:
    client = edgedb.create_async_client()
    yield client
    await client.close()


async def init_keto_write_grpc_client(
    keto_write_url: str,
) -> AsyncIterator[WriteServiceStub]:
    async with grpc.aio.insecure_channel(keto_write_url) as channel:
        yield WriteServiceStub(channel)


async def init_keto_read_grpc_channel(
    keto_read_url: str,
) -> AsyncIterator[grpc.aio.Channel]:
    async with grpc.aio.insecure_channel(keto_read_url) as channel:
        yield channel
