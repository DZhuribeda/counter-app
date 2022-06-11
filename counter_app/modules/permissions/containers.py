from dependency_injector import containers, providers
from counter_app.modules.permissions.service import PermissionsService


class PermissionsContainer(containers.DeclarativeContainer):

    config = providers.Configuration()
    gateways = providers.DependenciesContainer()

    permissions_service = providers.Factory(
        PermissionsService,
        spicedb_client=gateways.spicedb_client,
    )
