from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from src.application.auth.commands import (
    LoginCommand,
    LogoutCommand,
    RefreshTokenCommand,
    RegisterCommand,
)
from src.application.auth.exceptions import (
    NotAuthorizedException,
    TokenExpiredException,
    WrongTokenTypeException,
)
from src.application.auth.usecases import (  # UserConfirmationUseCase,
    LoginUseCase,
    LogoutUseCase,
    RefreshTokenUseCase,
    RegisterUseCase,
)
from src.application.auth.usecases.login import LogoutUseCase
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
    response: Response,
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> APIResponse[UserOut]:
    command = LoginCommand(password=credentials.password, username=credentials.username)
    user, token = await login_interactor.execute(command=command)
    response.set_cookie(
        "access_token",
        value=token.type + token.access_token,
        max_age=token.access_max_age,
        httponly=True,
        secure=True,
    )
    response.set_cookie(
        "refresh_token",
        value=token.type + token.refresh_token,
        max_age=token.refresh_max_age,
        httponly=True,
        secure=True,
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
        secure=True,
    )
    response.set_cookie(
        "refresh_token",
        value=token.type + token.refresh_token,
        max_age=token.refresh_max_age,
        httponly=True,
        secure=True,
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


# @router.get("/confirmation", summary="Confirms the user by the code from email")
# async def confirmation(
#     confirmation_interactor: FromDishka[UserConfirmationUseCase],
#     command: UserConfirmationCommand = Depends(),
# ) -> APIResponse:
#     await confirmation_interactor.execute(command)
#     return APIResponse()
