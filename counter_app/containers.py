from dependency_injector import containers, providers


from . import redis
from counter_app.modules.auth.service import AuthenticationService, JWKClient
from counter_app.modules.counter.service import CounterService


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    redis_pool = providers.Resource(
        redis.init_redis_pool,
        redis_dsn=config.redis_dsn,
        max_connections=config.redis_max_connections,
    )

    jwks_client = providers.Singleton(
        JWKClient,
        uri=config.jwks_url,
        cache_keys=config.jwks_cache_keys,
    )

    counter_service = providers.Factory(
        CounterService,
        redis=redis_pool,
    )

    authentication_service = providers.Factory(
        AuthenticationService,
        jwks_client=jwks_client,
    )
