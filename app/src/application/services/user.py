from dataclasses import dataclass
from uuid import UUID

from src.domain.exceptions.user import UserAlreadyExistsException, UserNotFoundException
from src.domain.users.entities import User
from src.domain.users.repository import UserRepositoryInterface
from src.domain.users.service import UserServiceInterface


class UserService(UserServiceInterface):
    __slots__ = ["user_repository"]

    def __init__(
        self,
        user_repository: UserRepositoryInterface,
    ) -> None:
        self.user_repository = user_repository

    async def create(self, user: User) -> None:
        user_exist = await self.get_by_email(email=user.email)
        if user_exist:
            raise UserAlreadyExistsException
        await self.user_repository.create(user=user)
        return None

    async def update(self, user_id: UUID, user: User) -> None:
        await self.get_by_id(user_id=user_id)
        await self.user_repository.update(user_id=user_id, user=user)
        return None

    async def delete(self, user_id: UUID) -> None:
        await self.get_by_id(user_id=user_id)
        await self.user_repository.delete(user_id=user_id)
        return None

    async def get_by_id(self, user_id: UUID) -> User:
        user = await self.user_repository.get_by_id(user_id=user_id)
        if not user:
            raise UserNotFoundException
        return user

    async def get_by_email(self, email: str) -> User | None:
        return await self.user_repository.get_by_email(email=email)

    async def get_many(
        self, offset: int, limit: int, search: str | None = None
    ) -> list[User]:
        return await self.user_repository.get_many(
            offset=offset, limit=limit, search=search
        )

    async def count(self, search: str | None = None) -> int:
        return await self.user_repository.count(search=search)
