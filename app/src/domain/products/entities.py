from dataclasses import dataclass
from enum import Enum
from uuid import UUID, uuid4

from src.domain.products.exceptions import ProductIncorrectPriceException
from src.domain.products.value_objects import ProductPrice


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
    price: ProductPrice  # в копейках
    units_of_measurement: UnitsOfMesaurement
    photo_url: str | None = None

    @staticmethod
    def create(
        name: str,
        category: str,
        description: str,
        price: int,
        units_of_measurement: UnitsOfMesaurement,
        photo_url: str | None = "/images/no_image.png",
    ) -> "Product":
        return Product(
            id=uuid4(),
            name=name,
            category=category,
            description=description,
            price=ProductPrice(price),
            units_of_measurement=units_of_measurement,
            photo_url=photo_url,
        )

    def __hash__(self) -> int:
        return hash(self.id)
