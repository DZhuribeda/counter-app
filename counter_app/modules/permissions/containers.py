from dependency_injector import containers, providers
from counter_app.modules.permissions.service import PermissionsService


class PermissionsContainer(containers.DeclarativeContainer):

    config = providers.Configuration()
    gateways = providers.DependenciesContainer()

    permissions_service = providers.Factory(
        PermissionsService,
        keto_write_service=gateways.keto_writer,
        keto_check_service=gateways.keto_check_service,
    )
