import logging
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, Request
from src.application.common.response import APIResponse
from src.application.orders.commands import (
    CreateOrderCommand,
    GetManyOrdersCommand,
    UpdateOrderCommand,
)
from src.application.orders.responses import CreateOrderResponse, OrderOut
from src.application.orders.usecases import (
    CreateOrderUseCase,
    GetManyOrdersUseCase,
    GetOrderUseCase,
    UpdateOrderByWebhookUseCase,
    UpdateOrderUseCase,
)
from src.domain.orders.entities import Order
from src.domain.orders.exceptions import (
    OrderItemIncorrectQuantityException,
    OrderNotFoundException,
)
from src.presentation.dependencies.auth import auth_required, get_current_user_data

router = APIRouter(
    tags=["Orders"],
    prefix="/orders",
    route_class=DishkaRoute,
)


@router.get(
    "",
    summary="Возвращает список заказов",
    dependencies=[Depends(auth_required)],
)
async def get_many_orders(
    get_orders_list_interactor: FromDishka[GetManyOrdersUseCase],
    command: GetManyOrdersCommand = Depends(),
) -> APIResponse[OrderOut]:
    response = await get_orders_list_interactor.execute(command=command)
    return APIResponse(data=response)


@router.post(
    "",
    summary="Создает новый заказ",
    responses={
        200: {"model": APIResponse[CreateOrderResponse]},
        400: {"model": OrderItemIncorrectQuantityException},
    },
    dependencies=[Depends(auth_required)],
)
async def create_order(
    create_orders_interactor: FromDishka[CreateOrderUseCase],
    command: CreateOrderCommand,
) -> APIResponse[CreateOrderResponse]:
    response = await create_orders_interactor.execute(command=command)
    return APIResponse(data=response)


@router.get(
    "/{order_id}",
    summary="Возвращает данные о заказе",
    responses={
        200: {"model": APIResponse[Order]},
        404: {"model": OrderNotFoundException},
    },
    dependencies=[Depends(auth_required)],
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
    dependencies=[Depends(auth_required)],
)
async def update_order(
    update_order_interactor: FromDishka[UpdateOrderUseCase],
    command: UpdateOrderCommand = Depends(),
) -> APIResponse[None]:
    await update_order_interactor.execute(command=command)
    return APIResponse()


@router.post("/webhooks/payment")
async def payment_webhook(
    request: Request,
    update_order_interactor: FromDishka[UpdateOrderByWebhookUseCase],
) -> APIResponse[None]:
    token = await request.body()
    await update_order_interactor.execute(token=token.decode())
    return APIResponse()
