from typing import AsyncGenerator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.application.common.interfaces.refresh import RefreshTokenRepositoryInterface
from src.application.common.interfaces.transaction import TransactionManagerInterface
from src.domain.chats.repository import (
    ChatRepositoryInterface,
    MessageRepositoryInterface,
)
from src.domain.orders.repository import (
    OrderItemRepositoryInterface,
    OrderRepositoryInterface,
)
from src.domain.products.repository import ProductRepositoryInterface
from src.domain.users.repository import UserRepositoryInterface
from src.infrastructure.persistence.postgresql.repositories import (
    SqlalchemyChatRepository,
    SqlalchemyMessageRepository,
    SqlalchemyOrderItemRepository,
    SqlalchemyOrderRepository,
    SqlalchemyProductRepository,
    SqlalchemyRefreshTokenRepository,
    SqlalchemyUserRepository,
)
from src.infrastructure.persistence.postgresql.transaction import TransactionManager


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
        SqlalchemyRefreshTokenRepository,
        provides=RefreshTokenRepositoryInterface,
    )
    chat_repository = provide(
        SqlalchemyChatRepository,
        provides=ChatRepositoryInterface,
    )
    message_repository = provide(
        SqlalchemyMessageRepository,
        provides=MessageRepositoryInterface,
    )