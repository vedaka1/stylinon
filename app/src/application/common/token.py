from dataclasses import dataclass
from uuid import UUID

from src.domain.users.entities import UserRole


@dataclass
class Token:
    access_token: str
    refresh_token: str
    access_max_age: int
    refresh_max_age: int
    token_type: str


@dataclass
class UserTokenData:
    user_id: UUID
    role: UserRole
