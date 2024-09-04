from dataclasses import dataclass

from src.application.common.transaction import TransactionManagerInterface
from src.application.contracts.commands.order import UpdateOrderCommand
from src.domain.orders.service import OrderServiceInterface


@dataclass
class UpdateOrderUseCase:
    order_service: OrderServiceInterface
    transaction_manager: TransactionManagerInterface

    async def execute(self, command: UpdateOrderCommand) -> None:
        await self.order_service.update(
            order_id=command.order_id,
            shipping_address=command.shipping_address,
            tracking_number=command.tracking_number,
            status=command.status,
        )
        await self.transaction_manager.commit()
        return None
