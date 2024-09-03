from typing import Annotated

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

router = APIRouter(
    tags=["Auth"],
    prefix="/auth",
    route_class=DishkaRoute,
)


@router.post("/register", status_code=201, summary="Создает нового пользователя")
async def register(
    command: RegisterCommand,
    register_user_interactor: FromDishka[RegisterUseCase],
) -> APIResponse[None]:
    await register_user_interactor.execute(command)
    return APIResponse()


@router.post(
    "/login",
    summary="Аутентифицирует пользователя и устанавливает access и refresh токены",
)
async def login(
    login_interactor: FromDishka[LoginUseCase],
    response: Response,
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> APIResponse[UserOut]:
    command = LoginCommand(password=credentials.password, username=credentials.username)
    user, token = await login_interactor.execute(command)
    response.set_cookie(
        "access_token",
        token.access_token,
        max_age=token.max_age,
        httponly=True,
        secure=True,
    )
    return APIResponse(data=user)


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
