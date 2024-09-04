from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends
from src.application.contracts.commands.product import (
    CreateProductCommand,
    GetManyProductsCommand,
)
from src.application.contracts.common.pagination import (
    ListPaginatedResponse,
    PaginationQuery,
)
from src.application.contracts.common.response import APIResponse
from src.application.usecases.product.create import CreateProductUseCase
from src.application.usecases.product.get import (
    GetManyProductsUseCase,
    GetProductUseCase,
)
from src.domain.exceptions.products import ProductNotFoundException
from src.domain.products.entities import Product, UnitsOfMesaurement
from src.presentation.dependencies.auth import auth_required, get_current_user_data

router = APIRouter(
    tags=["Products"],
    prefix="/products",
    route_class=DishkaRoute,
    dependencies=[Depends(auth_required)],
)


def get_pagination(limit: int = 100, page: int = 0) -> PaginationQuery:
    return PaginationQuery(page=page, limit=limit)


def get_products_list_command(
    name: str | None = None,
    category: str | None = None,
    description: str | None = None,
    price_from: int | None = None,
    price_to: int | None = None,
    units_of_measurement: UnitsOfMesaurement | None = None,
    pagination: PaginationQuery = Depends(get_pagination),
) -> GetManyProductsCommand:
    return GetManyProductsCommand(
        name=name,
        category=category,
        description=description,
        price_from=price_from,
        price_to=price_to,
        units_of_measurement=units_of_measurement,
        pagination=pagination,
    )


@router.get("", summary="Возвращает список товаров")
async def get_many_products(
    get_products_list_interactor: FromDishka[GetManyProductsUseCase],
    command: GetManyProductsCommand = Depends(get_products_list_command),
) -> APIResponse[ListPaginatedResponse[Product]]:
    response = await get_products_list_interactor.execute(command=command)
    return APIResponse(data=response)


@router.post("", summary="Создает новый товар")
async def create_product(
    create_product_interactor: FromDishka[CreateProductUseCase],
    command: CreateProductCommand,
) -> APIResponse[None]:
    await create_product_interactor.execute(command=command)
    return APIResponse()


@router.get(
    "/{product_id}",
    summary="Возвращает данные о товаре",
    responses={
        200: {"model": APIResponse[Product]},
        404: {"model": ProductNotFoundException},
    },
)
async def get_product(
    product_id: UUID,
    get_product_interactor: FromDishka[GetProductUseCase],
) -> APIResponse[Product]:
    response = await get_product_interactor.execute(product_id=product_id)
    return APIResponse(data=response)
