from dataclasses import dataclass, field
from enum import Enum
from uuid import UUID

from src.application.common.utils import convert_price
from src.domain.products.entities import ProductStatus, UnitsOfMesaurement
from src.domain.products.value_objects import ProductPrice


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
    # DELAYED_PAYMENT = "delayed_payment"


class PaymentObject(Enum):
    GOODS = "goods"
    SERVICE = "service"
    WORK = "work"


@dataclass
class ProductOut:
    id: UUID
    name: str
    category: str
    collection: str | None
    size: str | None
    description: str
    sku: str
    weight: int | None
    retail_price: float
    wholesale_price: float | None
    d1_delivery_price: float | None
    d1_self_pickup_price: float | None
    units_of_measurement: UnitsOfMesaurement
    image: str | None
    status: ProductStatus
    is_available: bool

    def __init__(
        self,
        id: UUID,
        name: str,
        sku: str,
        category: str,
        description: str,
        units_of_measurement: UnitsOfMesaurement,
        retail_price: ProductPrice,
        status: ProductStatus,
        is_available: bool,
        weight: int | None = None,
        wholesale_price: ProductPrice | None = None,
        d1_delivery_price: ProductPrice | None = None,
        d1_self_pickup_price: ProductPrice | None = None,
        collection: str | None = None,
        size: str | None = None,
        image: str | None = None,
    ) -> None:
        self.id = id
        self.name = name
        self.category = category
        self.description = description
        self.sku = sku
        self.weight = weight
        self.retail_price = retail_price.in_rubles()
        self.wholesale_price = convert_price(wholesale_price)
        self.d1_delivery_price = convert_price(d1_delivery_price)
        self.d1_self_pickup_price = convert_price(d1_self_pickup_price)
        self.image = image
        self.units_of_measurement = units_of_measurement
        self.status = status
        self.is_available = is_available
        self.collection = collection
        self.size = size


@dataclass
class ProductInPaymentDTO:
    name: str
    amount: int
    quantity: int
    vat_type: VatType | None = None
    payment_object: PaymentObject | None = None
    payment_method: PaymentMethod | None = None
    measure: UnitsOfMesaurement = field(default=UnitsOfMesaurement.PIECE)
