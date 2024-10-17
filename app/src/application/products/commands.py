from dataclasses import dataclass
from uuid import UUID

from pydantic import BaseModel
from src.application.common.pagination import PaginationQuery
from src.domain.products.entities import ProductStatus, UnitsOfMesaurement


@dataclass
class CreateProductVariantCommand:
    name: str
    sku: str
    bag_weight: int
    pallet_weight: int
    bags_per_pallet: int
    retail_price: int
    wholesale_delivery_price: int
    d2_delivery_price: int
    d2_self_pickup_price: int
    d1_delivery_price: int
    d1_self_pickup_price: int
    image: str | None
    status: ProductStatus


class CreateProductCommand(BaseModel):
    name: str
    category: str
    description: str
    units_of_measurement: UnitsOfMesaurement
    photo_url: str | None = None

    variants: list[CreateProductVariantCommand] = []


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
    price: int | None = None
    units_of_measurement: UnitsOfMesaurement | None = None
    photo_url: str | None = None


@dataclass
class CreateCategoryCommand:
    name: str
