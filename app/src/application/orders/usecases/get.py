from dataclasses import dataclass
from uuid import UUID

from src.application.orders.commands import GetManyOrdersCommand
from src.application.orders.dto import OrderItemOut, OrderOut
from src.domain.orders.exceptions import OrderNotFoundException
from src.domain.orders.repository import OrderRepositoryInterface


@dataclass
class GetManyOrdersUseCase:

    order_repository: OrderRepositoryInterface

    async def execute(self, command: GetManyOrdersCommand) -> list[OrderOut]:
        orders = await self.order_repository.get_many(
            date_from=command.date_from,
            date_to=command.date_to,
            status=command.status,
        )

        return [
            OrderOut(
                id=order.id,
                customer_email=order.customer_email,
                created_at=order.created_at,
                updated_at=order.updated_at,
                shipping_address=order.shipping_address,
                operation_id=order.operation_id,
                tracking_number=order.tracking_number,
                total_price=order.total_price,
                status=order.status,
                items=[
                    OrderItemOut(
                        product_id=order_item.product.id,
                        name=order_item.product.name,
                        category=order_item.product.category,
                        description=order_item.product.description,
                        price=order_item.product.price.value,
                        units_of_measurement=order_item.product.units_of_measurement,
                        quantity=order_item.quantity,
                        photo_url=order_item.product.photo_url,
                    )
                    for order_item in order.items
                    if order_item.product
                ],
            )
            for order in orders
        ]


@dataclass
class GetOrderUseCase:

    order_repository: OrderRepositoryInterface

    async def execute(self, order_id: UUID) -> OrderOut:
        order = await self.order_repository.get_by_id_with_products(order_id)

        if not order:
            raise OrderNotFoundException

        return OrderOut(
            id=order.id,
            customer_email=order.customer_email,
            created_at=order.created_at,
            updated_at=order.updated_at,
            shipping_address=order.shipping_address,
            operation_id=order.operation_id,
            tracking_number=order.tracking_number,
            total_price=order.total_price,
            status=order.status,
            items=[
                OrderItemOut(
                    product_id=order_item.product.id,
                    name=order_item.product.name,
                    category=order_item.product.category,
                    description=order_item.product.description,
                    price=order_item.product.price.value,
                    units_of_measurement=order_item.product.units_of_measurement,
                    quantity=order_item.quantity,
                    photo_url=order_item.product.photo_url,
                )
                for order_item in order.items
                if order_item.product
            ],
        )
