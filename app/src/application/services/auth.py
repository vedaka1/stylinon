from abc import ABC, abstractmethod
from uuid import UUID

from src.application.common.jwt_processor import JwtTokenProcessorInterface
from src.application.common.password_hasher import PasswordHasherInterface
from src.application.contracts.common.token import RefreshSession, Token
from src.domain.exceptions.auth import RefreshTokenNotFoundException
from src.domain.exceptions.user import (
    UserAlreadyExistsException,
    UserInvalidCredentialsException,
    UserNotFoundException,
)
from src.domain.users.entities import User
from src.domain.users.repository import UserRepositoryInterface
from src.infrastructure.persistence.postgresql.repositories.refresh import (
    RefreshTokenRepositoryInterface,
)
from src.infrastructure.settings import settings


class AuthServiceInterface(ABC):

    @abstractmethod
    async def login(self, username: str, password: str) -> tuple[User, Token]: ...

    @abstractmethod
    async def logout(self, refresh_token: str) -> None: ...

    @abstractmethod
    async def register(
        self,
        email: str,
        password: str,
        mobile_phone: str | None,
        first_name: str | None,
        last_name: str | None,
    ) -> None: ...

    @abstractmethod
    async def refresh(self, refresh_token: str) -> Token: ...


class AuthService(AuthServiceInterface):
    __slots__ = (
        "user_repository",
        "password_hasher",
        "jwt_processor",
        "refresh_token_repository",
    )

    def __init__(
        self,
        refresh_token_repository: RefreshTokenRepositoryInterface,
        user_repository: UserRepositoryInterface,
        password_hasher: PasswordHasherInterface,
        jwt_processor: JwtTokenProcessorInterface,
    ) -> None:
        self.refresh_token_repository = refresh_token_repository
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.jwt_processor = jwt_processor

    async def login(self, username: str, password: str) -> tuple[User, Token]:
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
        refresh_token = self.jwt_processor.create_refresh_token(user_id=user.id)
        refresh_session = RefreshSession.create(
            refresh_token=refresh_token,
            user_id=user.id,
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
        mobile_phone: str | None,
        first_name: str | None,
        last_name: str | None,
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
        user_id = self.jwt_processor.validate_refresh_token(token=refresh_token)
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
