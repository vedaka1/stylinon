from typing import AsyncIterable

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from src.infrastructure.settings import settings


def get_async_engine(db_url: str = settings.db.DB_URL) -> AsyncEngine:
    return create_async_engine(url=db_url, echo=False)


def get_async_sessionmaker(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_async_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncIterable[AsyncSession]:
    async with session_factory() as session:
        yield session
        await session.close()
