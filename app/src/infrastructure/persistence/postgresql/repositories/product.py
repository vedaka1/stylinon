from uuid import UUID

from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.products.entities import Product
from src.domain.products.repository import ProductRepositoryInterface
from src.infrastructure.persistence.postgresql.models.product import (
    ProductModel,
    map_to_product,
)


class SqlalchemyProductRepository(ProductRepositoryInterface):
    __slots__ = ["session"]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, product: Product) -> None:
        query = insert(ProductModel).values(
            id=product.id,
            name=product.name,
            category=product.category,
            description=product.description,
            price=product.price,
            units_of_measurement=product.units_of_measurement,
        )
        await self.session.execute(query)
        return None

    async def update(self, product: Product) -> None:
        query = (
            update(ProductModel)
            .where(ProductModel.id == product.id)
            .values(
                name=product.name,
                category=product.category,
                description=product.description,
                price=product.price,
                units_of_measurement=product.units_of_measurement,
            )
        )
        await self.session.execute(query)
        return None

    async def delete(self, product_id: UUID) -> None:
        query = delete(ProductModel).where(ProductModel.id == product_id)
        await self.session.execute(query)
        return None

    async def get_by_id(self, product_id: UUID) -> Product | None:
        query = select(ProductModel).where(ProductModel.id == product_id)
        cursor = await self.session.execute(query)
        entity = cursor.scalar_one_or_none()
        return map_to_product(entity) if entity else None

    async def get_by_category(
        self,
        category: str,
        offset: int = 0,
        limit: int = 100,
    ) -> list[Product]:
        query = (
            select(ProductModel)
            .where(ProductModel.category.ilike(f"%{category}%"))
            .limit(limit)
            .offset(offset)
        )
        cursor = await self.session.execute(query)
        entities = cursor.scalars().all()
        return [map_to_product(entity) for entity in entities]

    async def get_many(
        self,
        search: str | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> list[Product]:
        query = select(ProductModel)
        if search:
            query = query.where(
                ProductModel.name.ilike(f"%{search}%")
                | ProductModel.category.ilike(f"%{search}%")
                | ProductModel.description.ilike(f"%{search}%"),
            )
        query = query.limit(limit).offset(offset)
        cursor = await self.session.execute(query)
        entities = cursor.scalars().all()
        return [map_to_product(entity) for entity in entities]

    async def count(self, search: str | None = None) -> int:
        query = select(func.count()).select_from(ProductModel)
        if search:
            query = query.where(ProductModel.name.ilike(f"%{search}%"))
        cursor = await self.session.execute(query)
        count = cursor.scalar_one_or_none()
        return count if count else 0
