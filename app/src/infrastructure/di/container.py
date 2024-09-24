import logging
import logging.config
from functools import lru_cache
from typing import AsyncGenerator

import aiohttp
from dishka import AsyncContainer, Provider, Scope, make_async_container, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from src.application.acquiring.interface import AcquiringGatewayInterface
from src.application.acquiring.service import AcquiringService
from src.application.auth.service import AuthService, AuthServiceInterface
from src.application.auth.usecases import (
    LoginUseCase,
    LogoutUseCase,
    PasswordRecoveryUseCase,
    RefreshTokenUseCase,
    RegisterUseCase,
    ResetPasswordUseCase,
)
from src.application.chats.interface import WebsocketManagerInterface
from src.application.chats.usecases.post import SendMessageUseCase
from src.application.common.interfaces.acquiring import AcquiringServiceInterface
from src.application.common.interfaces.jwt_processor import JWTProcessorInterface
from src.application.common.interfaces.password_hasher import PasswordHasherInterface
from src.application.common.interfaces.refresh import RefreshTokenRepositoryInterface
from src.application.common.interfaces.smtp import SyncSMTPServerInterface
from src.application.common.interfaces.transaction import TransactionManagerInterface
from src.application.orders.service import OrderItemService, OrderService
from src.application.orders.usecases import (
    CreateOrderUseCase,
    GetManyOrdersUseCase,
    GetOrderUseCase,
    UpdateOrderByWebhookUseCase,
    UpdateOrderUseCase,
)
from src.application.products.service import ProductService
from src.application.products.usecases import (
    CreateProductUseCase,
    GetManyProductsUseCase,
    GetProductUseCase,
)
from src.application.users.service import UserService
from src.application.users.usecases import (
    GetUserOrdersUseCase,
    GetUsersListUseCase,
    GetUserUseCase,
)
from src.domain.orders.repository import (
    OrderItemRepositoryInterface,
    OrderRepositoryInterface,
)
from src.domain.orders.service import OrderItemServiceInterface, OrderServiceInterface
from src.domain.products.repository import ProductRepositoryInterface
from src.domain.products.service import ProductServiceInterface
from src.domain.users.repository import UserRepositoryInterface
from src.domain.users.service import UserServiceInterface
from src.infrastructure.authentication.jwt_processor import JWTProcessor
from src.infrastructure.authentication.password_hasher import PasswordHasher
from src.infrastructure.integrations.acquiring.main import TochkaAcquiringGateway
from src.infrastructure.integrations.smtp.server import SyncSMTPServer
from src.infrastructure.logging_config import logger_config_dict
from src.infrastructure.persistence.postgresql.database import (
    get_async_engine,
    get_async_sessionmaker,
)
from src.infrastructure.persistence.postgresql.repositories.order import (
    SqlalchemyOrderItemRepository,
    SqlalchemyOrderRepository,
)
from src.infrastructure.persistence.postgresql.repositories.product import (
    SqlalchemyProductRepository,
)
from src.infrastructure.persistence.postgresql.repositories.refresh import (
    RefreshTokenRepository,
)
from src.infrastructure.persistence.postgresql.repositories.user import (
    SqlalchemyUserRepository,
)
from src.infrastructure.persistence.postgresql.transaction import TransactionManager
from src.infrastructure.settings import settings
from src.infrastructure.websockets.manager import WebsocketManager


@lru_cache(1)
def init_logger() -> None:
    logging.config.dictConfig(logger_config_dict)
    return None


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def engine(self) -> AsyncEngine:
        return get_async_engine()

    @provide(scope=Scope.APP)
    def session_factory(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return get_async_sessionmaker(engine)

    @provide(scope=Scope.APP)
    def acquiring_session(self) -> aiohttp.ClientSession:
        headers = {"Authorization": f"Bearer {settings.tochka.TOKEN}"}
        return aiohttp.ClientSession(headers=headers)

    @provide(scope=Scope.APP)
    def smtp_server(self) -> SyncSMTPServerInterface:
        return SyncSMTPServer(
            from_address=settings.smtp.FROM_EMAIL,
            password=settings.smtp.PASSWORD,
            subject=settings.smtp.EMAIL_SUBJECT,
        )

    @provide(scope=Scope.APP)
    def websocker_manager(self) -> WebsocketManagerInterface:
        return WebsocketManager()


class SecurityProvider(Provider):
    password_hasher = provide(
        PasswordHasher,
        provides=PasswordHasherInterface,
        scope=Scope.APP,
    )
    jwt_processor = provide(
        JWTProcessor,
        provides=JWTProcessorInterface,
        scope=Scope.APP,
    )


class DatabaseConfigurationProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def provide_db_connection(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> AsyncGenerator[AsyncSession, None]:
        session: AsyncSession = session_factory()
        yield session
        await session.close()


class DatabaseAdaptersProvider(Provider):
    scope = Scope.REQUEST

    transaction_manager = provide(
        TransactionManager,
        provides=TransactionManagerInterface,
    )
    user_repository = provide(
        SqlalchemyUserRepository,
        provides=UserRepositoryInterface,
    )
    order_repositoty = provide(
        SqlalchemyOrderRepository,
        provides=OrderRepositoryInterface,
    )
    order_item_repositoty = provide(
        SqlalchemyOrderItemRepository,
        provides=OrderItemRepositoryInterface,
    )
    product_repository = provide(
        SqlalchemyProductRepository,
        provides=ProductRepositoryInterface,
    )
    refresh_session_repository = provide(
        RefreshTokenRepository,
        provides=RefreshTokenRepositoryInterface,
    )


class UseCasesProvider(Provider):
    scope = Scope.REQUEST

    register = provide(RegisterUseCase)
    login = provide(LoginUseCase)
    logout = provide(LogoutUseCase)
    refresh_token = provide(RefreshTokenUseCase)
    get_user = provide(GetUserUseCase)
    get_users_list = provide(GetUsersListUseCase)
    get_user_orders_list = provide(GetUserOrdersUseCase)
    get_order = provide(GetOrderUseCase)
    create_order = provide(CreateOrderUseCase)
    get_many_orders = provide(GetManyOrdersUseCase)
    update_order = provide(UpdateOrderUseCase)
    update_order_by_webhook = provide(UpdateOrderByWebhookUseCase)
    get_product = provide(GetProductUseCase)
    create_product = provide(CreateProductUseCase)
    get_many_products = provide(GetManyProductsUseCase)
    send_recovery_email = provide(PasswordRecoveryUseCase)
    reset_password = provide(ResetPasswordUseCase)
    send_message = provide(SendMessageUseCase)


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    user_service = provide(UserService, provides=UserServiceInterface)
    acquiring_service = provide(AcquiringService, provides=AcquiringServiceInterface)
    auth_service = provide(AuthService, provides=AuthServiceInterface)
    order_service = provide(OrderService, provides=OrderServiceInterface)
    order_item_service = provide(OrderItemService, provides=OrderItemServiceInterface)
    product_service = provide(ProductService, provides=ProductServiceInterface)


class GatewayProvider(Provider):
    scope = Scope.REQUEST

    acquiring_gateway = provide(
        TochkaAcquiringGateway,
        provides=AcquiringGatewayInterface,
    )


@lru_cache(1)
def get_container() -> AsyncContainer:
    return make_async_container(
        SettingsProvider(),
        SecurityProvider(),
        DatabaseConfigurationProvider(),
        DatabaseAdaptersProvider(),
        ServiceProvider(),
        UseCasesProvider(),
        GatewayProvider(),
    )
