from dataclasses import dataclass
from uuid import UUID

from pydantic import EmailStr
from src.application.common.pagination import PaginationQuery
from src.domain.users.entities import User


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
