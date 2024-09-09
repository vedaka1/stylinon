from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from src.domain.exceptions.order import OrderItemIncorrectQuantityException
from src.domain.products.entities import Product


# fmt: off
class OrderStatus(str, Enum):
    CREATED = "CREATED"         # Заказ создан и ожидает оплаты
    APPROVED = "APPROVED"       # Заказ оплачен
    PROCESSING = "PROCESSING"   # Заказ в обработке
    SHIPPED = "SHIPPED"         # Заказ отправлен
    COMPLETED = "COMPLETED"     # Заказ доставлен
    CANCELLED = "CANCELLED"     # Заказ отменен
    FAILED = "FAILED"           # Заказ не выполнен
# fmt: on


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

    items: list["OrderItem"] = field(default_factory=list)

    @staticmethod
    def create(
        user_email: str,
        transaction_id: UUID,
        shipping_address: str,
        *,
        status: OrderStatus = OrderStatus.CREATED,
    ) -> "Order":
        current_date = datetime.now()
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

    product: Product | None

    @staticmethod
    def create(
        order_id: UUID,
        product_id: UUID,
        quantity: int,
        product: Product | None = None,
    ) -> "OrderItem":
        if quantity <= 0:
            raise OrderItemIncorrectQuantityException
        return OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            product=product,
        )
