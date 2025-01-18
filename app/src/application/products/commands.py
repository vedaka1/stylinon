from dataclasses import dataclass
from uuid import UUID

from src.application.common.pagination import PaginationQuery
from src.domain.products.entities import ProductStatus, UnitsOfMesaurement


@dataclass
class CreateProductCommand:
    name: str
    sku: str
    category: str
    collection: str | None
    size: str | None
    weight: int | None
    image: str
    units_of_measurement: UnitsOfMesaurement
    status: ProductStatus
    retail_price: int
    wholesale_price: int | None = None
    d1_delivery_price: int | None = None
    d1_self_pickup_price: int | None = None
    description: str = 'Описания нет'


@dataclass
class GetManyProductsCommand:
    name: str | None
    category: str | None
    description: str | None
    collection: str | None
    price_from: int | None
    price_to: int | None
    units_of_measurement: UnitsOfMesaurement | None

    pagination: PaginationQuery


@dataclass
class UpdateProductCommand:
    product_id: UUID
    name: str | None = None
    category: str | None = None
    description: str | None = None
    sku: str | None = None
    weight: int | None = None
    collection: str | None = None
    size: str | None = None
    retail_price: int | None = None
    wholesale_price: int | None = None
    d1_delivery_price: int | None = None
    d1_self_pickup_price: int | None = None
    image: str | None | None = None
    units_of_measurement: UnitsOfMesaurement | None = None
    status: ProductStatus | None = None


@dataclass
class CreateCategoryCommand:
    name: str
