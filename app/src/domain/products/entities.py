from dataclasses import dataclass
from enum import Enum
from uuid import UUID, uuid4

from src.domain.products.value_objects import ProductPrice


class UnitsOfMesaurement(str, Enum):
    PIECE = "шт."
    GRAM = "г."
    KILOGRAM = "кг."
    TON = "т."
    MILLILITER = "мл."
    LITER = "л."
    MILLIMETER = "мм."
    CENTIMETER = "см."
    DECIMETER = "дм."
    METER = "м."


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
