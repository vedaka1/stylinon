import logging
from dataclasses import dataclass
from datetime import datetime

from src.application.auth.commands import (
    LoginCommand,
    LogoutWithJWTCommand,
    LogoutWithSessionCommand,
)
from src.application.auth.dto import RefreshSession, Token
from src.application.common.interfaces.jwt_processor import JWTProcessorInterface
from src.application.common.interfaces.password_hasher import PasswordHasherInterface
from src.application.common.interfaces.refresh import RefreshTokenRepositoryInterface
from src.application.common.interfaces.transaction import ICommiter
from src.application.users.dto import UserOut
from src.domain.users.entities import UserSession
from src.domain.users.exceptions import UserInvalidCredentialsException
from src.domain.users.repository import (
    UserRepositoryInterface,
    UserSessionRepositoryInterface,
)
from src.infrastructure.settings import settings

logger = logging.getLogger()


@dataclass
class LoginWithJWTUseCase:
    user_repository: UserRepositoryInterface
    password_hasher: PasswordHasherInterface
    refresh_token_repository: RefreshTokenRepositoryInterface
    jwt_processor: JWTProcessorInterface
    commiter: ICommiter

    async def execute(self, command: LoginCommand) -> tuple[UserOut, Token]:
        user = await self.user_repository.get_by_email(email=command.username)
        if not user:
            raise UserInvalidCredentialsException

        if not self.password_hasher.verify(password=command.password, hash=user.hashed_password):
            raise UserInvalidCredentialsException

        access_token = self.jwt_processor.create_access_token(user_id=user.id, user_role=user.role, email=user.email)
        current_session = await self.refresh_token_repository.get_by_user_id_and_user_agent(
            user_id=user.id,
            user_agent=command.user_agent,
        )

        user_out = UserOut(
            id=str(user.id),
            email=user.email,
            mobile_phone=user.mobile_phone,
            first_name=user.first_name,
            last_name=user.last_name,
            is_verified=user.is_verified,
            role=user.role,
        )
        # returns an exisiting refresh session, if any
        if current_session:
            max_age = current_session.expires_at - datetime.now()
            token = Token(
                access_token=access_token,
                refresh_token=current_session.refresh_token,
                access_max_age=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                refresh_max_age=int(max_age.total_seconds()),
            )
            return user_out, token

        refresh_token = self.jwt_processor.create_refresh_token(user_id=user.id)
        refresh_session = RefreshSession.create(
            refresh_token=refresh_token,
            user_id=user.id,
            user_agent=command.user_agent,
        )

        await self.refresh_token_repository.create(refresh_session=refresh_session)

        token = Token(
            access_token=access_token,
            refresh_token=refresh_token,
            access_max_age=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            refresh_max_age=settings.jwt.REFRESH_TOKEN_EXPIRE_DAYS * 60 * 60 * 24,
        )

        await self.commiter.commit()

        return user_out, token


@dataclass
class LoginWithSessionUseCase:
    user_repository: UserRepositoryInterface
    password_hasher: PasswordHasherInterface
    user_session_repository: UserSessionRepositoryInterface
    commiter: ICommiter

    async def execute(self, command: LoginCommand) -> tuple[UserOut, UserSession]:
        user = await self.user_repository.get_by_email(email=command.username)
        if not user:
            raise UserInvalidCredentialsException

        if not self.password_hasher.verify(password=command.password, hash=user.hashed_password):
            raise UserInvalidCredentialsException

        current_session = await self.user_session_repository.get_by_user_id_and_user_agent(
            user_id=user.id,
            user_agent=command.user_agent,
        )

        user_out = UserOut(
            id=str(user.id),
            email=user.email,
            mobile_phone=user.mobile_phone,
            first_name=user.first_name,
            last_name=user.last_name,
            is_verified=user.is_verified,
            role=user.role,
        )
        # returns an exisiting session, if any
        if current_session:
            return user_out, current_session

        session = UserSession.create(user_id=user.id, user_agent=command.user_agent)
        await self.user_session_repository.create(session=session)
        await self.commiter.commit()

        return user_out, session


@dataclass
class LogoutWithJWTUseCase:
    refresh_token_repository: RefreshTokenRepositoryInterface
    commiter: ICommiter

    async def execute(self, command: LogoutWithJWTCommand) -> None:
        await self.refresh_token_repository.delete_by_token(refresh_token=command.refresh_token)
        await self.commiter.commit()

        return None


@dataclass
class LogoutWithSessionUseCase:
    user_session_repository: UserSessionRepositoryInterface
    commiter: ICommiter

    async def execute(self, command: LogoutWithSessionCommand) -> None:
        await self.user_session_repository.delete(session_id=command.session_id)
        await self.commiter.commit()

        return None
