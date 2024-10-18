from typing import cast

from fastapi.security import SecurityScopes
from sqladmin.authentication import AuthenticationBackend
from src.application.auth.commands import LoginCommand
from src.application.auth.usecases.login import LoginWithSessionUseCase
from src.domain.users.entities import UserRole
from src.infrastructure.di.container import get_container
from src.presentation.dependencies.auth import get_current_user_data
from starlette.requests import Request


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        # Validate username/password credentials
        # And update session
        container = get_container()
        async with container() as container:
            login_usecase = await container.get(LoginWithSessionUseCase)

            user_agent = request.headers.get("User-Agent")

            if not user_agent:
                user_agent = "admin_panel"

            command = LoginCommand(
                username=cast(str, username),
                password=cast(str, password),
                user_agent=user_agent,
            )
            _, session = await login_usecase.execute(command)

            request.session["token"] = str(session.id)

            return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        try:
            await get_current_user_data(
                security_scopes=SecurityScopes(scopes=[UserRole.ADMIN.value]),
                authorization=token,
                container=get_container(),
            )
        except Exception as e:
            print(e)
            return False

        return True
