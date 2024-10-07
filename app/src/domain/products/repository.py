from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.products.entities import Product, UnitsOfMesaurement


class ProductRepositoryInterface(ABC):

    @abstractmethod
    async def create(self, product: Product) -> None: ...

    @abstractmethod
    async def create_many(self, products: list[Product]) -> None: ...

    @abstractmethod
    async def delete(self, product_id: UUID) -> None: ...

    @abstractmethod
    async def update(self, product: Product) -> None: ...

    @abstractmethod
    async def get_by_id(self, product_id: UUID) -> Product | None: ...

    @abstractmethod
    async def get_many(
        self,
        name: str | None = None,
        category: str | None = None,
        description: str | None = None,
        price_from: int | None = None,
        price_to: int | None = None,
        units_of_measurement: UnitsOfMesaurement | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> list[Product]: ...

    @abstractmethod
    async def count(
        self,
        name: str | None = None,
        category: str | None = None,
        description: str | None = None,
        price_from: int | None = None,
        price_to: int | None = None,
        units_of_measurement: UnitsOfMesaurement | None = None,
    ) -> int: ...

    @abstractmethod
    async def get_many_by_ids(
        self,
        product_ids: set[UUID],
    ) -> tuple[list[Product], set[UUID]]: ...
