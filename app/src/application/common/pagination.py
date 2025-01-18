from dataclasses import dataclass
from typing import Generic, TypeVar

from pydantic import BaseModel

TListItem = TypeVar('TListItem')


class PaginationOutSchema(BaseModel):
    limit: int
    page: int
    total: int


class PaginationQuery(BaseModel):
    page: int
    limit: int

    @property
    def offset(self) -> int:
        return self.page * self.limit


@dataclass
class ListPaginatedResponse(Generic[TListItem]):
    items: list[TListItem]
    pagination: PaginationOutSchema
