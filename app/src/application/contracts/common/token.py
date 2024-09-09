from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import UUID

from pytz import timezone
from src.domain.users.entities import UserRole
from src.infrastructure.settings import settings

tz_Moscow = timezone("Europe/Moscow")


@dataclass
class Token:
    access_token: str
    refresh_token: str
    access_max_age: int
    refresh_max_age: int
    token_type: str = "Bearer"


@dataclass
class UserTokenData:
    user_id: UUID
    email: str
    role: str


@dataclass
class RefreshSession:
    refresh_token: str
    user_id: UUID
    expires_at: datetime

    def __post_init__(self) -> None:
        token = self.refresh_token.split()[-1]
        self.refresh_token = token

    @staticmethod
    def create(refresh_token: str, user_id: UUID) -> "RefreshSession":
        return RefreshSession(
            refresh_token=refresh_token,
            user_id=user_id,
            expires_at=datetime.now()
            + timedelta(days=settings.jwt.REFRESH_TOKEN_EXPIRE_DAYS),
        )
