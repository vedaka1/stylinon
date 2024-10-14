from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from src.domain.orders.entities import OrderStatus
from src.domain.orders.exceptions import OrderItemIncorrectQuantityException
from src.domain.products.entities import UnitsOfMesaurement
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
        self.status = status
        self.items = items


@dataclass
class OrderItemOut:
    product_id: UUID
    name: str
    category: str
    description: str
    price: float
    units_of_measurement: UnitsOfMesaurement
    quantity: int
    photo_url: str | None = None

    def __init__(
        self,
        product_id: UUID,
        name: str,
        category: str,
        description: str,
        price: int,
        units_of_measurement: UnitsOfMesaurement,
        quantity: int,
        photo_url: str | None = None,
    ) -> None:
        self.product_id = product_id
        self.name = name
        self.category = category
        self.description = description
        self.price = ProductPrice(price).in_rubles()
        self.units_of_measurement = units_of_measurement
        self.quantity = quantity
        self.photo_url = photo_url


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
