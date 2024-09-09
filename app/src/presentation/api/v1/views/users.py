from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends
from src.application.contracts.commands.user import GetUsersListCommand
from src.application.contracts.common.pagination import (
    ListPaginatedResponse,
    PaginationQuery,
)
from src.application.contracts.common.response import APIResponse
from src.application.contracts.common.token import UserTokenData
from src.application.contracts.responses.order import OrderOut
from src.application.contracts.responses.user import UserOut
from src.application.usecases.user.get import (
    GetUserOrdersUseCase,
    GetUsersListUseCase,
    GetUserUseCase,
)
from src.presentation.dependencies.auth import get_current_user_data

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
    user_data: UserTokenData = Depends(get_current_user_data),
) -> APIResponse[UserOut]:
    response = await get_user_interactor.execute(user_id=user_data.user_id)
    return APIResponse(data=response)


@router.get("/me/orders", summary="Возвращает заказы текущего пользователя")
async def get_current_user_orders(
    get_user_orders_interactor: FromDishka[GetUserOrdersUseCase],
    user_data: UserTokenData = Depends(get_current_user_data),
) -> APIResponse[OrderOut]:
    response = await get_user_orders_interactor.execute(email=user_data.email)
    return APIResponse(data=response)


@router.get("", summary="Возвращает список пользователей")
async def get_users(
    get_users_list_interactor: FromDishka[GetUsersListUseCase],
    command: GetUsersListCommand = Depends(get_users_list_command),
    user_data: UserTokenData = Depends(get_current_user_data),
) -> APIResponse[ListPaginatedResponse[UserOut]]:
    response = await get_users_list_interactor.execute(command=command)
    return APIResponse(data=response)
