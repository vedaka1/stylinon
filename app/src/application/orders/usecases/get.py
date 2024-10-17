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
                is_self_pickup=order.is_self_pickup,
                status=order.status,
                items=[
                    OrderItemOut(
                        product_id=order_item.product.id,
                        name=order_item.product.name,
                        category=order_item.product.parent_product.category,
                        description=order_item.product.parent_product.description,
                        units_of_measurement=order_item.product.parent_product.units_of_measurement,
                        quantity=order_item.quantity,
                        product_name=order_item.product.name,
                        sku=order_item.product.sku,
                        bag_weight=order_item.product.bag_weight,
                        pallet_weight=order_item.product.pallet_weight,
                        bags_per_pallet=order_item.product.bags_per_pallet,
                        retail_price=order_item.product.retail_price,
                        wholesale_delivery_price=order_item.product.wholesale_delivery_price,
                        d2_delivery_price=order_item.product.d2_delivery_price,
                        d2_self_pickup_price=order_item.product.d2_self_pickup_price,
                        d1_delivery_price=order_item.product.d1_delivery_price,
                        d1_self_pickup_price=order_item.product.d1_self_pickup_price,
                        status=order_item.product.status,
                        image=order_item.product.image,
                    )
                    for order_item in order.items
                    if order_item.product and order_item.product.parent_product
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
        print(order)
        return OrderOut(
            id=order.id,
            customer_email=order.customer_email,
            created_at=order.created_at,
            updated_at=order.updated_at,
            shipping_address=order.shipping_address,
            operation_id=order.operation_id,
            tracking_number=order.tracking_number,
            total_price=order.total_price,
            is_self_pickup=order.is_self_pickup,
            status=order.status,
            items=[
                OrderItemOut(
                    product_id=order_item.product.id,
                    name=order_item.product.name,
                    category=order_item.product.parent_product.category,
                    description=order_item.product.parent_product.description,
                    units_of_measurement=order_item.product.parent_product.units_of_measurement,
                    quantity=order_item.quantity,
                    product_name=order_item.product.name,
                    sku=order_item.product.sku,
                    bag_weight=order_item.product.bag_weight,
                    pallet_weight=order_item.product.pallet_weight,
                    bags_per_pallet=order_item.product.bags_per_pallet,
                    retail_price=order_item.product.retail_price,
                    wholesale_delivery_price=order_item.product.wholesale_delivery_price,
                    d2_delivery_price=order_item.product.d2_delivery_price,
                    d2_self_pickup_price=order_item.product.d2_self_pickup_price,
                    d1_delivery_price=order_item.product.d1_delivery_price,
                    d1_self_pickup_price=order_item.product.d1_self_pickup_price,
                    status=order_item.product.status,
                    image=order_item.product.image,
                )
                for order_item in order.items
                if order_item.product and order_item.product.parent_product
            ],
        )
