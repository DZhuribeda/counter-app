from typing import AsyncIterator

import aioredis
import edgedb
from authzed.api.v1 import Client
from grpcutil import insecure_bearer_token_credentials


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


async def init_spicedb(
    spicedb_grpc_url: str,
    spicedb_grpc_preshared_key: str,
) -> AsyncIterator[Client]:
    client = Client(
        spicedb_grpc_url,
        insecure_bearer_token_credentials(spicedb_grpc_preshared_key),
    )
    yield client
    client.close()
