import logging
from abc import ABC, abstractmethod

from src.application.common.email.utils import (
    get_new_order_template,
    get_reset_password_template,
)
from src.application.common.interfaces.jwt_processor import JWTProcessorInterface
from src.application.common.interfaces.smtp import SyncSMTPServerInterface
from src.domain.orders.entities import Order

logger = logging.getLogger()


class EmailServiceInterface(ABC):

    @abstractmethod
    async def send_email(self, email: str, body: str) -> None: ...

    @abstractmethod
    async def send_recovery_email(self, email: str) -> None: ...

    @abstractmethod
    async def send_new_order_email(self, email: str, order: Order) -> None: ...


class EmailService:
    __slots__ = (
        "jwt_processor",
        "smtp_server",
        "frontend_url",
        "admin_email",
    )

    def __init__(
        self,
        jwt_processor: JWTProcessorInterface,
        smtp_server: SyncSMTPServerInterface,
    ) -> None:
        self.jwt_processor = jwt_processor
        self.smtp_server = smtp_server
        self.frontend_url = "http://localhost/api/v1/reset-password"
        self.admin_email = "vedaka13@yandex.ru"

    async def send_email(self, email: str, body: str, subject: str) -> None:
        message = self.smtp_server.create_message(
            content=body,
            sender_name=email,
            to_address=email,
            subject=subject,
        )
        await self.smtp_server.send_email(message=message)

    async def send_recovery_email(self, email: str) -> None:
        reset_token = self.jwt_processor.create_reset_password_token(email=email)
        reset_link = f"{self.frontend_url}/{reset_token}"
        email_content = get_reset_password_template(reset_link=reset_link)
        message = self.smtp_server.create_message(
            content=email_content,
            sender_name="OOO ТехСтрой-Сити",
            to_address=email,
            subject="Восстановление пароля",
        )
        await self.smtp_server.send_email(message=message)
        logger.info("Password recovery email sent", extra={"sent_to": email})
        return None

    async def send_new_order_email(self, email: str, order: Order) -> None:
        get_new_order_template(order)
