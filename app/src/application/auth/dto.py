from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import UUID, uuid4

from src.domain.users.entities import UserRole
from src.infrastructure.settings import settings


@dataclass
class Token:
    access_token: str
    refresh_token: str
    access_max_age: int
    refresh_max_age: int
    type: str = "Bearer "


@dataclass
class RefreshSession:
    user_id: UUID
    refresh_token: str
    expires_at: datetime

    def __post_init__(self) -> None:
        token = self.refresh_token.removeprefix("Bearer ")
        self.refresh_token = token

    @staticmethod
    def create(user_id: UUID, refresh_token: str) -> "RefreshSession":
        return RefreshSession(
            user_id=user_id,
            refresh_token=refresh_token,
            expires_at=datetime.now()
            + timedelta(days=settings.jwt.REFRESH_TOKEN_EXPIRE_DAYS),
        )


@dataclass
class UserTokenData:
    user_id: UUID
    email: str
    role: str
