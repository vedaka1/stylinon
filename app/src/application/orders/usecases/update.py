import logging
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.application.acquiring.enums import AcquiringWebhookType
from src.application.acquiring.exceptions import IncorrectAcqioringWebhookTypeException
from src.application.acquiring.interface import AcquiringGatewayInterface
from src.application.common.email.types import SenderName
from src.application.common.email.utils import get_new_order_template
from src.application.common.interfaces.jwt_processor import JWTProcessorInterface
from src.application.common.interfaces.smtp import SyncSMTPServerInterface
from src.application.common.interfaces.transaction import ICommiter
from src.application.orders.commands import UpdateOrderCommand
from src.domain.orders.entities import OrderStatus
from src.domain.orders.exceptions import OrderNotFoundException
from src.domain.orders.repository import OrderRepositoryInterface

logger = logging.getLogger()


@dataclass
class UpdateOrderUseCase:
    order_repository: OrderRepositoryInterface
    commiter: ICommiter

    async def execute(self, command: UpdateOrderCommand, order_id: UUID) -> None:
        order = await self.order_repository.get_by_id(order_id)
        if not order:
            raise OrderNotFoundException

        for key, value in command.__dict__.items():
            if value:
                setattr(order, key, value)

        order.updated_at = datetime.now()

        await self.order_repository.update(order=order)
        await self.commiter.commit()

        logger.info('Order updated', extra={'order_id': order_id})
        return None


@dataclass
class UpdateOrderByWebhookUseCase:
    order_repository: OrderRepositoryInterface
    acquiring_gateway: AcquiringGatewayInterface
    smtp_server: SyncSMTPServerInterface
    jwt_processor: JWTProcessorInterface
    sender_name: SenderName
    commiter: ICommiter

    async def execute(self, token: str) -> None:
        webhook_data = self.jwt_processor.validate_acquiring_token(token=token)
        if webhook_data.get('webhookType') != AcquiringWebhookType.acquiringInternetPayment:
            logger.error('Incorrect acquiring webhook type', extra={'data': webhook_data})
            raise IncorrectAcqioringWebhookTypeException

        order = await self.order_repository.get_by_operation_id(operation_id=webhook_data['operationId'])
        if not order:
            raise OrderNotFoundException

        order.status = OrderStatus.APPROVED
        await self.order_repository.update(order=order)

        email_content = get_new_order_template(order)
        message = self.smtp_server.create_message(
            content=email_content,
            sender_name=self.sender_name,
            to_address='vedaka13@yandex.com',
            subject='Новый заказ',
        )
        await self.smtp_server.send_email(message=message)
        await self.commiter.commit()

        logger.info('Order updated by webhook', extra={'order_id': order.id})
        return None
