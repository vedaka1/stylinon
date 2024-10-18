import pytest
from httpx import AsyncClient

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
        assert response.cookies.get("session") is not None
        # assert response.cookies.get("refresh_token") is not None

    @pytest.mark.usefixtures("clean_users_table")
    async def test_register(self, client: AsyncClient) -> None:
        await self._register_request(client)

    @pytest.mark.usefixtures("clean_users_table")
    async def test_login(self, client: AsyncClient) -> None:
        await self._register_request(client)
        await self._login_request(client)

    # @pytest.mark.usefixtures("clean_users_table")
    # async def test_refresh_token(self, client: AsyncClient) -> None:
    #     await self._register_request(client)
    #     await self._login_request(client)
    #     response = await client.post("/auth/refresh")
    #     assert response.status_code == 200
    #     assert response.cookies.get("session") is not None

    @pytest.mark.usefixtures("clean_users_table")
    async def test_logout(self, client: AsyncClient) -> None:
        await self._register_request(client)
        await self._login_request(client)
        response = await client.post("/auth/logout")
        assert response.status_code == 200
        assert response.cookies.get("session") is None
