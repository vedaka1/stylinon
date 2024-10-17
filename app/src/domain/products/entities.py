from dataclasses import dataclass, field
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
    INSTOCK = "in_stock"
    OUTOFSTOCK = "out_of_stock"


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
class Sku:
    id: UUID
    code: str
    retail_price: ProductPrice
    wholesale_delivery_price: ProductPrice
    d2_delivery_price: ProductPrice
    d2_self_pickup_price: ProductPrice
    d1_delivery_price: ProductPrice
    d1_self_pickup_price: ProductPrice
    status: ProductStatus

    @staticmethod
    def create(
        code: str,
        retail_price: int,
        wholesale_delivery_price: int,
        d2_delivery_price: int,
        d2_self_pickup_price: int,
        d1_delivery_price: int,
        d1_self_pickup_price: int,
        status: ProductStatus = ProductStatus.INSTOCK,
    ) -> "Sku":
        return Sku(
            id=uuid4(),
            code=code,
            retail_price=ProductPrice(retail_price),
            wholesale_delivery_price=ProductPrice(wholesale_delivery_price),
            d2_delivery_price=ProductPrice(d2_delivery_price),
            d2_self_pickup_price=ProductPrice(d2_self_pickup_price),
            d1_delivery_price=ProductPrice(d1_delivery_price),
            d1_self_pickup_price=ProductPrice(d1_self_pickup_price),
            status=status,
        )


@dataclass
class Product:
    id: UUID
    name: str
    category: str
    description: str
    units_of_measurement: UnitsOfMesaurement
    status: ProductStatus

    product_variants: list["ProductVariant"] = field(default_factory=list)

    @staticmethod
    def create(
        name: str,
        category: str,
        description: str,
        units_of_measurement: UnitsOfMesaurement = UnitsOfMesaurement.PIECE,
        *,
        status: ProductStatus = ProductStatus.INSTOCK,
    ) -> "Product":
        return Product(
            id=uuid4(),
            name=name,
            category=category,
            description=description,
            units_of_measurement=units_of_measurement,
            status=status,
        )

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass
class ProductVariant:
    id: UUID
    product_id: UUID
    name: str
    sku: str
    bag_weight: int
    pallet_weight: int
    bags_per_pallet: int
    retail_price: ProductPrice
    wholesale_delivery_price: ProductPrice
    d2_delivery_price: ProductPrice
    d2_self_pickup_price: ProductPrice
    d1_delivery_price: ProductPrice
    d1_self_pickup_price: ProductPrice
    image: str | None
    status: ProductStatus

    parent_product: Product | None = None

    @staticmethod
    def create(
        product_id: UUID,
        name: str,
        sku: str,
        bag_weight: int,
        pallet_weight: int,
        bags_per_pallet: int,
        retail_price: int,
        wholesale_delivery_price: int,
        d2_delivery_price: int,
        d2_self_pickup_price: int,
        d1_delivery_price: int,
        d1_self_pickup_price: int,
        image: str | None = "/images/no_image.png",
        status: ProductStatus = ProductStatus.INSTOCK,
    ) -> "ProductVariant":
        return ProductVariant(
            id=uuid4(),
            product_id=product_id,
            name=name,
            sku=sku,
            bag_weight=bag_weight,
            pallet_weight=pallet_weight,
            bags_per_pallet=bags_per_pallet,
            image=image,
            retail_price=ProductPrice(retail_price),
            wholesale_delivery_price=ProductPrice(wholesale_delivery_price),
            d2_delivery_price=ProductPrice(d2_delivery_price),
            d2_self_pickup_price=ProductPrice(d2_self_pickup_price),
            d1_delivery_price=ProductPrice(d1_delivery_price),
            d1_self_pickup_price=ProductPrice(d1_self_pickup_price),
            status=status,
        )

    def __hash__(self) -> int:
        return hash(self.id)
