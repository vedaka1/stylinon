from dataclasses import dataclass

from src.application.common.transaction import TransactionManagerInterface
from src.application.contracts.commands.user import LoginCommand
from src.application.contracts.common.token import Token
from src.application.contracts.responses.user import UserOut
from src.application.services.auth import AuthServiceInterface


@dataclass
class LoginUseCase:
    auth_service: AuthServiceInterface
    transaction_manager: TransactionManagerInterface

    async def execute(self, command: LoginCommand) -> tuple[UserOut, Token]:
        user, token = await self.auth_service.login(
            username=command.username,
            password=command.password,
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
        await self.transaction_manager.commit()
        return user_out, token


from dataclasses import dataclass

from src.application.common.transaction import TransactionManagerInterface
from src.application.contracts.commands.user import LoginCommand
from src.application.contracts.common.token import Token
from src.application.contracts.responses.user import UserOut
from src.application.services.auth import AuthServiceInterface


@dataclass
class LogoutUseCase:
    auth_service: AuthServiceInterface
    transaction_manager: TransactionManagerInterface

    async def execute(self, refresh_token: str) -> None:
        await self.auth_service.logout(refresh_token=refresh_token)
        await self.transaction_manager.commit()
        return None
