from abc import ABC, abstractmethod
from uuid import UUID

from src.application.auth.dto import UserTokenData


class IdentityProviderInterface(ABC):

    @abstractmethod
    async def get_current_user(self, authorization: str | None) -> UserTokenData: ...
