from dataclasses import dataclass
from uuid import UUID

from pydantic import EmailStr


@dataclass
class RegisterCommand:
    email: EmailStr
    password: str
    mobile_phone: str | None = None
    first_name: str | None = None
    last_name: str | None = None


@dataclass
class LoginCommand:
    password: str
    username: str
    user_agent: str


@dataclass
class LogoutWithJWTCommand:
    refresh_token: str


@dataclass
class LogoutWithSessionCommand:
    session_id: UUID


@dataclass
class ResetPasswordCommand:
    reset_token: str
    new_password: str


@dataclass
class RefreshTokenCommand:
    refresh_token: str
