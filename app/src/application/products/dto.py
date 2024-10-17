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
    DELAYED_PAYMENT = "delayed_payment"


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
    sku: str
    bag_weight: float
    pallet_weight: float
    bags_per_pallet: float
    retail_price: float
    wholesale_delivery_price: float | None
    d2_delivery_price: float | None
    d2_self_pickup_price: float | None
    d1_delivery_price: float | None
    d1_self_pickup_price: float | None
    units_of_measurement: UnitsOfMesaurement
    image: str | None
    status: ProductStatus

    def __init__(
        self,
        id: UUID,
        name: str,
        category: str,
        description: str,
        units_of_measurement: UnitsOfMesaurement,
        sku: str,
        bag_weight: float,
        pallet_weight: float,
        bags_per_pallet: float,
        retail_price: ProductPrice,
        wholesale_delivery_price: ProductPrice | None,
        d2_delivery_price: ProductPrice | None,
        d2_self_pickup_price: ProductPrice | None,
        d1_delivery_price: ProductPrice | None,
        d1_self_pickup_price: ProductPrice | None,
        status: ProductStatus,
        image: str | None = None,
    ) -> None:
        self.id = id
        self.name = name
        self.category = category
        self.description = description
        self.sku = sku
        self.bag_weight = bag_weight
        self.pallet_weight = pallet_weight
        self.bags_per_pallet = bags_per_pallet
        self.retail_price = retail_price.in_rubles()
        self.wholesale_delivery_price = convert_price(wholesale_delivery_price)
        self.d2_delivery_price = convert_price(d2_delivery_price)
        self.d2_self_pickup_price = convert_price(d2_self_pickup_price)
        self.d1_delivery_price = convert_price(d1_delivery_price)
        self.d1_self_pickup_price = convert_price(d1_self_pickup_price)
        self.image = image
        self.units_of_measurement = units_of_measurement
        self.status = status


@dataclass
class ProductInPaymentDTO:
    name: str
    amount: int
    quantity: int
    vat_type: VatType | None = None
    payment_object: PaymentObject | None = None
    payment_method: PaymentMethod | None = None
    measure: UnitsOfMesaurement = field(default=UnitsOfMesaurement.PIECE)
