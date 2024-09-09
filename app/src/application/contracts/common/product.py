from dataclasses import dataclass, field
from enum import Enum

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
class ProductInPayment:
    name: str
    amount: int
    quantity: int
    vat_type: VatType | None = None
    payment_object: PaymentObject | None = None
    payment_method: PaymentMethod | None = None
    measure: UnitsOfMesaurement = field(default=UnitsOfMesaurement.PIECES)
