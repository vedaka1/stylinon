# from uuid import UUID

# from sqlalchemy import delete, func, insert, select, update
# from sqlalchemy.ext.asyncio import AsyncSession
# from src.domain.products.entities import Sku
# from src.domain.products.repository import SkuRepositoryInterface
# from src.infrastructure.persistence.postgresql.models.product import (
#     SkuModel,
#     map_to_sku,
# )


# class SqlalchemySkuRepository(SkuRepositoryInterface):
#     __slots__ = ["session"]

#     def __init__(self, session: AsyncSession) -> None:
#         self.session = session

#     async def create(self, sku: Sku) -> None:
#         query = insert(SkuModel).values(
#             id=sku.id,
#             code=sku.code,
#             retail_price=sku.retail_price.value,
#             wholesale_delivery_price=sku.wholesale_delivery_price.value,
#             d2_delivery_price=sku.d2_delivery_price.value,
#             d2_self_pickup_price=sku.d2_self_pickup_price.value,
#             d1_delivery_price=sku.d1_delivery_price.value,
#             d1_self_pickup_price=sku.d1_self_pickup_price.value,
#             status=sku.status,
#         )

#         await self.session.execute(query)

#         return None

#     async def update(self, sku: Sku) -> None:
#         query = (
#             update(SkuModel)
#             .where(SkuModel.id == sku.id)
#             .values(
#                 code=sku.code,
#                 retail_price=sku.retail_price.value,
#                 wholesale_delivery_price=sku.wholesale_delivery_price.value,
#                 d2_delivery_price=sku.d2_delivery_price.value,
#                 d2_self_pickup_price=sku.d2_self_pickup_price.value,
#                 d1_delivery_price=sku.d1_delivery_price.value,
#                 d1_self_pickup_price=sku.d1_self_pickup_price.value,
#                 status=sku.status,
#             )
#         )

#         await self.session.execute(query)

#         return None

#     async def delete(self, sku_id: UUID) -> None:
#         query = delete(SkuModel).where(SkuModel.id == sku_id)

#         await self.session.execute(query)

#         return None

#     async def get_by_id(self, sku_id: UUID) -> Sku | None:
#         query = select(SkuModel).where(SkuModel.id == sku_id)

#         cursor = await self.session.execute(query)

#         entity = cursor.scalar_one_or_none()

#         return map_to_sku(entity) if entity else None

#     async def get_many_by_ids(self, sku_ids: set[UUID]) -> tuple[list[Sku], set[UUID]]:
#         query = select(SkuModel).where(SkuModel.id.in_(sku_ids))

#         cursor = await self.session.execute(query)

#         entities = cursor.scalars().all()

#         missing_sku: set[UUID] = set()
#         skus: list[Sku] = []

#         for entity in entities:
#             if entity not in sku_ids:
#                 missing_sku.add(entity.id)
#             else:
#                 skus.append(map_to_sku(entity))

#         return skus, missing_sku

#     async def count(self) -> int:
#         query = select(func.count()).select_from(SkuModel)

#         cursor = await self.session.execute(query)

#         count = cursor.scalar_one_or_none()

#         return count if count else 0
