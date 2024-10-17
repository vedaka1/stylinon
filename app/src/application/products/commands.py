from dataclasses import dataclass
from uuid import UUID

from pydantic import BaseModel
from src.application.common.pagination import PaginationQuery
from src.domain.products.entities import ProductStatus, UnitsOfMesaurement


class CreateProductCommand(BaseModel):
    name: str
    category: str
    description: str
    sku: str
    bag_weight: int
    pallet_weight: int
    bags_per_pallet: int
    retail_price: int
    wholesale_delivery_price: int | None
    d2_delivery_price: int | None
    d2_self_pickup_price: int | None
    d1_delivery_price: int | None
    d1_self_pickup_price: int | None
    image: str | None
    units_of_measurement: UnitsOfMesaurement
    status: ProductStatus


@dataclass
class GetManyProductsCommand:
    name: str | None
    category: str | None
    description: str | None
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
    bag_weight: int | None = None
    pallet_weight: int | None = None
    bags_per_pallet: int | None = None
    retail_price: int | None = None
    wholesale_delivery_price: int | None = None
    d2_delivery_price: int | None = None
    d2_self_pickup_price: int | None = None
    d1_delivery_price: int | None = None
    d1_self_pickup_price: int | None = None
    image: str | None | None = None
    units_of_measurement: UnitsOfMesaurement | None = None
    status: ProductStatus | None = None


@dataclass
class CreateCategoryCommand:
    name: str
