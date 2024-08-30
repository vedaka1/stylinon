import logging
import os
from functools import lru_cache
from typing import Generator

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
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
from src.infrastructure.persistence.postgresql.models import *
from src.infrastructure.settings import settings
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
async def setup_db(postgres_url: str):
    engine = get_async_engine(postgres_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


@pytest.fixture
def container(postgres_url: str):
    from dishka import AsyncContainer, Provider, Scope, make_async_container, provide

    class SettingsProvider(Provider):
        @provide(scope=Scope.APP)
        def engine(self) -> AsyncEngine:
            return get_async_engine(db_url=postgres_url)

        @provide(scope=Scope.APP)
        def session_factory(self, engine: AsyncEngine) -> async_sessionmaker:
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
