import logging
import os
from functools import lru_cache
from typing import AsyncGenerator, Generator, cast

import pytest
from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from src.application.contracts.common.response import ErrorAPIResponse
from src.domain.exceptions.base import ApplicationException
from src.infrastructure.di.container import (
    DatabaseAdaptersProvider,
    DatabaseConfigurationProvider,
    SecurityProvider,
    ServiceProvider,
    UseCasesProvider,
)
from src.infrastructure.persistence.postgresql.database import (
    get_async_engine,
    get_async_sessionmaker,
)
from src.infrastructure.persistence.postgresql.models import (
    Base,
    OrderItemModel,
    OrderModel,
    ProductModel,
    UserModel,
)
from src.presentation.api.v1.router import api_router as api_router_v1
from starlette.types import ExceptionHandler
from testcontainers.postgres import PostgresContainer

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
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


@pytest.fixture(scope="session")
def container(postgres_url: str) -> Generator[AsyncContainer, None, None]:
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

    container = get_container()
    yield container


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
