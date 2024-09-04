from typing import Annotated, Any

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from src.application.contracts.commands.user import LoginCommand, RegisterCommand
from src.application.contracts.common.response import APIResponse
from src.application.contracts.responses.user import UserOut
from src.application.usecases.auth import (  # UserConfirmationUseCase,
    LoginUseCase,
    RegisterUseCase,
)
from src.application.usecases.auth.refresh_token import RefreshTokenUseCase
from src.domain.exceptions.auth import TokenExpiredException, WrongTokenTypeException
from src.domain.exceptions.user import (
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
        token.access_token,
        max_age=token.access_max_age,
        httponly=True,
        secure=True,
    )
    response.set_cookie(
        "refresh_token",
        token.refresh_token,
        max_age=token.refresh_max_age,
        httponly=True,
        secure=True,
    )
    return APIResponse(data=user)


@router.post(
    "/refresh",
    summary="Устанавливает новый access токен",
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
    print(refresh_token)
    token = await refresh_interactor.execute(refresh_token=refresh_token)
    response.set_cookie(
        "access_token",
        token.access_token,
        max_age=token.access_max_age,
        httponly=True,
        secure=True,
    )
    return APIResponse()


@router.post("/logout", summary="Logout")
async def logout(
    response: Response,
) -> APIResponse[UserOut]:
    response.delete_cookie("access_token")
    return APIResponse()


# @router.get("/confirmation", summary="Confirms the user by the code from email")
# async def confirmation(
#     confirmation_interactor: FromDishka[UserConfirmationUseCase],
#     command: UserConfirmationCommand = Depends(),
# ) -> APIResponse:
#     await confirmation_interactor.execute(command)
#     return APIResponse()
