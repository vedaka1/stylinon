import logging
from functools import lru_cache
from typing import AsyncGenerator

from dishka import AsyncContainer, Provider, Scope, make_async_container, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from src.application.common.jwt_processor import JwtTokenProcessorInterface
from src.application.common.password_hasher import PasswordHasherInterface
from src.application.common.transaction import TransactionManagerInterface
from src.application.services.order import OrderService
from src.application.services.order_item import OrderItemService
from src.application.services.product import ProductService
from src.application.services.user import UserService
from src.application.usecases.auth import LoginUseCase, RegisterUseCase
from src.application.usecases.order.create import CreateOrderUseCase
from src.application.usecases.order.get import GetManyOrdersUseCase, GetOrderUseCase
from src.application.usecases.order.update import UpdateOrderUseCase
from src.application.usecases.user.get import GetUsersListUseCase, GetUserUseCase
from src.domain.orders.repository import (
    OrderItemRepositoryInterface,
    OrderRepositoryInterface,
)
from src.domain.orders.service import OrderItemServiceInterface, OrderServiceInterface
from src.domain.products.repository import ProductRepositoryInterface
from src.domain.products.service import ProductServiceInterface
from src.domain.users.repository import UserRepositoryInterface
from src.domain.users.service import UserServiceInterface
from src.infrastructure.authentication.jwt_processor import JwtTokenProcessor
from src.infrastructure.authentication.password_hasher import PasswordHasher
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
from src.infrastructure.persistence.postgresql.repositories.user import (
    SqlalchemyUserRepository,
)
from src.infrastructure.persistence.postgresql.transaction import TransactionManager


@lru_cache(1)
def init_logger() -> None:
    logging.basicConfig(
        # filename="log.log",
        level=logging.INFO,
        encoding="UTF-8",
        format="%(asctime)s %(levelname)s: %(message)s",
    )
    return None


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def engine(self) -> AsyncEngine:
        return get_async_engine()

    @provide(scope=Scope.APP)
    def session_factory(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return get_async_sessionmaker(engine)


class SecurityProvider(Provider):
    password_hasher = provide(
        PasswordHasher,
        provides=PasswordHasherInterface,
        scope=Scope.APP,
    )
    jwt_processor = provide(
        JwtTokenProcessor,
        provides=JwtTokenProcessorInterface,
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


class UseCasesProvider(Provider):
    scope = Scope.REQUEST

    register = provide(RegisterUseCase)
    login = provide(LoginUseCase)
    get_user = provide(GetUserUseCase)
    get_users_list = provide(GetUsersListUseCase)
    get_order = provide(GetOrderUseCase)
    create_order = provide(CreateOrderUseCase)
    get_many_orders = provide(GetManyOrdersUseCase)
    update_order = provide(UpdateOrderUseCase)


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    user_service = provide(UserService, provides=UserServiceInterface)
    order_service = provide(OrderService, provides=OrderServiceInterface)
    order_item_service = provide(OrderItemService, provides=OrderItemServiceInterface)
    product_service = provide(ProductService, provides=ProductServiceInterface)


@lru_cache(1)
def get_container() -> AsyncContainer:
    return make_async_container(
        SettingsProvider(),
        SecurityProvider(),
        DatabaseConfigurationProvider(),
        DatabaseAdaptersProvider(),
        ServiceProvider(),
        UseCasesProvider(),
    )
