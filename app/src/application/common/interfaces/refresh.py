from abc import ABC, abstractmethod

from src.application.auth.dto import RefreshSession


class RefreshTokenRepositoryInterface(ABC):

    @abstractmethod
    async def create(self, refresh_session: RefreshSession) -> None: ...

    @abstractmethod
    async def delete_by_token(self, refresh_token: str) -> None: ...

    @abstractmethod
    async def get(self, refresh_token: str) -> RefreshSession | None: ...
