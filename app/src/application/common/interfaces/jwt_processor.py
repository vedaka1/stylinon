from abc import ABC, abstractmethod
from enum import Enum
from typing import Any
from uuid import UUID

from src.application.auth.dto import UserTokenData
from src.domain.users.entities import UserRole


class TokenType(Enum):
    ACCESS = 'access_token'
    REFRESH = 'refresh_token'
    RESET = 'reset_token'


class JWTProcessorInterface(ABC):
    @abstractmethod
    def create_access_token(self, user_id: UUID, user_role: UserRole, email: str) -> str: ...

    @abstractmethod
    def create_refresh_token(self, user_id: UUID) -> str: ...

    @abstractmethod
    def create_reset_password_token(self, email: str) -> str: ...

    @abstractmethod
    def _generate_token(self, token_type: TokenType, payload: dict[str, Any]) -> str: ...

    @abstractmethod
    def validate_access_token(self, token: str) -> UserTokenData: ...

    @abstractmethod
    def validate_refresh_token(self, token: str) -> UUID: ...

    @abstractmethod
    def validate_acquiring_token(self, token: str) -> dict[str, Any]: ...

    @abstractmethod
    def validate_reset_password_token(self, token: str) -> dict[str, Any]: ...
