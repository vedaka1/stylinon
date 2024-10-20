import aiohttp
from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from src.application.chats.interface import WebsocketManagerInterface
from src.application.common.email.types import SenderName
from src.application.common.interfaces import SyncSMTPServerInterface
from src.infrastructure.integrations.smtp.server import SyncSMTPServer
from src.infrastructure.persistence.postgresql.database import (
    get_async_engine,
    get_async_sessionmaker,
)
from src.infrastructure.settings import settings
from src.infrastructure.utils.common import StorageBackend
from src.infrastructure.websockets.manager import WebsocketManager


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
        )

    @provide(scope=Scope.APP)
    def websocker_manager(self) -> WebsocketManagerInterface:
        return WebsocketManager()

    @provide(scope=Scope.APP)
    def sender_name(self) -> SenderName:
        return SenderName(settings.smtp.SENDER_NAME)

    @provide(scope=Scope.APP)
    def storage_backend(self) -> StorageBackend:
        return StorageBackend(path="/images")
