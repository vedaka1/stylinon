from dataclasses import dataclass

from src.application.auth.commands import ResetPasswordCommand
from src.application.auth.service import AuthServiceInterface
from src.application.common.interfaces.transaction import TransactionManagerInterface


@dataclass
class PasswordRecoveryUseCase:
    auth_service: AuthServiceInterface

    async def execute(self, email: str) -> None:
        await self.auth_service.send_recovery_email(email=email)
        return None


@dataclass
class ResetPasswordUseCase:
    auth_service: AuthServiceInterface
    transaction_manager: TransactionManagerInterface

    async def execute(self, command: ResetPasswordCommand) -> None:
        await self.auth_service.reset_password(
            reset_token=command.reset_token,
            new_password=command.new_password,
        )
        await self.transaction_manager.commit()
        return None
