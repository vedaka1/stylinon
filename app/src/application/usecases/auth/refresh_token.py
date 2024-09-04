from dataclasses import dataclass
from uuid import UUID

from src.application.common.jwt_processor import JwtTokenProcessorInterface
from src.application.common.password_hasher import PasswordHasherInterface
from src.application.common.token import Token
from src.domain.users.service import UserServiceInterface
from src.infrastructure.settings import settings


@dataclass
class RefreshTokenUseCase:
    user_service: UserServiceInterface
    password_hasher: PasswordHasherInterface
    jwt_processor: JwtTokenProcessorInterface

    async def execute(self, refresh_token: str) -> Token:
        user_id = self.jwt_processor.validate_refresh_token(token=refresh_token)
        user = await self.user_service.get_by_id(user_id=user_id)
        access_token = self.jwt_processor.create_access_token(
            user_id=user.id,
            user_role=user.role,
            email=user.email,
        )
        token = Token(
            access_token=access_token,
            refresh_token=refresh_token,
            access_max_age=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            refresh_max_age=settings.jwt.REFRESH_TOKEN_EXPIRE_DAYS * 60 * 60 * 24,
            token_type="Bearer",
        )
        return token
