from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from pytz import timezone
from src.domain.exceptions.order import OrderItemIncorrectQuantityException
from src.domain.products.entities import Product

tz_Moscow = timezone("Europe/Moscow")


class OrderStatus(Enum):
    CREATED = "CREATED"
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"


@dataclass
class Order:
    id: UUID
    user_email: str
    created_at: datetime
    updated_at: datetime
    shipping_address: str
    transaction_id: UUID
    tracking_number: str | None
    status: OrderStatus

    order_items: list["OrderItem"] = field(default_factory=list)

    @staticmethod
    def create(
        user_email: str,
        transaction_id: UUID,
        shipping_address: str,
        *,
        status: OrderStatus = OrderStatus.CREATED
    ) -> "Order":
        current_date = datetime.now(tz=tz_Moscow)
        return Order(
            id=uuid4(),
            user_email=user_email,
            created_at=current_date,
            updated_at=current_date,
            shipping_address=shipping_address,
            transaction_id=transaction_id,
            tracking_number=None,
            status=status,
        )


@dataclass
class OrderItem:
    order_id: UUID
    product_id: UUID
    quantity: int

    product: Product

    @staticmethod
    def create(
        order_id: UUID,
        product_id: UUID,
        quantity: int,
        product: Product,
    ) -> "OrderItem":
        if quantity <= 0:
            raise OrderItemIncorrectQuantityException
        return OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            product=product,
        )
