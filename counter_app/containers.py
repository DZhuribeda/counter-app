from dependency_injector import containers, providers

from counter_app.modules.counter.containers import CounterContainer
from counter_app.modules.permissions.containers import PermissionsContainer


from . import services
from counter_app.modules.auth.service import AuthenticationService, JWKClient
from counter_app.ory.keto.acl.v1alpha1.check_service_pb2_grpc import CheckServiceStub
from counter_app.ory.keto.acl.v1alpha1.expand_service_pb2_grpc import ExpandServiceStub
from counter_app.ory.keto.acl.v1alpha1.read_service_pb2_grpc import ReadServiceStub


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

    keto_writer = providers.Resource(
        services.init_keto_write_grpc_client,
        keto_write_url=config.keto_write_url,
    )

    keto_read_channel = providers.Resource(
        services.init_keto_read_grpc_channel,
        keto_read_url=config.keto_read_url,
    )

    keto_check_service = providers.Factory(
        CheckServiceStub,
        keto_read_channel,
    )

    keto_read_service = providers.Factory(
        ReadServiceStub,
        keto_read_channel,
    )

    keto_expand_service = providers.Factory(
        ExpandServiceStub,
        keto_read_channel,
    )


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    gateways = providers.Container(
        Gateways,
        config=config,
    )

    permissions = providers.Container(
        PermissionsContainer,
        config=config,
        gateways=gateways,
    )

    counter = providers.Container(
        CounterContainer,
        config=config,
        gateways=gateways,
        permissions=permissions,
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
