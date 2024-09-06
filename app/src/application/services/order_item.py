from uuid import UUID

from src.domain.orders.entities import OrderItem
from src.domain.orders.repository import OrderItemRepositoryInterface
from src.domain.orders.service import OrderItemServiceInterface


class OrderItemService(OrderItemServiceInterface):
    __slots__ = ("order_item_repository",)

    def __init__(self, order_item_repository: OrderItemRepositoryInterface):
        self.order_item_repository = order_item_repository

    async def create(self, order_item: OrderItem) -> None:
        return await self.order_item_repository.create(order_item=order_item)

    async def create_many(self, order_items: list[OrderItem]) -> None:
        return await self.order_item_repository.create_many(order_items=order_items)

    async def update(self, order_item: OrderItem) -> None:
        return await self.order_item_repository.update(order_item=order_item)

    async def delete(self, order_id: UUID, product_id: UUID) -> None:
        return await self.order_item_repository.delete(
            order_id=order_id,
            product_id=product_id,
        )

    async def get_by_order_id(self, order_id: UUID) -> list[OrderItem]:
        return await self.order_item_repository.get_by_order_id(order_id=order_id)
