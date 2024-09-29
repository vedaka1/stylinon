from dataclasses import dataclass
from uuid import UUID

from src.application.orders.commands import GetManyOrdersCommand
from src.application.orders.responses import OrderItemOut, OrderOut
from src.domain.orders.entities import Order
from src.domain.orders.service import OrderServiceInterface


@dataclass
class GetManyOrdersUseCase:
    order_service: OrderServiceInterface

    async def execute(self, command: GetManyOrdersCommand) -> list[OrderOut]:
        orders = await self.order_service.get_many(
            date_from=command.date_from,
            date_to=command.date_to,
            status=command.status,
        )
        return [
            OrderOut(
                id=order.id,
                user_email=order.user_email,
                created_at=order.created_at,
                updated_at=order.updated_at,
                shipping_address=order.shipping_address,
                operation_id=order.operation_id,
                tracking_number=order.tracking_number,
                total_price=order.total_price,
                status=order.status,
                items=[
                    OrderItemOut(
                        name=order_item.product.name,
                        category=order_item.product.category,
                        description=order_item.product.description,
                        price=order_item.product.price.value,
                        quantity=order_item.quantity,
                        units_of_measurement=order_item.product.units_of_measurement,
                    )
                    for order_item in order.items
                    if order_item.product
                ],
            )
            for order in orders
        ]


@dataclass
class GetOrderUseCase:

    order_service: OrderServiceInterface

    async def execute(self, order_id: UUID) -> Order:
        order = await self.order_service.get_by_id_with_products(order_id)
        return order
