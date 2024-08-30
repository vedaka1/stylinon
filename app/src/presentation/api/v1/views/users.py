from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from src.application.contracts.commands.user import (
    DeleteUserCommand,
    GetUserCommand,
    GetUsersListCommand,
    UpdateUserCommand,
    UserConfirmationCommand,
)
from src.application.contracts.common.pagination import (
    ListPaginatedResponse,
    PaginationQuery,
)
from src.application.contracts.common.response import APIResponse
from src.application.contracts.responses.user import UserOut
from src.application.usecases.user.get import GetUsersListUseCase, GetUserUseCase
from src.infrastructure.settings import settings
from src.presentation.dependencies.auth import get_current_user_id

router = APIRouter(
    tags=["Users"],
    prefix="/users",
    route_class=DishkaRoute,
)


def get_pagination(limit: int = 10, page: int = 0) -> PaginationQuery:
    return PaginationQuery(page=page, limit=limit)


def get_users_list_command(
    search: str | None = None,
    pagination: PaginationQuery = Depends(get_pagination),
) -> GetUsersListCommand:
    return GetUsersListCommand(search=search, pagiantion=pagination)


@router.get("/me", summary="Возвращает текущего авторизованного пользователя")
async def get_current_user(
    get_user_interactor: FromDishka[GetUserUseCase],
    user_id: UUID = Depends(get_current_user_id),
) -> APIResponse[UserOut]:
    response = await get_user_interactor.execute(user_id)
    return APIResponse(data=response)


@router.get("/", summary="Возвращает список пользователей")
async def get_users(
    get_users_list_interactor: FromDishka[GetUsersListUseCase],
    command: GetUsersListCommand = Depends(get_users_list_command),
    user_id: UUID = Depends(get_current_user_id),
) -> APIResponse[ListPaginatedResponse[UserOut]]:
    response = await get_users_list_interactor.execute(command)
    return APIResponse(data=response)
