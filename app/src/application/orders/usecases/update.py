import logging
from dataclasses import dataclass

from src.application.acquiring.dto import AcquiringWebhookType
from src.application.acquiring.exceptions import IncorrectAcqioringWebhookTypeException
from src.application.common.acquiring import AcquiringServiceInterface
from src.application.common.transaction import TransactionManagerInterface
from src.application.orders.commands import UpdateOrderCommand
from src.domain.orders.entities import OrderStatus
from src.domain.orders.service import OrderServiceInterface

logger = logging.getLogger()


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


@dataclass
class UpdateOrderByWebhookUseCase:
    order_service: OrderServiceInterface
    acquiring_service: AcquiringServiceInterface
    transaction_manager: TransactionManagerInterface

    async def execute(self, token: str) -> None:
        data = self.acquiring_service.handle_webhook(token=token)
        if data.get("webhookType") != AcquiringWebhookType.acquiringInternetPayment:
            raise IncorrectAcqioringWebhookTypeException
        order = await self.order_service.get_by_operation_id(
            operation_id=data["operationId"],
        )
        await self.order_service.update(
            order_id=order.id,
            status=OrderStatus.APPROVED,
        )
        await self.transaction_manager.commit()
        return None
