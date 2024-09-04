import pytest
from dishka import AsyncContainer
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

pytestmark = pytest.mark.asyncio(loop_scope="session")


class TestAuth:

    async def test_register(self, client: AsyncClient) -> None:
        response = await client.post(
            "/auth/register",
            json={
                "email": "test_auth@test.com",
                "password": "1234qwe",
            },
        )
        assert response.status_code == 201

    # async def test_login(self, client: AsyncClient):
    #     response = await client.post(
    #         "/auth/login",
    #         data={"username": "test_auth@test.com", "password": "1234qwe"},
    #     )
    #     assert response.status_code == 200
    #     print(response.text)
    #     assert response.cookies.get("access_token") is not None

    # async def test_refresh_token(self, client: AsyncClient):
    #     response = await client.post("/auth/refresh")
    #     assert response.status_code == 200
    #     assert response.cookies.get("access_token") is not None
    #     assert response.cookies.get("refresh_token") is not None

    async def test_logout(self, client: AsyncClient, container: AsyncContainer) -> None:
        async with container() as di_container:
            response = await client.post("/auth/logout")
            assert response.status_code == 200
            assert response.cookies.get("access_token") is None
            # assert response.cookies.get("refresh_token") is None
            sessionmaker = await di_container.get(async_sessionmaker[AsyncSession])
            session = sessionmaker()
            await session.execute(
                text("""DELETE FROM users WHERE users.email = 'test_auth@test.com';"""),
            )
            await session.commit()
            await session.close()
