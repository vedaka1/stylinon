from abc import ABC, abstractmethod
from uuid import UUID

from src.application.products.filters import ProductFilters
from src.domain.products.entities import Category, Product


class ProductRepositoryInterface(ABC):

    @abstractmethod
    async def create(self, product: Product) -> None: ...

    # @abstractmethod
    # async def create_many(self, products: list[Product]) -> None: ...

    @abstractmethod
    async def delete(self, product_id: UUID) -> None: ...

    @abstractmethod
    async def update(self, product: Product) -> None: ...

    @abstractmethod
    async def get_by_id(self, product_id: UUID) -> Product | None: ...

    @abstractmethod
    async def get_many(
        self,
        filters: ProductFilters | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> list[Product]: ...

    @abstractmethod
    async def count(
        self,
        filters: ProductFilters | None = None,
    ) -> int: ...

    @abstractmethod
    async def get_many_by_ids(
        self,
        product_ids: set[UUID],
    ) -> tuple[list[Product], set[UUID]]:
        """
        ### Args:
        `product_ids` - set of product ids

        ### Returns:
        `tuple[list[Product], set[UUID]]` - a tuple with a list of products and set of missing product ids
        """
        ...


class CategoryRepositoryInterface(ABC):

    @abstractmethod
    async def create(self, category: Category) -> None: ...

    @abstractmethod
    async def delete(self, category_name: str) -> None: ...

    @abstractmethod
    async def update(self, category: Category) -> None: ...

    @abstractmethod
    async def get_by_name(self, category_name: str) -> Category | None: ...

    @abstractmethod
    async def get_many(self) -> list[Category]: ...

    @abstractmethod
    async def count(self) -> int: ...
