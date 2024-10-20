from uuid import UUID, uuid4

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, Form, Security, UploadFile
from src.application.common.pagination import ListPaginatedResponse, PaginationQuery
from src.application.common.response import APIResponse
from src.application.products.commands import (
    CreateProductCommand,
    GetManyProductsCommand,
    UpdateProductCommand,
)
from src.application.products.dto import ProductOut
from src.application.products.usecases import (
    CreateProductUseCase,
    GetManyProductsUseCase,
    GetProductUseCase,
)
from src.application.products.usecases.update import UpdateProductUseCase
from src.domain.common.exceptions.base import ApplicationException
from src.domain.products.entities import ProductStatus, UnitsOfMesaurement
from src.domain.products.exceptions import ProductNotFoundException
from src.domain.users.entities import UserRole
from src.infrastructure.utils.common import StorageBackend
from src.presentation.dependencies.auth import get_current_user_data

router = APIRouter(
    tags=["Products"],
    prefix="/products",
    route_class=DishkaRoute,
)


def get_pagination(limit: int = 100, page: int = 0) -> PaginationQuery:
    return PaginationQuery(page=page, limit=limit)


def get_products_list_command(
    name: str | None = None,
    category: str | None = None,
    collection: str | None = None,
    description: str | None = None,
    price_from: int | None = None,
    price_to: int | None = None,
    units_of_measurement: UnitsOfMesaurement | None = None,
    pagination: PaginationQuery = Depends(get_pagination),
) -> GetManyProductsCommand:
    return GetManyProductsCommand(
        name=name,
        collection=collection,
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
) -> APIResponse[ListPaginatedResponse[ProductOut]]:
    response = await get_products_list_interactor.execute(command=command)

    return APIResponse(data=response)


@router.post(
    "",
    summary="Создает новый товар",
    dependencies=[
        Security(
            get_current_user_data,
            scopes=[
                UserRole.ADMIN.value,
                UserRole.MANAGER.value,
            ],
        ),
    ],
)
async def create_product(
    create_product_interactor: FromDishka[CreateProductUseCase],
    storage_backend: FromDishka[StorageBackend],
    name: str = Form(...),
    category: str = Form(...),
    description: str = Form("Описания нет"),
    units_of_measurement: UnitsOfMesaurement = Form(...),
    sku: str = Form(...),
    retail_price: int = Form(...),
    collection: str | None = Form(None),
    size: str | None = Form(None),
    wholesale_price: int | None = Form(None),
    d1_delivery_price: int | None = Form(None),
    d1_self_pickup_price: int | None = Form(None),
    status: ProductStatus = Form(...),
    weight: int | None = Form(None),
    image: UploadFile | None = None,
) -> APIResponse[None]:
    image_path = "/images/no_image.png"

    if image:
        try:
            content_type = "jpg"

            if image.filename:
                content_type = image.filename.split(".")[1]

            image_id = str(uuid4())

            file_name = f"{image_id}.{content_type}"

            image_path = storage_backend.write(file_name=file_name, file=image)

        except Exception:
            raise ApplicationException

        finally:
            await image.close()

    command = CreateProductCommand(
        name=name,
        category=category,
        description=description,
        collection=collection,
        size=size,
        sku=sku,
        weight=weight,
        retail_price=retail_price,
        wholesale_price=wholesale_price,
        d1_delivery_price=d1_delivery_price,
        d1_self_pickup_price=d1_self_pickup_price,
        units_of_measurement=units_of_measurement,
        image=image_path,
        status=status,
    )

    await create_product_interactor.execute(command=command)

    return APIResponse()


@router.get(
    "/{product_id}",
    summary="Возвращает данные о товаре",
    responses={
        200: {"model": APIResponse[ProductOut]},
        404: {"model": ProductNotFoundException},
    },
)
async def get_product(
    product_id: UUID,
    get_product_interactor: FromDishka[GetProductUseCase],
) -> APIResponse[ProductOut]:
    response = await get_product_interactor.execute(product_id=product_id)

    return APIResponse(data=response)


@router.patch(
    "/{product_id}",
    summary="Обновляет данные о товаре",
    dependencies=[
        Security(
            get_current_user_data,
            scopes=[
                UserRole.ADMIN.value,
                UserRole.MANAGER.value,
            ],
        ),
    ],
)
async def update_product(
    update_product_interactor: FromDishka[UpdateProductUseCase],
    command: UpdateProductCommand = Depends(),
) -> APIResponse[None]:
    await update_product_interactor.execute(command=command)

    return APIResponse()
