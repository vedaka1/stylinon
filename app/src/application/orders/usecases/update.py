import logging
from dataclasses import dataclass

from src.application.acquiring.dto import AcquiringWebhookType
from src.application.acquiring.exceptions import IncorrectAcqioringWebhookTypeException
from src.application.common.interfaces.acquiring import AcquiringServiceInterface
from src.application.common.interfaces.transaction import TransactionManagerInterface
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
        logger.info("Order updated", extra={"order_id": command.order_id})
        return None


@dataclass
class UpdateOrderByWebhookUseCase:
    order_service: OrderServiceInterface
    acquiring_service: AcquiringServiceInterface
    transaction_manager: TransactionManagerInterface

    async def execute(self, token: str) -> None:
        webhook_data = self.acquiring_service.handle_webhook(token=token)
        if (
            webhook_data.get("webhookType")
            != AcquiringWebhookType.acquiringInternetPayment
        ):
            logger.error(
                "Incorrect acquiring webhook type",
                extra={"data": webhook_data},
            )
            raise IncorrectAcqioringWebhookTypeException
        order = await self.order_service.get_by_operation_id(
            operation_id=webhook_data["operationId"],
        )
        await self.order_service.update(
            order_id=order.id,
            status=OrderStatus.APPROVED,
        )
        await self.transaction_manager.commit()
        logger.info("Order updated by webhook", extra={"order_id": order.id})
        return None
