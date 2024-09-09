from dataclasses import dataclass
from uuid import UUID

from src.application.common.jwt_processor import JwtTokenProcessorInterface
from src.application.common.password_hasher import PasswordHasherInterface
from src.application.common.transaction import TransactionManagerInterface
from src.application.contracts.common.token import Token
from src.application.services.auth import AuthServiceInterface


@dataclass
class RefreshTokenUseCase:
    auth_service: AuthServiceInterface
    transaction_manager: TransactionManagerInterface

    async def execute(self, refresh_token: str) -> Token:
        print(refresh_token)
        token = await self.auth_service.refresh(refresh_token)
        await self.transaction_manager.commit()
        print(token)
        return token
