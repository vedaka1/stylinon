from abc import ABC, abstractmethod

from src.application.auth.dto import UserData


class IdentityProviderInterface(ABC):

    @abstractmethod
    async def get_current_user(self, authorization: str | None) -> UserData: ...
