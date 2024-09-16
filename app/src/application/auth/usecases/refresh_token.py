from dataclasses import dataclass

from src.application.auth.dto import Token
from src.application.auth.service import AuthServiceInterface
from src.application.common.transaction import TransactionManagerInterface


@dataclass
class RefreshTokenUseCase:
    auth_service: AuthServiceInterface
    transaction_manager: TransactionManagerInterface

    async def execute(self, refresh_token: str) -> Token:
        try:
            return await self.auth_service.refresh(refresh_token)
        finally:
            await self.transaction_manager.commit()
