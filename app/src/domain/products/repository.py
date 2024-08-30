from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.products.entities import Product


class ProductRepositoryInterface(ABC):

    @abstractmethod
    async def create(self, product: Product) -> None: ...

    @abstractmethod
    async def delete(self, product_id: UUID) -> None: ...

    @abstractmethod
    async def update(self, product: Product) -> None: ...

    @abstractmethod
    async def get_by_id(self, product_id: UUID) -> Product | None: ...

    @abstractmethod
    async def get_by_category(
        self,
        category: str,
        offset: int = 0,
        limit: int = 100,
    ) -> list[Product]: ...

    @abstractmethod
    async def get_many(
        self,
        search: str | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> list[Product]: ...

    @abstractmethod
    async def count(self, search: str | None = None) -> int: ...
