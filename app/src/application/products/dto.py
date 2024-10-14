from dataclasses import dataclass, field
from enum import Enum
from uuid import UUID

from src.domain.products.entities import UnitsOfMesaurement
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


class PaymentObject(Enum):
    GOODS = "goods"
    SERVICE = "service"
    WORK = "work"


@dataclass
class ProductOut:
    id: UUID
    name: str
    category: str
    description: str
    price: float
    units_of_measurement: UnitsOfMesaurement
    photo_url: str | None = None

    def __init__(
        self,
        id: UUID,
        name: str,
        category: str,
        description: str,
        price: int,
        units_of_measurement: UnitsOfMesaurement,
        photo_url: str | None = None,
    ) -> None:
        self.id = id
        self.name = name
        self.category = category
        self.description = description
        self.price = ProductPrice(price).in_rubles()
        self.units_of_measurement = units_of_measurement
        self.photo_url = photo_url


@dataclass
class ProductInPaymentDTO:
    name: str
    amount: int
    quantity: int
    vat_type: VatType | None = None
    payment_object: PaymentObject | None = None
    payment_method: PaymentMethod | None = None
    measure: UnitsOfMesaurement = field(default=UnitsOfMesaurement.PIECE)
