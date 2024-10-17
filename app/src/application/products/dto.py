from dataclasses import dataclass, field
from enum import Enum
from uuid import UUID

from src.domain.products.entities import ProductStatus, UnitsOfMesaurement


class VatType(Enum):
    NONE = "none"
    VAT0 = "vat0"
    VAT10 = "vat10"
    VAT20 = "vat20"
    VAT110 = "vat110"
    VAT120 = "vat120"


class PaymentMethod(Enum):
    FULL_PAYMENT = "full_payment"
    FULL_PREPAYMENT = "full_prepayment"
    DELAYED_PAYMENT = "delayed_payment"


class PaymentObject(Enum):
    GOODS = "goods"
    SERVICE = "service"
    WORK = "work"


@dataclass
class ProductWithoutVariantsOut:
    id: UUID
    name: str
    category: str
    description: str
    units_of_measurement: UnitsOfMesaurement


@dataclass
class ProductVariantOut:
    id: UUID
    name: str
    sku: str
    bag_weight: float
    pallet_weight: float
    bags_per_pallet: float
    retail_price: float
    wholesale_delivery_price: float
    d2_delivery_price: float
    d2_self_pickup_price: float
    d1_delivery_price: float
    d1_self_pickup_price: float
    image: str | None
    status: ProductStatus

    parent_product: "ProductWithoutVariantsOut | None" = None


@dataclass
class ProductOut:
    id: UUID
    name: str
    category: str
    description: str
    units_of_measurement: UnitsOfMesaurement

    variants: list[ProductVariantOut]


@dataclass
class ProductInPaymentDTO:
    name: str
    amount: int
    quantity: int
    vat_type: VatType | None = None
    payment_object: PaymentObject | None = None
    payment_method: PaymentMethod | None = None
    measure: UnitsOfMesaurement = field(default=UnitsOfMesaurement.PIECE)
