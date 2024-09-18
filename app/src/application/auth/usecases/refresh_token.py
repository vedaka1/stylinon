from dataclasses import dataclass

from src.application.auth.commands import RefreshTokenCommand
from src.application.auth.dto import Token
from src.application.auth.service import AuthServiceInterface
from src.application.common.interfaces.transaction import TransactionManagerInterface


@dataclass
class RefreshTokenUseCase:
    auth_service: AuthServiceInterface
    transaction_manager: TransactionManagerInterface

    async def execute(self, command: RefreshTokenCommand) -> Token:
        try:
            return await self.auth_service.refresh(refresh_token=command.refresh_token)
        finally:
            await self.transaction_manager.commit()
