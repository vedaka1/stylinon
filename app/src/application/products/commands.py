from dataclasses import dataclass
from uuid import UUID

from src.application.common.pagination import PaginationQuery
from src.domain.products.entities import UnitsOfMesaurement


@dataclass
class CreateProductCommand:
    name: str
    category: str
    description: str
    price: int
    units_of_measurement: UnitsOfMesaurement


@dataclass
class GetManyProductsCommand:
    name: str | None
    category: str | None
    description: str | None
    price_from: int | None
    price_to: int | None
    units_of_measurement: UnitsOfMesaurement | None

    pagination: PaginationQuery
