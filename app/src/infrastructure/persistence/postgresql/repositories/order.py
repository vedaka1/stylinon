from uuid import UUID

from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from src.domain.orders.entities import Order, OrderItem, OrderStatus
from src.domain.orders.repository import (
    OrderItemRepositoryInterface,
    OrderRepositoryInterface,
)
from src.infrastructure.persistence.postgresql.models.order import (
    OrderItemModel,
    OrderModel,
    map_to_order,
    map_to_order_item,
)


class SqlalchemyOrderRepository(OrderRepositoryInterface):
    __slots__ = ["session"]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, order: Order) -> None:
        query = insert(OrderModel).values(
            id=order.id,
            user_email=order.user_email,
            created_at=order.created_at,
            updated_at=order.updated_at,
            shipping_address=order.shipping_address,
            transaction_id=order.transaction_id,
            tracking_number=order.tracking_number,
            status=order.status,
        )
        await self.session.execute(query)
        return None

    async def delete(self, order_id: UUID) -> None:
        query = delete(OrderModel).where(OrderModel.id == order_id)
        await self.session.execute(query)
        return None

    async def update(self, order: Order) -> None:
        query = (
            update(OrderModel)
            .where(OrderModel.id == order.id)
            .values(status=order.status)
        )
        await self.session.execute(query)
        return None

    async def get_by_id(self, order_id: UUID) -> Order | None:
        query = select(OrderModel).where(OrderModel.id == order_id)
        cursor = await self.session.execute(query)
        entity = cursor.scalar_one_or_none()
        return map_to_order(entity) if entity else None

    async def get_by_id_with_products(self, order_id: UUID) -> Order | None:
        query = (
            select(OrderModel)
            .options(
                selectinload(OrderModel.order_items).joinedload(OrderItemModel.product)
            )
            .where(OrderModel.id == order_id)
        )
        cursor = await self.session.execute(query)
        entity = cursor.scalar_one_or_none()
        return map_to_order(entity, with_products=True) if entity else None

    async def get_by_user_email(self, user_email: str) -> list[Order]:
        query = select(OrderModel).where(OrderModel.user_email == user_email)
        cursor = await self.session.execute(query)
        entities = cursor.scalars().all()
        return [map_to_order(entity) for entity in entities]

    async def get_many(
        self,
        date_from: str | None = None,
        date_to: str | None = None,
        status: OrderStatus | None = None,
    ) -> list[Order]:
        query = select(OrderModel)
        if date_from:
            query = query.where(OrderModel.created_at >= date_from)
        elif date_to:
            query = query.where(OrderModel.created_at <= date_to)
        elif status:
            query = query.where(OrderModel.status == status)

        cursor = await self.session.execute(query)
        entities = cursor.scalars().all()
        return [map_to_order(entity) for entity in entities]

    # async def count(
    #     self,
    #     date_from: str | None = None,
    #     date_to: str | None = None,
    #     status: OrderStatus | None = None,
    # ) -> int:
    #     query = select(func.count()).select_from(OrderModel)
    #     if date_from:
    #         query = query.where(OrderModel.created_at >= date_from)
    #     elif date_to:
    #         query = query.where(OrderModel.created_at <= date_to)
    #     elif status:
    #         query = query.where(OrderModel.status == status)

    #     cursor = await self.session.execute(query)
    #     count = cursor.scalar_one_or_none()
    #     return count if count else 0


class SqlalchemyOrderItemRepository(OrderItemRepositoryInterface):
    __slots__ = ["session"]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, order_item: OrderItem) -> None:
        query = insert(OrderItemModel).values(
            order_id=order_item.order_id,
            product_id=order_item.product_id,
            quantity=order_item.quantity,
        )
        await self.session.execute(query)
        return None

    async def delete(self, order_id: UUID, product_id: UUID) -> None:
        query = delete(OrderItemModel).where(
            (OrderItemModel.order_id == order_id)
            & (OrderItemModel.product_id == product_id)
        )
        await self.session.execute(query)
        return None

    async def update(self, order_item: OrderItem) -> None:
        query = (
            update(OrderItemModel)
            .where(
                (OrderItemModel.order_id == order_item.order_id)
                & (OrderItemModel.product_id == order_item.product_id)
            )
            .values(
                product_id=order_item.product_id,
                quantity=order_item.quantity,
            )
        )
        await self.session.execute(query)
        return None

    async def get_by_order_id(self, order_id: UUID) -> list[OrderItem]:
        query = select(OrderItemModel).where(OrderItemModel.order_id == order_id)
        cursor = await self.session.execute(query)
        entities = cursor.scalars().all()
        return [map_to_order_item(entity) for entity in entities]
