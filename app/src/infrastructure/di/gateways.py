from dishka import Provider, Scope, provide
from src.application.acquiring.interface import AcquiringGatewayInterface
from src.infrastructure.integrations.acquiring.gateway import TochkaAcquiringGateway


class GatewayProvider(Provider):
    scope = Scope.APP

    acquiring_gateway = provide(
        TochkaAcquiringGateway,
        provides=AcquiringGatewayInterface,
    )
