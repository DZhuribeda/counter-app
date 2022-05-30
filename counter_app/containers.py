from dependency_injector import containers, providers

from counter_app.modules.counter.containers import CounterContainer


from . import services
from counter_app.modules.auth.service import AuthenticationService, JWKClient


class Gateways(containers.DeclarativeContainer):
    config = providers.Configuration()

    edgedb_client = providers.Resource(
        services.init_edgedb_client,
    )

    redis_pool = providers.Resource(
        services.init_redis_pool,
        redis_dsn=config.redis_dsn,
        max_connections=config.redis_max_connections,
    )


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    gateways = providers.Container(
        Gateways,
        config=config,
    )

    counter = providers.Container(
        CounterContainer,
        config=config,
        gateways=gateways,
    )

    jwks_client = providers.Singleton(
        JWKClient,
        uri=config.jwks_url,
        cache_keys=config.jwks_cache_keys,
    )

    authentication_service = providers.Factory(
        AuthenticationService,
        jwks_client=jwks_client,
    )
