from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from src.application.common.utils import convert_price
from src.domain.orders.entities import OrderStatus
from src.domain.orders.exceptions import OrderItemIncorrectQuantityException
from src.domain.products.entities import ProductStatus, UnitsOfMesaurement
from src.domain.products.value_objects import ProductPrice


@dataclass
class ProductInOrder:
    id: UUID
    quantity: int

    def __post_init__(self) -> None:
        if self.quantity < 1:
            raise OrderItemIncorrectQuantityException


@dataclass
class OrderOut:
    id: UUID
    customer_email: str
    created_at: datetime
    updated_at: datetime
    shipping_address: str
    operation_id: UUID
    tracking_number: str | None
    total_price: float
    is_self_pickup: bool
    status: OrderStatus
    items: list["OrderItemOut"] = field(default_factory=list)

    def __init__(
        self,
        id: UUID,
        customer_email: str,
        created_at: datetime,
        updated_at: datetime,
        shipping_address: str,
        operation_id: UUID,
        tracking_number: str | None,
        total_price: int,
        is_self_pickup: bool,
        status: OrderStatus,
        items: list["OrderItemOut"] = field(default_factory=list),
    ) -> None:
        self.id = id
        self.customer_email = customer_email
        self.created_at = created_at
        self.updated_at = updated_at
        self.shipping_address = shipping_address
        self.operation_id = operation_id
        self.tracking_number = tracking_number
        self.total_price = ProductPrice(total_price).in_rubles()
        self.is_self_pickup = is_self_pickup
        self.status = status
        self.items = items


@dataclass
class OrderItemOut:
    product_id: UUID
    name: str
    category: str
    description: str
    units_of_measurement: UnitsOfMesaurement
    quantity: int
    product_name: str
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
    status: ProductStatus
    image: str | None = None

    def __init__(
        self,
        product_id: UUID,
        name: str,
        category: str,
        description: str,
        units_of_measurement: UnitsOfMesaurement,
        quantity: int,
        product_name: str,
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
        self.product_id = product_id
        self.name = name
        self.category = category
        self.description = description
        self.units_of_measurement = units_of_measurement
        self.quantity = quantity
        self.product_name = product_name
        self.sku = sku
        self.bag_weight = bag_weight
        self.pallet_weight = pallet_weight
        self.bags_per_pallet = bags_per_pallet
        self.image = image
        self.retail_price = retail_price.in_rubles()
        self.wholesale_delivery_price = convert_price(wholesale_delivery_price)
        self.d2_delivery_price = convert_price(d2_delivery_price)
        self.d2_self_pickup_price = convert_price(d2_self_pickup_price)
        self.d1_delivery_price = convert_price(d1_delivery_price)
        self.d1_self_pickup_price = convert_price(d1_self_pickup_price)
        self.status = status
        self.image = image


@dataclass
class CreateOrderOut:
    id: UUID
    customer_email: str
    created_at: datetime
    payment_link: str
    shipping_address: str
    operation_id: UUID
    total_price: float
    status: OrderStatus
