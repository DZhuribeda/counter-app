from dependency_injector import containers, providers
from counter_app.modules.counter.repository import CounterRepository

from counter_app.modules.counter.service import CounterService


class CounterContainer(containers.DeclarativeContainer):

    config = providers.Configuration()
    gateways = providers.DependenciesContainer()

    counter_repository = providers.Factory(
        CounterRepository,
        redis=gateways.redis_pool,
        edgedb=gateways.edgedb_client,
    )

    counter_service = providers.Factory(
        CounterService,
        counter_repository=counter_repository,
    )
