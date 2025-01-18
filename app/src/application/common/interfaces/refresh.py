from abc import ABC, abstractmethod
from uuid import UUID

from src.application.auth.dto import RefreshSession


class RefreshTokenRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, refresh_session: RefreshSession) -> None: ...

    @abstractmethod
    async def delete_by_token(self, refresh_token: str) -> None: ...

    @abstractmethod
    async def delete_by_user_id(self, user_id: UUID) -> None: ...

    @abstractmethod
    async def get(self, refresh_token: str) -> RefreshSession | None: ...

    @abstractmethod
    async def get_by_user_id_and_user_agent(self, user_id: UUID, user_agent: str) -> RefreshSession | None: ...
