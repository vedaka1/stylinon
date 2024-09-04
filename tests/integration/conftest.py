import typing
from typing import AsyncGenerator, Generator, cast

import pytest
from dishka import AsyncContainer
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.application.common.transaction import TransactionManagerInterface

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


@pytest.fixture(scope="session")
def client(app: FastAPI) -> Generator[AsyncClient, None, None]:
    client = AsyncClient(
        base_url="http://localhost:5000/api/v1",
        transport=ASGITransport(app=cast(_ASGIApp, app)),
    )
    yield client


@pytest.fixture
async def users_table(container: AsyncContainer) -> AsyncGenerator[None, None]:
    async with container() as di_container:
        sessionmaker = await di_container.get(async_sessionmaker[AsyncSession])
        transaction_manager = await di_container.get(TransactionManagerInterface)
        session = sessionmaker()
        yield
        await session.execute(text("""DELETE FROM users;"""))
        await transaction_manager.commit()
