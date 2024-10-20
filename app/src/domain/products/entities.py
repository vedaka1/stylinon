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
    CUBIC_MILLIMETER = "мм2."
    CUBIC_CENTIMETER = "см2."
    CUBIC_DECIMETER = "дм2."
    CUBIC_METER = "м2."


class ProductStatus(str, Enum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    ON_REQUEST = "on_request"


@dataclass
class Category:
    name: str
    is_available: bool

    @staticmethod
    def create(name: str, is_available: bool = True) -> "Category":
        return Category(
            name=name,
            is_available=is_available,
        )


@dataclass
class Product:
    id: UUID
    name: str
    sku: str
    description: str
    category: str
    collection: str | None
    weight: int | None
    size: str | None
    retail_price: ProductPrice
    wholesale_price: ProductPrice | None
    d1_delivery_price: ProductPrice | None
    d1_self_pickup_price: ProductPrice | None
    units_of_measurement: UnitsOfMesaurement
    image: str | None
    status: ProductStatus
    is_available: bool

    @staticmethod
    def create(
        name: str,
        sku: str,
        category: str,
        description: str,
        retail_price: ProductPrice,
        *,
        weight: int | None = None,
        collection: str | None = None,
        size: str | None = None,
        wholesale_price: ProductPrice | None = None,
        d1_delivery_price: ProductPrice | None = None,
        d1_self_pickup_price: ProductPrice | None = None,
        units_of_measurement: UnitsOfMesaurement = UnitsOfMesaurement.PIECE,
        image: str | None = "/images/no_image.png",
        status: ProductStatus = ProductStatus.AVAILABLE,
        is_available: bool = True,
    ) -> "Product":
        return Product(
            id=uuid4(),
            name=name,
            category=category,
            description=description,
            units_of_measurement=units_of_measurement,
            sku=sku,
            weight=weight,
            collection=collection,
            size=size,
            image=image,
            retail_price=retail_price,
            wholesale_price=wholesale_price,
            d1_delivery_price=d1_delivery_price,
            d1_self_pickup_price=d1_self_pickup_price,
            status=status,
            is_available=is_available,
        )

    def __hash__(self) -> int:
        return hash(self.id)
