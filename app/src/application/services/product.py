from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.exceptions.products import ProductNotFoundException
from src.domain.products.entities import Product
from src.domain.products.repository import ProductRepositoryInterface
from src.domain.products.service import ProductServiceInterface


class ProductService(ProductServiceInterface):
    __slots__ = ("product_repository",)

    def __init__(self, product_repository: ProductRepositoryInterface) -> None:
        self.product_repository = product_repository

    @abstractmethod
    async def create(self, product: Product) -> None:
        await self.product_repository.create(product)
        return None

    async def delete(self, product_id: UUID) -> None:
        await self.product_repository.delete(product_id)
        return None

    async def update(self, product: Product) -> None:
        await self.get_by_id(product.id)
        await self.product_repository.update(product)
        return None

    async def get_by_id(self, product_id: UUID) -> Product:
        product = await self.product_repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundException
        return product

    async def get_by_category(
        self, offset: int, limit: int, category: str
    ) -> list[Product]:
        products = await self.product_repository.get_by_category(
            category=category, offset=offset, limit=limit
        )
        return products

    async def get_many(
        self, offset: int, limit: int, search: str | None = None
    ) -> list[Product]:
        products = await self.product_repository.get_many(
            search=search, offset=offset, limit=limit
        )
        return products

    async def count(self, search: str | None = None) -> int:
        return await self.product_repository.count(search=search)
