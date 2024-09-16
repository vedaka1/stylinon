from datetime import date
from uuid import UUID

from src.application.common.jwt_processor import JwtTokenProcessorInterface
from src.domain.exceptions.order import OrderNotFoundException
from src.domain.orders.entities import Order, OrderItem, OrderStatus
from src.domain.orders.repository import (
    OrderItemRepositoryInterface,
    OrderRepositoryInterface,
)
from src.domain.orders.service import OrderItemServiceInterface, OrderServiceInterface


class OrderService(OrderServiceInterface):
    __slots__ = (
        "order_repository",
        "jwt_processor",
    )

    def __init__(
        self,
        order_repository: OrderRepositoryInterface,
        jwt_processor: JwtTokenProcessorInterface,
    ) -> None:
        self.order_repository = order_repository
        self.jwt_processor = jwt_processor

    async def create(self, order: Order) -> None:
        return await self.order_repository.create(order)

    async def delete(self, order_id: UUID) -> None:
        return await self.order_repository.delete(order_id)

    async def update(
        self,
        order_id: UUID,
        shipping_address: str | None = None,
        tracking_number: str | None = None,
        status: OrderStatus | None = None,
    ) -> None:
        order = await self.get_by_id(order_id)
        if shipping_address:
            order.shipping_address = shipping_address
        if tracking_number:
            order.tracking_number = tracking_number
        if status:
            order.status = status
        return await self.order_repository.update(order)

    async def get_by_id(self, order_id: UUID) -> Order:
        order = await self.order_repository.get_by_id(order_id)
        if not order:
            raise OrderNotFoundException
        return order

    async def get_by_id_with_products(self, order_id: UUID) -> Order:
        order = await self.order_repository.get_by_id_with_products(order_id)
        if not order:
            raise OrderNotFoundException
        return order

    async def get_by_operation_id(self, operation_id: UUID) -> Order:
        order = await self.order_repository.get_by_operation_id(
            operation_id=operation_id,
        )
        if not order:
            raise OrderNotFoundException
        return order

    async def get_by_user_email(self, user_email: str) -> list[Order]:
        return await self.order_repository.get_by_user_email(user_email)

    async def get_many(
        self,
        date_from: date | None = None,
        date_to: date | None = None,
        status: OrderStatus | None = None,
    ) -> list[Order]:
        return await self.order_repository.get_many(
            date_from=date_from,
            date_to=date_to,
            status=status,
        )

    # @abstractmethod
    # async def count(
    #     self,
    #     date_from: str | None = None,
    #     date_to: str | None = None,
    #     status: OrderStatus | None = None,
    # ) -> int: ...


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
