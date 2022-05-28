from dependency_injector import containers, providers

from . import redis
from counter_app.modules.counter.service import CounterService


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    redis_pool = providers.Resource(
        redis.init_redis_pool,
        redis_dsn=config.redis_dsn,
        max_connections=config.redis_max_connections,
    )

    counter_service = providers.Factory(
        CounterService,
        redis=redis_pool,
    )
