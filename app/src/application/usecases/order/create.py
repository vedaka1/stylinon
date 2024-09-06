from dataclasses import dataclass
from uuid import uuid4

from src.application.common.transaction import TransactionManagerInterface
from src.application.contracts.commands.order import CreateOrderCommand
from src.domain.orders.entities import Order, OrderItem
from src.domain.orders.service import OrderItemServiceInterface, OrderServiceInterface
from src.domain.products.service import ProductServiceInterface

# from src.infrastructure.acquiring.interface import AcquiringGatewayInterface


@dataclass
class CreateOrderUseCase:
    order_service: OrderServiceInterface
    order_item_service: OrderItemServiceInterface
    products_service: ProductServiceInterface
    # acquiring_gateway: AcquiringGatewayInterface
    transaction_manager: TransactionManagerInterface

    async def execute(self, command: CreateOrderCommand) -> None:

        order = Order.create(
            user_email=command.user_email,
            transaction_id=uuid4(),
            shipping_address=command.shipping_address,
        )
        order_items = [
            OrderItem.create(
                order_id=order.id,
                product_id=item.id,
                quantity=item.quantity,
            )
            for item in command.items
        ]
        await self.order_service.create(order=order)
        await self.order_item_service.create_many(order_items)
        await self.transaction_manager.commit()
        return None
