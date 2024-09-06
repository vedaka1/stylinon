import pytest
from dishka import AsyncContainer
from src.domain.users.entities import User
from src.domain.users.repository import UserRepositoryInterface

pytestmark = pytest.mark.asyncio(loop_scope="session")


class TestUser:
    @staticmethod
    def create_user() -> User:
        return User.create(
            email="test@test.com",
            hashed_password="test",
            mobile_phone="89999999999",
            first_name="test_first_name",
            last_name="test_last_name",
        )

    @staticmethod
    def check_user(user_data: User | None) -> None:
        assert user_data
        assert user_data.email == "test@test.com"
        assert user_data.hashed_password == "test"
        assert user_data.mobile_phone == "89999999999"
        assert user_data.first_name == "test_first_name"
        assert user_data.last_name == "test_last_name"
        assert user_data.is_verified is False


class TestUserRepository:
    async def test_create_user(self, container: AsyncContainer) -> None:
        async with container() as di_container:
            user_repository = await di_container.get(UserRepositoryInterface)
            # Create user
            user = TestUser.create_user()
            await user_repository.create(user)
            # Check it
            user_data = await user_repository.get_by_id(user.id)
            TestUser.check_user(user_data)

    async def test_delete_user(self, container: AsyncContainer) -> None:
        async with container() as di_container:
            user_repository = await di_container.get(UserRepositoryInterface)
            # Create user
            user = TestUser.create_user()
            await user_repository.create(user)
            # Delete user
            await user_repository.delete(user.id)
            # Check it
            result = await user_repository.get_by_id(user.id)
            assert result is None

    async def test_get_user_by_email(self, container: AsyncContainer) -> None:
        async with container() as di_container:
            user_repository = await di_container.get(UserRepositoryInterface)
            # Create user
            user = TestUser.create_user()
            await user_repository.create(user)
            # Check it and get it
            user_data = await user_repository.get_by_email(user.email)
            TestUser.check_user(user_data)

    async def test_get_all_users(self, container: AsyncContainer) -> None:
        async with container() as di_container:
            user_repository = await di_container.get(UserRepositoryInterface)
            # Create users
            user = TestUser.create_user()
            await user_repository.create(user)
            # Check users
            users = await user_repository.get_many(offset=0, limit=10)
            assert len(users) == 1
            users = await user_repository.get_many(offset=0, limit=10, search="test")
            assert len(users) == 1
            users = await user_repository.get_many(offset=1, limit=10, search="test")
            assert len(users) == 0
            users = await user_repository.get_many(offset=0, limit=10, search="1q2w3e")
            assert len(users) == 0

    async def test_count(self, container: AsyncContainer) -> None:
        async with container() as di_container:
            user_repository = await di_container.get(UserRepositoryInterface)
            # Create users
            user = TestUser.create_user()
            await user_repository.create(user)
            count = await user_repository.count()
            assert count == 1
            count = await user_repository.count(search="test")
            assert count == 1
            count = await user_repository.count(search="1q2w3e")
            assert count == 0
