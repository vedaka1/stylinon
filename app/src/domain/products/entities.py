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


class ProductStatus(str, Enum):
    IN_STOCK = "in_stock"
    OUT_OF_STOCK = "out_of_stock"


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
    category: str
    description: str
    sku: str
    bag_weight: int
    pallet_weight: int
    bags_per_pallet: int
    retail_price: ProductPrice
    wholesale_delivery_price: ProductPrice | None
    d2_delivery_price: ProductPrice | None
    d2_self_pickup_price: ProductPrice | None
    d1_delivery_price: ProductPrice | None
    d1_self_pickup_price: ProductPrice | None
    units_of_measurement: UnitsOfMesaurement
    image: str | None
    status: ProductStatus
    is_available: bool

    @staticmethod
    def create(
        name: str,
        category: str,
        description: str,
        sku: str,
        bag_weight: int,
        pallet_weight: int,
        bags_per_pallet: int,
        retail_price: ProductPrice,
        *,
        wholesale_delivery_price: ProductPrice | None = None,
        d2_delivery_price: ProductPrice | None = None,
        d2_self_pickup_price: ProductPrice | None = None,
        d1_delivery_price: ProductPrice | None = None,
        d1_self_pickup_price: ProductPrice | None = None,
        units_of_measurement: UnitsOfMesaurement = UnitsOfMesaurement.PIECE,
        image: str | None = "/images/no_image.png",
        status: ProductStatus = ProductStatus.IN_STOCK,
        is_available: bool = True,
    ) -> "Product":
        return Product(
            id=uuid4(),
            name=name,
            category=category,
            description=description,
            units_of_measurement=units_of_measurement,
            sku=sku,
            bag_weight=bag_weight,
            pallet_weight=pallet_weight,
            bags_per_pallet=bags_per_pallet,
            image=image,
            retail_price=retail_price,
            wholesale_delivery_price=wholesale_delivery_price,
            d2_delivery_price=d2_delivery_price,
            d2_self_pickup_price=d2_self_pickup_price,
            d1_delivery_price=d1_delivery_price,
            d1_self_pickup_price=d1_self_pickup_price,
            status=status,
            is_available=is_available,
        )

    def __hash__(self) -> int:
        return hash(self.id)
