from datetime import date
from uuid import UUID

from src.domain.exceptions.order import OrderNotFoundException
from src.domain.orders.entities import Order, OrderItem, OrderStatus
from src.domain.orders.repository import OrderRepositoryInterface
from src.domain.orders.service import OrderServiceInterface


class OrderService(OrderServiceInterface):
    __slots__ = "order_repository"

    def __init__(self, order_repository: OrderRepositoryInterface) -> None:
        self.order_repository = order_repository

    async def create(self, order: Order) -> None:
        return await self.order_repository.create(order)

    async def delete(self, order_id: UUID) -> None:
        return await self.order_repository.delete(order_id)

    async def update(
        self,
        order_id: UUID,
        shipping_address: str | None,
        tracking_number: str | None,
        status: OrderStatus | None,
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

    async def get_by_user_email(self, user_email: str) -> list[Order]:
        return await self.order_repository.get_by_user_email(user_email)

    async def get_many(
        self,
        date_from: date | None = None,
        date_to: date | None = None,
        status: OrderStatus | None = None,
    ) -> list[Order]:
        return await self.order_repository.get_many(
            date_from=date_from, date_to=date_to, status=status
        )

    # @abstractmethod
    # async def count(
    #     self,
    #     date_from: str | None = None,
    #     date_to: str | None = None,
    #     status: OrderStatus | None = None,
    # ) -> int: ...
