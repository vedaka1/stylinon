from dataclasses import dataclass
from re import M
from uuid import UUID

from src.application.common.pagination import PaginationQuery


@dataclass
class CreateMessageCommand:
    message: str


@dataclass
class CreateChatCommand:
    title: str


@dataclass
class GetChatsListCommand:
    pagination: PaginationQuery
    search: str | None = None
