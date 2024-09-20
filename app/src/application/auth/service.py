import logging
from abc import ABC, abstractmethod
from datetime import datetime

from src.application.auth.dto import RefreshSession, Token
from src.application.auth.exceptions import (
    RefreshTokenNotFoundException,
    TokenExpiredException,
)
from src.application.common.email.templates import get_reset_password_template
from src.application.common.interfaces.jwt_processor import JwtTokenProcessorInterface
from src.application.common.interfaces.password_hasher import PasswordHasherInterface
from src.application.common.interfaces.refresh import RefreshTokenRepositoryInterface
from src.application.common.interfaces.smtp import SyncSMTPServerInterface
from src.domain.users.entities import User
from src.domain.users.exceptions import (
    UserAlreadyExistsException,
    UserInvalidCredentialsException,
    UserNotFoundException,
)
from src.domain.users.repository import UserRepositoryInterface
from src.infrastructure.settings import settings

logger = logging.getLogger()


class AuthServiceInterface(ABC):

    @abstractmethod
    async def login(
        self,
        username: str,
        password: str,
        user_agent: str,
    ) -> tuple[User, Token]: ...

    @abstractmethod
    async def logout(self, refresh_token: str) -> None: ...

    @abstractmethod
    async def register(
        self,
        email: str,
        password: str,
        mobile_phone: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> None: ...

    @abstractmethod
    async def refresh(self, refresh_token: str) -> Token: ...

    @abstractmethod
    async def reset_password(self, reset_token: str, new_password: str) -> None: ...

    @abstractmethod
    async def send_recovery_email(self, email: str) -> None: ...


class AuthService(AuthServiceInterface):
    __slots__ = (
        "user_repository",
        "password_hasher",
        "jwt_processor",
        "refresh_token_repository",
        "smtp_server",
    )

    def __init__(
        self,
        refresh_token_repository: RefreshTokenRepositoryInterface,
        user_repository: UserRepositoryInterface,
        password_hasher: PasswordHasherInterface,
        jwt_processor: JwtTokenProcessorInterface,
        smtp_server: SyncSMTPServerInterface,
    ) -> None:
        self.refresh_token_repository = refresh_token_repository
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.jwt_processor = jwt_processor
        self.smtp_server = smtp_server

    async def login(
        self,
        username: str,
        password: str,
        user_agent: str,
    ) -> tuple[User, Token]:
        user = await self.user_repository.get_by_email(email=username)
        if not user:
            raise UserNotFoundException
        if not self.password_hasher.verify(
            password=password,
            hash=user.hashed_password,
        ):
            raise UserInvalidCredentialsException
        access_token = self.jwt_processor.create_access_token(
            user_id=user.id,
            user_role=user.role,
            email=user.email,
        )
        current_session = (
            await self.refresh_token_repository.get_by_user_id_and_user_agent(
                user_id=user.id,
                user_agent=user_agent,
            )
        )
        if current_session:
            max_age = current_session.expires_at - datetime.now()
            token = Token(
                access_token=access_token,
                refresh_token=current_session.refresh_token,
                access_max_age=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                refresh_max_age=int(max_age.total_seconds()),
            )
            return user, token
        refresh_token = self.jwt_processor.create_refresh_token(user_id=user.id)
        refresh_session = RefreshSession.create(
            refresh_token=refresh_token,
            user_id=user.id,
            user_agent=user_agent,
        )
        await self.refresh_token_repository.create(refresh_session=refresh_session)
        token = Token(
            access_token=access_token,
            refresh_token=refresh_token,
            access_max_age=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            refresh_max_age=settings.jwt.REFRESH_TOKEN_EXPIRE_DAYS * 60 * 60 * 24,
        )
        return user, token

    async def logout(self, refresh_token: str) -> None:
        await self.refresh_token_repository.delete_by_token(refresh_token=refresh_token)
        return None

    async def register(
        self,
        email: str,
        password: str,
        mobile_phone: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> None:
        user_exist = await self.user_repository.get_by_email(email=email)
        if user_exist:
            raise UserAlreadyExistsException
        hashed_password = self.password_hasher.hash(password)
        user = User.create(
            email=email,
            hashed_password=hashed_password,
            mobile_phone=mobile_phone,
            first_name=first_name,
            last_name=last_name,
        )
        await self.user_repository.create(user=user)
        return None

    async def refresh(self, refresh_token: str) -> Token:
        refresh_session = await self.refresh_token_repository.get(
            refresh_token=refresh_token,
        )
        if not refresh_session:
            raise RefreshTokenNotFoundException
        try:
            user_id = self.jwt_processor.validate_refresh_token(token=refresh_token)
        except TokenExpiredException:
            await self.refresh_token_repository.delete_by_token(
                refresh_token=refresh_session.refresh_token,
            )
            raise
        user = await self.user_repository.get_by_id(user_id=user_id)
        if not user:
            raise UserNotFoundException
        access_token = self.jwt_processor.create_access_token(
            user_id=user.id,
            user_role=user.role,
            email=user.email,
        )
        new_refresh_token = self.jwt_processor.create_refresh_token(user_id=user.id)
        new_refresh_session = RefreshSession.create(
            refresh_token=new_refresh_token,
            user_id=user.id,
            user_agent=refresh_session.user_agent,
        )
        await self.refresh_token_repository.delete_by_token(
            refresh_token=refresh_session.refresh_token,
        )
        await self.refresh_token_repository.create(refresh_session=new_refresh_session)
        return Token(
            access_token=access_token,
            refresh_token=new_refresh_token,
            access_max_age=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            refresh_max_age=settings.jwt.REFRESH_TOKEN_EXPIRE_DAYS * 60 * 60 * 24,
        )

    async def reset_password(self, reset_token: str, new_password: str) -> None:
        token_data = self.jwt_processor.validate_reset_password_token(token=reset_token)
        user = await self.user_repository.get_by_email(email=token_data["email"])
        if not user:
            raise UserNotFoundException
        hashed_password = self.password_hasher.hash(password=new_password)
        user.hashed_password = hashed_password
        await self.user_repository.update(user=user)
        await self.refresh_token_repository.delete_by_user_id(user_id=user.id)
        logger.info("Password reset", extra={"user_email": user.email})
        return None

    async def send_recovery_email(self, email: str) -> None:
        reset_token = self.jwt_processor.create_reset_password_token(email=email)
        reset_link = f"http://localhost/api/v1/reset-password/{reset_token}"
        email_content = get_reset_password_template(reset_link=reset_link)
        message = self.smtp_server.create_message(
            content=email_content,
            to_address=email,
        )
        await self.smtp_server.send_email(message=message)
        logger.info("Password recovery email sent", extra={"sent_to": email})
        return None
