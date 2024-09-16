from abc import ABC, abstractmethod
from datetime import date
from uuid import UUID

from src.domain.orders.entities import Order, OrderItem, OrderStatus


class OrderRepositoryInterface(ABC):

    @abstractmethod
    async def create(self, order: Order) -> None: ...

    @abstractmethod
    async def delete(self, order_id: UUID) -> None: ...

    @abstractmethod
    async def update(self, order: Order) -> None: ...

    @abstractmethod
    async def get_by_id(self, order_id: UUID) -> Order | None: ...

    @abstractmethod
    async def get_by_id_with_products(self, order_id: UUID) -> Order | None: ...

    @abstractmethod
    async def get_by_operation_id(self, operation_id: UUID) -> Order | None: ...

    @abstractmethod
    async def get_by_user_email(self, user_email: str) -> list[Order]: ...

    @abstractmethod
    async def get_many(
        self,
        date_from: date | None = None,
        date_to: date | None = None,
        status: OrderStatus | None = None,
    ) -> list[Order]: ...

    # @abstractmethod
    # async def count(
    #     self,
    #     date_from: str | None = None,
    #     date_to: str | None = None,
    #     status: OrderStatus | None = None,
    # ) -> int: ...


class OrderItemRepositoryInterface(ABC):

    @abstractmethod
    async def create(self, order_item: OrderItem) -> None: ...

    @abstractmethod
    async def create_many(self, order_items: list[OrderItem]) -> None: ...

    @abstractmethod
    async def update(self, order_item: OrderItem) -> None: ...

    @abstractmethod
    async def delete(self, order_id: UUID, product_id: UUID) -> None: ...

    @abstractmethod
    async def get_by_order_id(self, order_id: UUID) -> list[OrderItem]: ...
