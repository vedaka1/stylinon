from dataclasses import dataclass
from datetime import date

from pydantic import EmailStr
from src.application.orders.dto import ProductInOrder
from src.application.products.dto import PaymentMethod
from src.domain.orders.entities import OrderStatus


@dataclass
class GetManyOrdersCommand:
    date_from: date | None = None
    date_to: date | None = None
    status: OrderStatus | None = None


@dataclass
class CreateOrderCommand:
    customer_email: EmailStr
    shipping_address: str
    is_self_pickup: bool
    items: list[ProductInOrder]
    payment_method: PaymentMethod = PaymentMethod.FULL_PREPAYMENT


@dataclass
class UpdateOrderCommand:
    shipping_address: str | None = None
    tracking_number: str | None = None
    status: OrderStatus | None = None
