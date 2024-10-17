from uuid import UUID

from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.domain.products.entities import ProductVariant
from src.domain.products.repository import ProductVariantRepositoryInterface
from src.infrastructure.persistence.postgresql.models.product import (
    ProductVariantModel,
    map_to_product_variant,
)


class SqlalchemyProductVariantRepository(ProductVariantRepositoryInterface):
    __slots__ = ["session"]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, product_variant: ProductVariant) -> None:
        query = insert(ProductVariantModel).values(
            id=product_variant.id,
            product_id=product_variant.product_id,
            name=product_variant.name,
            sku=product_variant.sku,
            bag_weight=product_variant.bag_weight,
            pallet_weight=product_variant.pallet_weight,
            bags_per_pallet=product_variant.bags_per_pallet,
            image=product_variant.image,
            retail_price=product_variant.retail_price.value,
            wholesale_delivery_price=product_variant.wholesale_delivery_price.value,
            d2_delivery_price=product_variant.d2_delivery_price.value,
            d2_self_pickup_price=product_variant.d2_self_pickup_price.value,
            d1_delivery_price=product_variant.d1_delivery_price.value,
            d1_self_pickup_price=product_variant.d1_self_pickup_price.value,
            status=product_variant.status,
        )

        await self.session.execute(query)

        return None

    async def delete(self, product_variant_id: UUID) -> None:
        query = delete(ProductVariantModel).where(
            ProductVariantModel.id == product_variant_id,
        )

        await self.session.execute(query)

        return None

    async def get_by_id(self, product_variant_id: UUID) -> ProductVariant | None:
        query = select(ProductVariantModel).where(
            ProductVariantModel.id == product_variant_id,
        )

        cursor = await self.session.execute(query)

        entity = cursor.scalar_one_or_none()

        return map_to_product_variant(entity, with_relations=True) if entity else None

    async def get_many(
        self,
        offset: int = 0,
        limit: int = 100,
    ) -> list[ProductVariant]:
        query = select(ProductVariantModel).options(
            selectinload(ProductVariantModel.parent_product),
        )

        query = query.limit(limit).offset(offset)

        cursor = await self.session.execute(query)

        entities = cursor.scalars().all()

        return [
            map_to_product_variant(entity, with_relations=True) for entity in entities
        ]

    async def get_many_by_ids(
        self,
        product_variant_ids: set[UUID],
    ) -> tuple[list[ProductVariant], set[UUID]]:
        query = select(ProductVariantModel).where(
            ProductVariantModel.id.in_(product_variant_ids),
        )

        cursor = await self.session.execute(query)

        entities = cursor.scalars().all()

        existing_entities = set()

        for entity in entities:
            existing_entities.add(entity.id)

        missing_entities = product_variant_ids - existing_entities

        return (
            [map_to_product_variant(entity) for entity in entities],
            missing_entities,
        )

    async def count(self) -> int:
        query = select(func.count()).select_from(ProductVariantModel)

        cursor = await self.session.execute(query)

        count = cursor.scalar_one_or_none()

        return count if count else 0

    async def update(self, product_variant: ProductVariant) -> None:
        query = (
            update(ProductVariantModel)
            .where(ProductVariantModel.id == product_variant.id)
            .values(
                product_id=product_variant.product_id,
                name=product_variant.name,
                sku=product_variant.sku,
                bag_weight=product_variant.bag_weight,
                pallet_weight=product_variant.pallet_weight,
                bags_per_pallet=product_variant.bags_per_pallet,
                image=product_variant.image,
                retail_price=product_variant.retail_price.value,
                wholesale_delivery_price=product_variant.wholesale_delivery_price.value,
                d2_delivery_price=product_variant.d2_delivery_price.value,
                d2_self_pickup_price=product_variant.d2_self_pickup_price.value,
                d1_delivery_price=product_variant.d1_delivery_price.value,
                d1_self_pickup_price=product_variant.d1_self_pickup_price.value,
                status=product_variant.status,
            )
        )

        await self.session.execute(query)

        return None
