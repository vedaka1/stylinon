from dataclasses import dataclass
from enum import Enum
from uuid import UUID, uuid4

from src.domain.exceptions.products import ProductIncorrectPriceException


class UnitsOfMesaurement(str, Enum):
    KILOGRAMS = "кг."
    GRAMS = "г."
    LITERS = "л."
    MILLILITERS = "мл."
    PIECES = "шт."


@dataclass
class Product:
    id: UUID
    name: str
    category: str
    description: str
    price: int  # в копейках
    units_of_measurement: UnitsOfMesaurement

    @staticmethod
    def create(
        name: str,
        category: str,
        description: str,
        price: int,
        units_of_measurement: UnitsOfMesaurement,
    ) -> "Product":
        if price <= 0:
            raise ProductIncorrectPriceException
        return Product(
            id=uuid4(),
            name=name,
            category=category,
            description=description,
            price=price,
            units_of_measurement=units_of_measurement,
        )

    def __hash__(self) -> int:
        return hash(self.id)
