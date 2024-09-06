from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from src.domain.orders.entities import OrderStatus
from src.domain.products.entities import UnitsOfMesaurement


@dataclass
class OrderOut:
    id: UUID
    user_email: str
    created_at: datetime
    updated_at: datetime
    shipping_address: str
    transaction_id: UUID
    tracking_number: str | None
    status: OrderStatus
    items: list["OrderItemOut"] = field(default_factory=list)


@dataclass
class OrderItemOut:
    name: str
    category: str
    description: str
    price: int
    quantity: int
    units_of_measurement: UnitsOfMesaurement
