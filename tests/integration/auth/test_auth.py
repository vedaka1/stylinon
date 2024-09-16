import pytest
from dishka import AsyncContainer
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

pytestmark = pytest.mark.asyncio(loop_scope="session")


class TestAuth:

    async def _register_request(self, client: AsyncClient) -> None:
        response = await client.post(
            "/auth/register",
            json={
                "email": "test_auth@test.com",
                "password": "1234qwe",
            },
        )
        assert response.status_code == 201

    async def _login_request(self, client: AsyncClient) -> None:
        response = await client.post(
            "/auth/login",
            data={"username": "test_auth@test.com", "password": "1234qwe"},
        )
        assert response.status_code == 200
        assert response.cookies.get("access_token") is not None
        assert response.cookies.get("refresh_token") is not None

    @pytest.mark.usefixtures("clean_users_table")
    async def test_register(self, client: AsyncClient) -> None:
        await self._register_request(client)

    @pytest.mark.usefixtures("clean_users_table")
    async def test_login(self, client: AsyncClient) -> None:
        await self._register_request(client)
        await self._login_request(client)

    # async def test_refresh_token(self, client: AsyncClient):
    #     response = await client.post("/auth/refresh", cookies=client.cookies)
    #     assert response.status_code == 200
    #     assert response.cookies.get("access_token") is not None
    #     assert response.cookies.get("refresh_token") is not None

    # @pytest.mark.usefixtures("clean_users_table")
    # async def test_logout(self, client: AsyncClient) -> None:
    #     await self._register_request(client)
    #     await self._login_request(client)
    # headers = {
    #     "Cookies": f"access_token={client.cookies['access_token']}; refresh_token={client.cookies['access_token']}",
    # }
    # response = await client.post("/auth/logout", headers=headers)
    # response = await client.get("/users/me")
    # print(response)
    # assert response.status_code == 200
    # assert response.cookies.get("access_token") is None
    # assert response.cookies.get("refresh_token") is None
