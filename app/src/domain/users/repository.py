from abc import ABC, abstractmethod
from enum import Enum
from uuid import UUID

from src.domain.users.entities import User, UserSession


class UserPrimaryKey(Enum):
    ID = 'id'
    EMAIL = 'email'


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
        self,
        search: str | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> list[User]: ...

    @abstractmethod
    async def count(self, search: str | None = None) -> int: ...


class UserSessionRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, session: UserSession) -> None: ...

    @abstractmethod
    async def update(self, session: UserSession) -> None: ...

    @abstractmethod
    async def delete(self, session_id: UUID) -> None: ...

    @abstractmethod
    async def get_by_id(self, session_id: UUID) -> UserSession | None: ...

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> list[UserSession]: ...

    @abstractmethod
    async def get_by_user_id_and_user_agent(self, user_id: UUID, user_agent: str) -> UserSession | None: ...
