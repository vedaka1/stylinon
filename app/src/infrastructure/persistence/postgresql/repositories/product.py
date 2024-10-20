from uuid import UUID

from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.application.products.filters import ProductFilters
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
            sku=product.sku,
            category=product.category,
            description=product.description,
            collection=product.collection,
            weight=product.weight,
            size=product.size,
            retail_price=product.retail_price.value,
            wholesale_price=(
                product.wholesale_price.value if product.wholesale_price else None
            ),
            d1_delivery_price=(
                product.d1_delivery_price.value if product.d1_delivery_price else None
            ),
            d1_self_pickup_price=(
                product.d1_self_pickup_price.value
                if product.d1_self_pickup_price
                else None
            ),
            units_of_measurement=product.units_of_measurement,
            image=product.image,
            status=product.status,
            is_available=product.is_available,
        )

        await self.session.execute(query)

        return None

    async def update(self, product: Product) -> None:
        query = (
            update(ProductModel)
            .where(ProductModel.id == product.id)
            .values(
                name=product.name,
                sku=product.sku,
                category=product.category,
                description=product.description,
                collection=product.collection,
                weight=product.weight,
                size=product.size,
                retail_price=product.retail_price.value,
                wholesale_price=(
                    product.wholesale_price.value if product.wholesale_price else None
                ),
                d1_delivery_price=(
                    product.d1_delivery_price.value
                    if product.d1_delivery_price
                    else None
                ),
                d1_self_pickup_price=(
                    product.d1_self_pickup_price.value
                    if product.d1_self_pickup_price
                    else None
                ),
                units_of_measurement=product.units_of_measurement,
                image=product.image,
                status=product.status,
                is_available=product.is_available,
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

    async def get_many(
        self,
        filters: ProductFilters | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> list[Product]:
        query = select(ProductModel)

        if filters:
            if filters.name:
                query = query.where(ProductModel.name.ilike(f"%{filters.name}%"))
            if filters.category:
                query = query.where(
                    ProductModel.category.ilike(f"%{filters.category}%"),
                )
            if filters.description:
                query = query.where(
                    ProductModel.description.ilike(f"%{filters.description}%"),
                )
            if filters.price_from:
                query = query.where(
                    ProductModel.retail_price >= filters.price_from,
                )
            if filters.price_to:
                query = query.where(
                    ProductModel.retail_price <= filters.price_to,
                )
            if filters.units_of_measurement:
                query = query.where(
                    ProductModel.units_of_measurement == filters.units_of_measurement,
                )
            if filters.is_available:
                query = query.where(
                    ProductModel.is_available == filters.is_available,
                )

        query = query.limit(limit).offset(offset)

        cursor = await self.session.execute(query)

        entities = cursor.scalars().all()

        return [map_to_product(entity) for entity in entities]

    async def count(
        self,
        filters: ProductFilters | None = None,
    ) -> int:
        query = select(func.count()).select_from(ProductModel)

        if filters:
            if filters.name:
                query = query.where(ProductModel.name.ilike(f"%{filters.name}%"))
            if filters.category:
                query = query.where(
                    ProductModel.category.ilike(f"%{filters.category}%"),
                )
            if filters.description:
                query = query.where(
                    ProductModel.description.ilike(f"%{filters.description}%"),
                )
            if filters.price_from:
                query = query.where(
                    ProductModel.retail_price >= filters.price_from,
                )
            if filters.price_to:
                query = query.where(
                    ProductModel.retail_price <= filters.price_to,
                )
            if filters.units_of_measurement:
                query = query.where(
                    ProductModel.units_of_measurement == filters.units_of_measurement,
                )
            if filters.is_available:
                query = query.where(
                    ProductModel.is_available == filters.is_available,
                )

        cursor = await self.session.execute(query)

        count = cursor.scalar_one_or_none()

        return count if count else 0

    async def get_many_by_ids(
        self,
        product_ids: set[UUID],
    ) -> tuple[list[Product], set[UUID]]:
        """Returns a tuple with a list of existing products and a set of missing products, if any"""
        query = select(ProductModel).filter(ProductModel.id.in_(product_ids))

        cursor = await self.session.execute(query)

        entities = cursor.scalars().all()

        existing_entities = set()

        for entity in entities:
            existing_entities.add(entity.id)

        missing_entities = product_ids - existing_entities

        return (
            [map_to_product(entity) for entity in entities],
            missing_entities,
        )
