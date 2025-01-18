from dataclasses import dataclass

from src.application.auth.commands import RefreshTokenCommand
from src.application.auth.dto import RefreshSession, Token
from src.application.auth.exceptions import (
    RefreshTokenNotFoundException,
    TokenExpiredException,
)
from src.application.common.interfaces.jwt_processor import JWTProcessorInterface
from src.application.common.interfaces.password_hasher import PasswordHasherInterface
from src.application.common.interfaces.refresh import RefreshTokenRepositoryInterface
from src.application.common.interfaces.transaction import ICommiter
from src.domain.users.exceptions import UserNotFoundException
from src.domain.users.repository import UserRepositoryInterface
from src.infrastructure.settings import settings


@dataclass
class RefreshTokenUseCase:
    jwt_processor: JWTProcessorInterface
    user_repository: UserRepositoryInterface
    password_hasher: PasswordHasherInterface
    refresh_token_repository: RefreshTokenRepositoryInterface
    commiter: ICommiter

    async def execute(self, command: RefreshTokenCommand) -> Token:
        refresh_session = await self.refresh_token_repository.get(refresh_token=command.refresh_token)
        if not refresh_session:
            raise RefreshTokenNotFoundException

        try:
            user_id = self.jwt_processor.validate_refresh_token(token=command.refresh_token)
        except TokenExpiredException:
            await self.refresh_token_repository.delete_by_token(refresh_token=refresh_session.refresh_token)
            await self.commiter.commit()
            raise

        user = await self.user_repository.get_by_id(user_id=user_id)
        if not user:
            raise UserNotFoundException

        access_token = self.jwt_processor.create_access_token(user_id=user.id, user_role=user.role, email=user.email)
        new_refresh_token = self.jwt_processor.create_refresh_token(user_id=user.id)
        new_refresh_session = RefreshSession.create(
            refresh_token=new_refresh_token,
            user_id=user.id,
            user_agent=refresh_session.user_agent,
        )

        await self.refresh_token_repository.delete_by_token(refresh_token=refresh_session.refresh_token)
        await self.refresh_token_repository.create(refresh_session=new_refresh_session)
        await self.commiter.commit()

        return Token(
            access_token=access_token,
            refresh_token=new_refresh_token,
            access_max_age=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            refresh_max_age=settings.jwt.REFRESH_TOKEN_EXPIRE_DAYS * 60 * 60 * 24,
        )
