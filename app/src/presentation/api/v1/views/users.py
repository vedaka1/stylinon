from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, Security
from src.application.auth.dto import UserData
from src.application.chats.dto import ChatOut
from src.application.chats.usecases.get import GetUserChatsUseCase
from src.application.common.pagination import ListPaginatedResponse, PaginationQuery
from src.application.common.response import APIResponse
from src.application.orders.dto import OrderOut
from src.application.users.commands import GetUsersListCommand
from src.application.users.dto import UserOut
from src.application.users.usecases import GetUserOrdersUseCase, GetUsersListUseCase
from src.domain.users.entities import UserRole
from src.presentation.dependencies.auth import get_current_user_data

router = APIRouter(tags=['Users'], prefix='/users', route_class=DishkaRoute)


def get_pagination(limit: int = 10, page: int = 0) -> PaginationQuery:
    return PaginationQuery(page=page, limit=limit)


def get_users_list_command(
    search: str | None = None,
    pagination: PaginationQuery = Depends(get_pagination),
) -> GetUsersListCommand:
    return GetUsersListCommand(search=search, pagiantion=pagination)


@router.get(
    '',
    summary='Возвращает список пользователей',
    dependencies=[Security(get_current_user_data, scopes=[UserRole.ADMIN.value, UserRole.MANAGER.value])],
)
async def get_users(
    get_users_list_interactor: FromDishka[GetUsersListUseCase],
    command: GetUsersListCommand = Depends(get_users_list_command),
) -> APIResponse[ListPaginatedResponse[UserOut]]:
    response = await get_users_list_interactor.execute(command=command)
    return APIResponse(data=response)


@router.get('/me', summary='Возвращает текущего авторизованного пользователя')
async def get_current_user(
    user_data: Annotated[UserData, Security(get_current_user_data, scopes=[])],
) -> APIResponse[UserOut]:
    response = UserOut(
        id=str(user_data.user_id),
        email=user_data.email,
        role=user_data.role,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        mobile_phone=user_data.mobile_phone,
        is_verified=user_data.is_verified,
    )
    return APIResponse(data=response)


@router.get('/me/orders', summary='Возвращает заказы текущего пользователя')
async def get_current_user_orders(
    get_user_orders_interactor: FromDishka[GetUserOrdersUseCase],
    user_data: UserData = Depends(get_current_user_data),
) -> APIResponse[OrderOut]:
    response = await get_user_orders_interactor.execute(email=user_data.email)
    return APIResponse(data=response)


@router.get('/me/chats', summary='Возвращает чаты текущего пользователя')
async def get_current_user_chats(
    get_user_chats_interactor: FromDishka[GetUserChatsUseCase],
    user_data: UserData = Depends(get_current_user_data),
) -> APIResponse[ChatOut]:
    response = await get_user_chats_interactor.execute(user_id=user_data.user_id)
    return APIResponse(data=response)
