from dependency_injector import containers, providers

from . import redis, services


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    redis_pool = providers.Resource(
        redis.init_redis_pool,
        redis_dsn=config.redis_dsn,
        max_connections=config.redis_max_connections,
    )

    service = providers.Factory(
        services.Service,
        redis=redis_pool,
    )
