from dataclasses import dataclass
from uuid import uuid4

from src.application.common.transaction import TransactionManagerInterface
from src.application.contracts.commands.order import CreateOrderCommand
from src.domain.orders.entities import Order, OrderItem
from src.domain.orders.service import OrderItemServiceInterface, OrderServiceInterface


@dataclass
class CreateOrderUseCase:
    order_service: OrderServiceInterface
    order_item_service: OrderItemServiceInterface

    transaction_manager: TransactionManagerInterface

    async def execute(self, command: CreateOrderCommand) -> None:
        order = Order.create(
            user_email=command.user_email,
            transaction_id=uuid4(),
            shipping_address=command.shipping_address,
        )
        order_items = [
            OrderItem.create(
                order_id=order.id, product_id=item.id, quantity=item.quantity
            )
            for item in command.items
        ]
        await self.order_service.create(order=order)
        for item in order_items:
            await self.order_item_service.create(order_item=item)

        await self.transaction_manager.commit()
        return None
