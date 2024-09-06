from uuid import UUID

from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.products.entities import Product, UnitsOfMesaurement
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

    async def create_many(self, products: list[Product]) -> None:
        query = insert(ProductModel).values(
            [
                {
                    "id": product.id,
                    "name": product.name,
                    "category": product.category,
                    "description": product.description,
                    "price": product.price,
                    "units_of_measurement": product.units_of_measurement,
                }
                for product in products
            ],
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
        name: str | None = None,
        category: str | None = None,
        description: str | None = None,
        price_from: int | None = None,
        price_to: int | None = None,
        units_of_measurement: UnitsOfMesaurement | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> list[Product]:
        query = select(ProductModel)
        if name:
            query = query.where(ProductModel.name.ilike(f"%{name}%"))
        if category:
            query = query.where(ProductModel.category.ilike(f"%{category}%"))
        if description:
            query = query.where(ProductModel.description.ilike(f"%{description}%"))
        if price_from:
            query = query.where(ProductModel.price >= price_from)
        if price_to:
            query = query.where(ProductModel.price <= price_to)
        if units_of_measurement:
            query = query.where(
                ProductModel.units_of_measurement == units_of_measurement,
            )

        query = query.limit(limit).offset(offset)
        cursor = await self.session.execute(query)
        entities = cursor.scalars().all()
        return [map_to_product(entity) for entity in entities]

    async def count(
        self,
        name: str | None = None,
        category: str | None = None,
        description: str | None = None,
        price_from: int | None = None,
        price_to: int | None = None,
        units_of_measurement: UnitsOfMesaurement | None = None,
    ) -> int:
        query = select(func.count()).select_from(ProductModel)
        if name:
            query = query.where(ProductModel.name.ilike(f"%{name}%"))
        if category:
            query = query.where(ProductModel.category.ilike(f"%{category}%"))
        if description:
            query = query.where(ProductModel.description.ilike(f"%{description}%"))
        if price_from:
            query = query.where(ProductModel.price >= price_from)
        if price_to:
            query = query.where(ProductModel.price <= price_to)
        if units_of_measurement:
            query = query.where(
                ProductModel.units_of_measurement == units_of_measurement,
            )
        cursor = await self.session.execute(query)
        count = cursor.scalar_one_or_none()
        return count if count else 0
