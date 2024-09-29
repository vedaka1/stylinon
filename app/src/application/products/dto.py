from dataclasses import dataclass, field
from enum import Enum
from uuid import UUID

from src.domain.orders.exceptions import OrderItemIncorrectQuantityException
from src.domain.products.entities import UnitsOfMesaurement


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
    price: int  # в копейках
    units_of_measurement: UnitsOfMesaurement
    photo_url: str | None = None


@dataclass
class ProductInPaymentDTO:
    name: str
    amount: int
    quantity: int
    vat_type: VatType | None = None
    payment_object: PaymentObject | None = None
    payment_method: PaymentMethod | None = None
    measure: UnitsOfMesaurement = field(default=UnitsOfMesaurement.PIECES)

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise OrderItemIncorrectQuantityException
