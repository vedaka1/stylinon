from dataclasses import dataclass

from src.domain.products.entities import ProductStatus, UnitsOfMesaurement


@dataclass
class ProductFilters:
    name: str | None = None
    category: str | None = None
    description: str | None = None
    price_from: int | None = None
    price_to: int | None = None
    units_of_measurement: UnitsOfMesaurement | None = None
    status: ProductStatus | None = None
    collection: str | None = None
    is_available: bool | None = None
