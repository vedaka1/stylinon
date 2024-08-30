from dataclasses import dataclass
from uuid import UUID, uuid4

from src.domain.exceptions.products import ProductIncorrectPriceException


@dataclass
class Product:
    id: UUID
    name: str
    category: str
    description: str
    price: int
    units_of_measurement: str

    @staticmethod
    def create(
        name: str,
        category: str,
        description: str,
        price: int,
        units_of_measurement: str,
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
