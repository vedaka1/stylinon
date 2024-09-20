from abc import abstractmethod
from uuid import UUID

from src.domain.products.entities import Product, UnitsOfMesaurement
from src.domain.products.exceptions import ProductNotFoundException
from src.domain.products.repository import ProductRepositoryInterface
from src.domain.products.service import ProductServiceInterface


class ProductService(ProductServiceInterface):
    __slots__ = ("product_repository",)

    def __init__(self, product_repository: ProductRepositoryInterface) -> None:
        self.product_repository = product_repository

    async def create(self, product: Product) -> None:
        await self.product_repository.create(product=product)
        return None

    async def create_many(self, products: list[Product]) -> None:
        return await self.product_repository.create_many(products=products)

    async def delete(self, product_id: UUID) -> None:
        await self.product_repository.delete(product_id=product_id)
        return None

    async def update(self, product: Product) -> None:
        await self.get_by_id(product.id)
        await self.product_repository.update(product=product)
        return None

    async def get_by_id(self, product_id: UUID) -> Product:
        product = await self.product_repository.get_by_id(product_id=product_id)
        if not product:
            raise ProductNotFoundException
        return product

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
    ) -> list[Product]:
        products = await self.product_repository.get_many(
            name=name,
            category=category,
            description=description,
            price_from=price_from,
            price_to=price_to,
            units_of_measurement=units_of_measurement,
            offset=offset,
            limit=limit,
        )
        return products

    async def count(
        self,
        name: str | None = None,
        category: str | None = None,
        description: str | None = None,
        price_from: int | None = None,
        price_to: int | None = None,
        units_of_measurement: UnitsOfMesaurement | None = None,
    ) -> int:
        return await self.product_repository.count(
            name=name,
            category=category,
            description=description,
            price_from=price_from,
            price_to=price_to,
            units_of_measurement=units_of_measurement,
        )

    async def get_many_by_ids(
        self,
        product_ids: list[UUID],
    ) -> tuple[list[Product], set[UUID]]:
        return await self.product_repository.get_many_by_ids(product_ids=product_ids)
