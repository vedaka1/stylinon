import logging
from dataclasses import dataclass
from datetime import datetime

from src.application.acquiring.dto import AcquiringWebhookType
from src.application.acquiring.exceptions import IncorrectAcqioringWebhookTypeException
from src.application.common.email.utils import get_new_order_template
from src.application.common.interfaces.acquiring import AcquiringServiceInterface
from src.application.common.interfaces.smtp import SyncSMTPServerInterface
from src.application.common.interfaces.transaction import TransactionManagerInterface
from src.application.orders.commands import UpdateOrderCommand
from src.domain.orders.entities import OrderStatus
from src.domain.orders.exceptions import OrderNotFoundException
from src.domain.orders.repository import OrderRepositoryInterface

logger = logging.getLogger()


@dataclass
class UpdateOrderUseCase:

    order_repository: OrderRepositoryInterface
    transaction_manager: TransactionManagerInterface

    async def execute(self, command: UpdateOrderCommand) -> None:
        order = await self.order_repository.get_by_id(command.order_id)

        if not order:
            raise OrderNotFoundException

        if command.shipping_address:
            order.shipping_address = command.shipping_address
        if command.tracking_number:
            order.tracking_number = command.tracking_number
        if command.status:
            order.status = command.status

        order.updated_at = datetime.now()

        await self.order_repository.update(order=order)

        await self.transaction_manager.commit()

        logger.info("Order updated", extra={"order_id": command.order_id})

        return None


@dataclass
class UpdateOrderByWebhookUseCase:

    order_repository: OrderRepositoryInterface
    acquiring_service: AcquiringServiceInterface
    transaction_manager: TransactionManagerInterface
    smtp_server: SyncSMTPServerInterface

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

        order = await self.order_repository.get_by_operation_id(
            operation_id=webhook_data["operationId"],
        )

        if not order:
            raise OrderNotFoundException

        order.status = OrderStatus.APPROVED

        await self.order_repository.update(order=order)

        email_content = get_new_order_template(order)

        message = self.smtp_server.create_message(
            content=email_content,
            to_address="vedaka13@yandex.com",
        )

        await self.smtp_server.send_email(message=message)

        logger.info("Order updated by webhook", extra={"order_id": order.id})

        await self.transaction_manager.commit()

        return None
