from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from src.domain.orders.exceptions import OrderItemIncorrectQuantityException
from src.domain.products.entities import Product
from src.domain.products.value_objects import ProductPrice


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
    customer_email: str
    created_at: datetime
    updated_at: datetime
    shipping_address: str
    operation_id: UUID
    tracking_number: str | None
    total_price: int
    is_self_pickup: bool
    status: OrderStatus

    items: list['OrderItem'] = field(default_factory=list)

    @staticmethod
    def create(
        customer_email: str,
        operation_id: UUID,
        shipping_address: str,
        total_price: int,
        is_self_pickup: bool,
        *,
        status: OrderStatus = OrderStatus.CREATED,
    ) -> 'Order':
        current_date = datetime.now()
        return Order(
            id=uuid4(),
            customer_email=customer_email,
            created_at=current_date,
            updated_at=current_date,
            shipping_address=shipping_address,
            operation_id=operation_id,
            tracking_number=None,
            total_price=total_price,
            is_self_pickup=is_self_pickup,
            status=status,
        )


@dataclass
class OrderItem:
    order_id: UUID
    product_id: UUID
    quantity: int
    price: ProductPrice

    product: Product | None

    @staticmethod
    def create(order_id: UUID, product_id: UUID, quantity: int, price: ProductPrice) -> 'OrderItem':
        if quantity <= 0:
            raise OrderItemIncorrectQuantityException
        return OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            price=price,
            product=None,
        )
