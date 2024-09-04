from dataclasses import dataclass

from src.application.common.jwt_processor import JwtTokenProcessorInterface
from src.application.common.password_hasher import PasswordHasherInterface
from src.application.common.token import Token
from src.application.common.transaction import TransactionManagerInterface
from src.application.contracts.commands.user import LoginCommand
from src.application.contracts.responses.user import UserOut
from src.domain.exceptions.user import UserInvalidCredentialsException
from src.domain.users.service import UserServiceInterface
from src.infrastructure.settings import settings


@dataclass
class LoginUseCase:
    user_service: UserServiceInterface
    password_hasher: PasswordHasherInterface
    jwt_processor: JwtTokenProcessorInterface
    transaction_manager: TransactionManagerInterface

    async def execute(self, command: LoginCommand) -> tuple[UserOut, Token]:

        user = await self.user_service.get_by_email(command.username)
        if not user:
            raise UserInvalidCredentialsException
        if not self.password_hasher.verify(
            password=command.password,
            hash=user.hashed_password,
        ):
            raise UserInvalidCredentialsException
        access_token = self.jwt_processor.create_access_token(
            user_id=user.id,
            user_role=user.role,
        )
        refresh_token = self.jwt_processor.create_refresh_token(user_id=user.id)
        user_out = UserOut(
            id=str(user.id),
            email=user.email,
            mobile_phone=user.mobile_phone,
            first_name=user.first_name,
            last_name=user.last_name,
            is_verified=user.is_verified,
            role=user.role,
        )
        token = Token(
            access_token=access_token,
            refresh_token=refresh_token,
            access_max_age=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            refresh_max_age=settings.jwt.REFRESH_TOKEN_EXPIRE_DAYS * 60 * 60 * 24,
            token_type="Bearer",
        )
        return user_out, token
