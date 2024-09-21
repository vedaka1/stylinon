from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from src.application.auth.commands import (
    LoginCommand,
    LogoutCommand,
    RefreshTokenCommand,
    RegisterCommand,
    ResetPasswordCommand,
)
from src.application.auth.exceptions import (
    NotAuthorizedException,
    TokenExpiredException,
    WrongTokenTypeException,
)
from src.application.auth.usecases import (
    LoginUseCase,
    LogoutUseCase,
    PasswordRecoveryUseCase,
    RefreshTokenUseCase,
    RegisterUseCase,
    ResetPasswordUseCase,
)
from src.application.common.response import APIResponse
from src.application.users.responses import UserOut
from src.domain.users.exceptions import (
    UserAlreadyExistsException,
    UserInvalidCredentialsException,
)
from src.presentation.dependencies.auth import get_refresh_token

router = APIRouter(
    tags=["Auth"],
    prefix="/auth",
    route_class=DishkaRoute,
)


@router.post(
    "/register",
    status_code=201,
    summary="Создает нового пользователя",
    responses={
        201: {"model": APIResponse[None]},
        409: {"model": UserAlreadyExistsException},
    },
)
async def register(
    command: RegisterCommand,
    register_user_interactor: FromDishka[RegisterUseCase],
) -> APIResponse[None]:
    await register_user_interactor.execute(command=command)
    return APIResponse()


@router.post(
    "/login",
    summary="Аутентифицирует пользователя и устанавливает access и refresh токены",
    responses={
        200: {"model": APIResponse[UserOut]},
        400: {"model": UserInvalidCredentialsException},
    },
)
async def login(
    login_interactor: FromDishka[LoginUseCase],
    request: Request,
    response: Response,
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> APIResponse[UserOut]:
    user_agent = request.headers.get("user-agent")
    if not user_agent:
        user_agent = "none"
    command = LoginCommand(
        password=credentials.password,
        username=credentials.username,
        user_agent=user_agent,
    )
    user, token = await login_interactor.execute(command=command)
    response.set_cookie(
        "access_token",
        value=token.type + token.access_token,
        max_age=token.access_max_age,
        httponly=True,
        # secure=True,
    )
    response.set_cookie(
        "refresh_token",
        value=token.type + token.refresh_token,
        max_age=token.refresh_max_age,
        httponly=True,
        # secure=True,
    )
    return APIResponse(data=user)


@router.post(
    "/refresh",
    summary="Устанавливает новые access и refresh токены",
    responses={
        200: {"model": APIResponse[None]},
        400: {"model": WrongTokenTypeException},
        401: {"model": TokenExpiredException},
    },
)
async def refresh(
    response: Response,
    refresh_interactor: FromDishka[RefreshTokenUseCase],
    refresh_token: Annotated[str, Depends(get_refresh_token)],
) -> APIResponse[None]:
    command = RefreshTokenCommand(refresh_token=refresh_token)
    token = await refresh_interactor.execute(command=command)
    response.set_cookie(
        "access_token",
        value=token.type + token.access_token,
        max_age=token.access_max_age,
        httponly=True,
        # secure=True,
    )
    response.set_cookie(
        "refresh_token",
        value=token.type + token.refresh_token,
        max_age=token.refresh_max_age,
        httponly=True,
        # secure=True,
    )
    return APIResponse()


@router.post(
    "/logout",
    summary="Logout",
    responses={
        200: {"model": APIResponse[None]},
        401: {"model": NotAuthorizedException},
    },
)
async def logout(
    response: Response,
    logout_interactor: FromDishka[LogoutUseCase],
    refresh_token: Annotated[str, Depends(get_refresh_token)],
) -> APIResponse[None]:
    command = LogoutCommand(refresh_token=refresh_token)
    await logout_interactor.execute(command=command)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return APIResponse()


@router.post(
    "/password-recovery/{email}",
    summary="Отправка письма для восстановления пароля через email",
    responses={200: {"model": APIResponse[None]}},
)
async def password_recovery(
    email: EmailStr,
    password_recovery_interactor: FromDishka[PasswordRecoveryUseCase],
) -> APIResponse[None]:
    await password_recovery_interactor.execute(email=email)
    return APIResponse()


@router.post(
    "/reset-password",
    summary="Сброс пароля",
    responses={200: {"model": APIResponse[None]}},
)
async def reset_password(
    command: ResetPasswordCommand,
    response: Response,
    reset_password_interactor: FromDishka[ResetPasswordUseCase],
) -> APIResponse[None]:
    await reset_password_interactor.execute(command=command)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return APIResponse()
