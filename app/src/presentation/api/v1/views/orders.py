from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from src.application.contracts.commands.order import (
    CreateOrderCommand,
    GetManyOrdersCommand,
    UpdateOrderCommand,
)
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
from src.application.usecases.order.create import CreateOrderUseCase
from src.application.usecases.order.get import GetManyOrdersUseCase, GetOrderUseCase
from src.application.usecases.order.update import UpdateOrderUseCase
from src.application.usecases.user.get import GetUsersListUseCase, GetUserUseCase
from src.domain.orders.entities import Order
from src.infrastructure.settings import settings
from src.presentation.dependencies.auth import get_current_user_id

router = APIRouter(
    tags=["Orders"],
    prefix="/orders",
    route_class=DishkaRoute,
)


@router.get("", summary="Возвращает список заказов")
async def get_many_orders(
    get_orders_list_interactor: FromDishka[GetManyOrdersUseCase],
    command: GetManyOrdersCommand = Depends(),
    user_id: UUID = Depends(get_current_user_id),
) -> APIResponse[Order]:
    response = await get_orders_list_interactor.execute(command)
    return APIResponse(data=response)


@router.post("", summary="Создает новый заказ")
async def create_order(
    create_orders_interactor: FromDishka[CreateOrderUseCase],
    command: CreateOrderCommand,
    user_id: UUID = Depends(get_current_user_id),
) -> APIResponse:
    await create_orders_interactor.execute(command=command)
    return APIResponse()


@router.get("/{order_id}", summary="Возвращает данные о заказе")
async def get_order(
    order_id: UUID,
    get_order_interactor: FromDishka[GetOrderUseCase],
    user_id: UUID = Depends(get_current_user_id),
) -> APIResponse[Order]:
    response = await get_order_interactor.execute(order_id=order_id)
    return APIResponse(data=response)


@router.patch("/{order_id}", summary="Обновить данные о заказе")
async def update_order(
    order_id: UUID,
    update_order_interactor: FromDishka[UpdateOrderUseCase],
    command: UpdateOrderCommand = Depends(),
    user_id: UUID = Depends(get_current_user_id),
) -> APIResponse:
    await update_order_interactor.execute(command=command)
    return APIResponse()
