from dataclasses import dataclass
from uuid import UUID

from pydantic import EmailStr
from src.application.common.pagination import PaginationQuery
from src.domain.users.entities import User


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


@dataclass
class GetUserCommand:
    user_id: UUID


@dataclass
class DeleteUserCommand:
    user_id: UUID


@dataclass
class UpdateUserCommand:
    user_id: UUID
    user: User


@dataclass
class GetUsersListCommand:
    search: str | None
    pagiantion: PaginationQuery


@dataclass
class UserConfirmationCommand:
    id: UUID
    code: UUID
