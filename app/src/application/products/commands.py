from dataclasses import dataclass
from uuid import UUID

from pydantic import BaseModel
from src.application.common.pagination import PaginationQuery
from src.domain.products.entities import UnitsOfMesaurement


class CreateProductCommand(BaseModel):
    name: str
    category: str
    description: str
    price: int
    units_of_measurement: UnitsOfMesaurement
    photo_url: str | None = None


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
