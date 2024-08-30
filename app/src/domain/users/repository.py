from abc import ABC, abstractmethod
from enum import Enum
from uuid import UUID

from src.domain.users.entities import User


class UserPrimaryKey(Enum):
    ID = "id"
    EMAIL = "email"


class UserRepositoryInterface(ABC):

    @abstractmethod
    async def create(self, user: User) -> None: ...

    @abstractmethod
    async def update(self, user: User) -> None: ...

    @abstractmethod
    async def delete(self, user_id: UUID) -> None: ...

    @abstractmethod
    async def _get_by(self, key: UserPrimaryKey, value: UUID | str) -> User | None: ...

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def get_many(
        self, offset: int, limit: int, search: str | None = None
    ) -> list[User]: ...

    @abstractmethod
    async def count(self, search: str | None = None) -> int: ...
