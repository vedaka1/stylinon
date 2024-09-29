import logging
import os
import typing
from typing import AsyncGenerator, Generator, cast

import aiohttp
import pytest
from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from src.application.chats.interface import WebsocketManagerInterface
from src.application.common.interfaces.smtp import SyncSMTPServerInterface
from src.application.common.response import ErrorAPIResponse
from src.domain.common.exceptions.base import ApplicationException
from src.infrastructure.di.container import (
    DatabaseAdaptersProvider,
    DatabaseConfigurationProvider,
    GatewayProvider,
    SecurityProvider,
    ServiceProvider,
    UseCasesProvider,
)
from src.infrastructure.integrations.smtp.server import SyncSMTPServer
from src.infrastructure.persistence.postgresql.database import (
    get_async_engine,
    get_async_sessionmaker,
)
from src.infrastructure.persistence.postgresql.models import Base
from src.infrastructure.settings import settings
from src.infrastructure.websockets.manager import WebsocketManager
from src.presentation.api.v1.router import api_router as api_router_v1
from starlette.types import ExceptionHandler
from testcontainers.postgres import PostgresContainer

_Message = typing.Dict[str, typing.Any]
_Receive = typing.Callable[[], typing.Awaitable[_Message]]
_Send = typing.Callable[
    [typing.Dict[str, typing.Any]],
    typing.Coroutine[None, None, None],
]
_ASGIApp = typing.Callable[
    [typing.Dict[str, typing.Any], _Receive, _Send],
    typing.Coroutine[None, None, None],
]
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def postgres_url() -> Generator[str, None, None]:
    postgres = PostgresContainer(
        image="postgres:15-alpine",
        username="username",
        password="password",
        dbname="test",
    )
    if os.name == "nt":
        postgres.get_container_host_ip = lambda: "localhost"
    try:
        postgres.start()
        postgres_url_ = postgres.get_connection_url().replace("psycopg2", "asyncpg")
        logger.info("postgres url %s", postgres_url_)
        yield postgres_url_
    finally:
        postgres.stop()


@pytest.fixture(scope="session", autouse=True)
async def setup_db(postgres_url: str) -> AsyncGenerator[None, None]:
    engine = get_async_engine(postgres_url)
    print("URL: ", postgres_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


@pytest.fixture(scope="session")
async def container(postgres_url: str) -> AsyncGenerator[AsyncContainer, None]:
    from dishka import AsyncContainer, Provider, Scope, make_async_container, provide

    class SettingsProvider(Provider):
        @provide(scope=Scope.APP)
        def engine(self) -> AsyncEngine:
            return get_async_engine(db_url=postgres_url)

        @provide(scope=Scope.APP)
        def session_factory(
            self,
            engine: AsyncEngine,
        ) -> async_sessionmaker[AsyncSession]:
            return get_async_sessionmaker(engine)

        @provide(scope=Scope.APP)
        def smtp_server(self) -> SyncSMTPServerInterface:
            return SyncSMTPServer(
                from_address=settings.smtp.FROM_EMAIL,
                password=settings.smtp.PASSWORD,
                subject=settings.smtp.EMAIL_SUBJECT,
            )

        @provide(scope=Scope.APP)
        async def acquiring_session(
            self,
        ) -> AsyncGenerator[aiohttp.ClientSession, None]:
            headers = {"Authorization": f"Bearer {settings.tochka.TOKEN}"}
            acquiring_session = aiohttp.ClientSession(headers=headers)
            yield acquiring_session
            await acquiring_session.close()

        @provide(scope=Scope.APP)
        def websocker_manager(self) -> WebsocketManagerInterface:
            return WebsocketManager()

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

    container = get_container()
    yield container
    await container.close()


async def application_exception_handler(
    request: Request,
    exc: ApplicationException,
) -> ORJSONResponse:
    logger.error(msg="Handle error", exc_info=exc, extra={"error": exc})
    return ErrorAPIResponse(details=exc.message, status_code=exc.status_code)


def init_exc_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        ApplicationException,
        cast(ExceptionHandler, application_exception_handler),
    )


@pytest.fixture(scope="session")
def app(container: AsyncContainer) -> Generator[FastAPI, None, None]:
    app = FastAPI()

    api_v1 = FastAPI()
    setup_dishka(container, api_v1)
    init_exc_handlers(api_v1)
    api_v1.include_router(api_router_v1)
    api_v1.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "HEAD", "OPTIONS", "DELETE", "PUT", "PATCH"],
        allow_headers=[
            "Access-Control-Allow-Headers",
            "Content-Type",
            "Authorization",
            "Access-Control-Allow-Origin",
        ],
    )
    app.mount("/api/v1", api_v1)
    yield app


@pytest.fixture(scope="session")
def client(app: FastAPI) -> Generator[AsyncClient, None, None]:
    client = AsyncClient(
        base_url="http://localhost:5000/api/v1",
        transport=ASGITransport(app=cast(_ASGIApp, app)),
    )
    yield client


@pytest.fixture
async def clean_users_table(container: AsyncContainer) -> AsyncGenerator[None, None]:
    yield
    async with container() as di_container:
        sessionmaker = await di_container.get(async_sessionmaker[AsyncSession])
        async with sessionmaker() as session:
            await session.execute(text("DELETE FROM users"))
            await session.commit()


@pytest.fixture
async def clean_orders_table(container: AsyncContainer) -> AsyncGenerator[None, None]:
    yield
    async with container() as di_container:
        sessionmaker = await di_container.get(async_sessionmaker[AsyncSession])
        async with sessionmaker() as session:
            await session.execute(text("DELETE FROM orders"))
            await session.commit()
