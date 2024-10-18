from dataclasses import dataclass

from src.domain.products.entities import UnitsOfMesaurement


@dataclass
class ProductFilters:
    name: str | None = None
    category: str | None = None
    description: str | None = None
    price_from: int | None = None
    price_to: int | None = None
    units_of_measurement: UnitsOfMesaurement | None = None
    is_available: bool | None = None
