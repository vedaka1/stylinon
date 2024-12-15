import logging
from dataclasses import dataclass

from src.application.auth.commands import ResetPasswordCommand
from src.application.common.email.types import SenderName
from src.application.common.email.utils import get_reset_password_template
from src.application.common.interfaces.jwt_processor import JWTProcessorInterface
from src.application.common.interfaces.password_hasher import PasswordHasherInterface
from src.application.common.interfaces.refresh import RefreshTokenRepositoryInterface
from src.application.common.interfaces.smtp import SyncSMTPServerInterface
from src.application.common.interfaces.transaction import TransactionManagerInterface
from src.domain.users.exceptions import UserNotFoundException
from src.domain.users.repository import UserRepositoryInterface

logger = logging.getLogger()


@dataclass
class PasswordRecoveryUseCase:
    user_repository: UserRepositoryInterface
    jwt_processor: JWTProcessorInterface
    smtp_server: SyncSMTPServerInterface
    sender_name: SenderName

    async def execute(self, email: str) -> None:
        user = await self.user_repository.get_by_email(email=email)
        if not user:
            raise UserNotFoundException

        frontend_url = "https://localhost/api/v1/reset-password"

        reset_token = self.jwt_processor.create_reset_password_token(email=email)
        reset_link = f"{frontend_url}/{reset_token}"
        email_content = get_reset_password_template(reset_link=reset_link)

        message = self.smtp_server.create_message(
            content=email_content,
            sender_name=self.sender_name,
            to_address=email,
            subject="Восстановление пароля",
        )

        await self.smtp_server.send_email(message=message)

        logger.info("PasswordRecoveryUseCase", extra={"sent_to": email})
        return None


@dataclass
class ResetPasswordUseCase:
    jwt_processor: JWTProcessorInterface
    user_repository: UserRepositoryInterface
    password_hasher: PasswordHasherInterface
    refresh_token_repository: RefreshTokenRepositoryInterface
    transaction_manager: TransactionManagerInterface

    async def execute(self, command: ResetPasswordCommand) -> None:
        token_data = self.jwt_processor.validate_reset_password_token(
            token=command.reset_token,
        )
        user = await self.user_repository.get_by_email(email=token_data["email"])

        if not user:
            raise UserNotFoundException

        hashed_password = self.password_hasher.hash(password=command.new_password)

        user.hashed_password = hashed_password

        await self.user_repository.update(user=user)

        await self.refresh_token_repository.delete_by_user_id(user_id=user.id)

        await self.transaction_manager.commit()

        logger.info("ResetPasswordUseCase", extra={"user_email": user.email})

        return None
