from dataclasses import dataclass
from datetime import date
from uuid import UUID

from pydantic import EmailStr
from src.domain.orders.entities import OrderStatus


@dataclass
class GetManyOrdersCommand:
    date_from: date | None = None
    date_to: date | None = None
    status: OrderStatus | None = None


@dataclass
class ProductInOrder:
    id: UUID
    quantity: int


@dataclass
class CreateOrderCommand:
    customer_email: EmailStr
    shipping_address: str
    items: list[ProductInOrder]


@dataclass
class UpdateOrderCommand:
    order_id: UUID
    shipping_address: str | None = None
    tracking_number: str | None = None
    status: OrderStatus | None = None
