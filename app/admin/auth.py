from datetime import datetime

from fastapi.security import SecurityScopes
from src.application.auth.commands import LoginCommand
from src.application.auth.usecases.login import LoginWithSessionUseCase
from src.domain.users.entities import UserRole
from src.infrastructure.di.container import get_container
from src.presentation.dependencies.auth import get_current_user_data
from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminConfig, AdminUser, AuthProvider
from starlette_admin.exceptions import LoginFailed


class UsernameAndPasswordProvider(AuthProvider):
    """
    This is only for demo purpose, it's not a better
    way to save and validate user credentials
    """

    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        container = get_container()

        async with container() as container:
            login_usecase = await container.get(LoginWithSessionUseCase)

            user_agent = request.headers.get("User-Agent")

            if not user_agent:
                user_agent = "admin_panel"

            command = LoginCommand(
                username=username,
                password=password,
                user_agent=user_agent,
            )
            try:
                user, session = await login_usecase.execute(command)

            except Exception as e:
                print(e)
                raise LoginFailed("Invalid username or password")

            response.set_cookie(
                "session_id",
                value=str(session.id),
                max_age=int((session.expires_in - datetime.now()).total_seconds()),
                httponly=True,
                # secure=True,
            )
            return response

    async def is_authenticated(self, request: Request) -> bool:
        session_id = request.cookies.get("session_id", None)

        if not session_id:
            return False

        try:
            user_data = await get_current_user_data(
                security_scopes=SecurityScopes(scopes=[UserRole.ADMIN.value]),
                authorization=session_id,
                container=get_container(),
            )
            request.state.user = {
                "id": user_data.user_id,
                "first_name": user_data.first_name,
                "scopes": user_data.scopes,
            }
            return True

        except Exception as e:
            print(e)

            return False

    def get_admin_config(self, request: Request) -> AdminConfig:
        user = request.state.user  # Retrieve current user
        first_name = user["first_name"] if user.get("first_name", None) else "admin"
        # Update app title according to current_user
        custom_app_title = "Hello, " + first_name + "!"
        # Update logo url according to current_user
        custom_logo_url = None

        # if user.get("company_logo_url", None):
        #     custom_logo_url = request.url_for("static", path=user["company_logo_url"])

        return AdminConfig(
            app_title=custom_app_title,
            logo_url=custom_logo_url,
        )

    def get_admin_user(self, request: Request) -> AdminUser:
        user = request.state.user  # Retrieve current user

        photo_url = None

        # if user["avatar"] is not None:
        #     photo_url = request.url_for("static", path=user["avatar"])

        return AdminUser(username=user["first_name"], photo_url=photo_url)

    async def logout(self, request: Request, response: Response) -> Response:
        request.state.user = None

        response.delete_cookie("session_id")
        response.delete_cookie("session")

        return response
