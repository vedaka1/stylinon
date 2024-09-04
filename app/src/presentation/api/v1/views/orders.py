from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends
from src.application.common.token import UserTokenData
from src.application.contracts.commands.order import (
    CreateOrderCommand,
    GetManyOrdersCommand,
    UpdateOrderCommand,
)
from src.application.contracts.common.response import APIResponse
from src.application.usecases.order.create import CreateOrderUseCase
from src.application.usecases.order.get import GetManyOrdersUseCase, GetOrderUseCase
from src.application.usecases.order.update import UpdateOrderUseCase
from src.domain.exceptions.base import ApplicationException
from src.domain.exceptions.order import OrderNotFoundException
from src.domain.orders.entities import Order
from src.presentation.dependencies.auth import auth_required, get_current_user_data

router = APIRouter(
    tags=["Orders"],
    prefix="/orders",
    route_class=DishkaRoute,
    dependencies=[Depends(auth_required)],
)


@router.get("", summary="Возвращает список заказов")
async def get_many_orders(
    get_orders_list_interactor: FromDishka[GetManyOrdersUseCase],
    command: GetManyOrdersCommand = Depends(),
) -> APIResponse[Order]:
    response = await get_orders_list_interactor.execute(command=command)
    return APIResponse(data=response)


@router.post("", summary="Создает новый заказ")
async def create_order(
    create_orders_interactor: FromDishka[CreateOrderUseCase],
    command: CreateOrderCommand,
) -> APIResponse[None]:
    await create_orders_interactor.execute(command=command)
    return APIResponse()


@router.get(
    "/{order_id}",
    summary="Возвращает данные о заказе",
    responses={
        200: {"model": APIResponse[Order]},
        404: {"model": OrderNotFoundException},
    },
)
async def get_order(
    order_id: UUID,
    get_order_interactor: FromDishka[GetOrderUseCase],
) -> APIResponse[Order]:
    response = await get_order_interactor.execute(order_id=order_id)
    return APIResponse(data=response)


@router.patch(
    "/{order_id}",
    summary="Обновить данные о заказе",
    responses={
        200: {"model": APIResponse[Order]},
        404: {"model": OrderNotFoundException},
    },
)
async def update_order(
    update_order_interactor: FromDishka[UpdateOrderUseCase],
    command: UpdateOrderCommand = Depends(),
) -> APIResponse[None]:
    await update_order_interactor.execute(command=command)
    return APIResponse()
