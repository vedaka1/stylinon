from dataclasses import dataclass
from uuid import UUID

from src.application.contracts.commands.order import GetManyOrdersCommand
from src.domain.orders.entities import Order
from src.domain.orders.service import OrderServiceInterface


@dataclass
class GetManyOrdersUseCase:

    order_service: OrderServiceInterface

    async def execute(self, command: GetManyOrdersCommand) -> list[Order]:
        return await self.order_service.get_many(
            date_from=command.date_from, date_to=command.date_to, status=command.status
        )


@dataclass
class GetOrderUseCase:

    order_service: OrderServiceInterface

    async def execute(self, order_id: UUID) -> Order:
        order = await self.order_service.get_by_id_with_products(order_id)
        return order
