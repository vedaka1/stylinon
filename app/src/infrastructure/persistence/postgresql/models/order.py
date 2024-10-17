from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.domain.orders.entities import Order, OrderItem, OrderStatus
from src.domain.products.value_objects import ProductPrice
from src.infrastructure.persistence.postgresql.models.base import Base
from src.infrastructure.persistence.postgresql.models.product import map_to_product

if TYPE_CHECKING:
    from src.infrastructure.persistence.postgresql.models.product import ProductModel


class OrderModel(Base):
    __tablename__ = "orders"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True)
    customer_email: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False),
        nullable=False,
    )
    shipping_address: Mapped[str] = mapped_column(nullable=False)
    operation_id: Mapped[UUID] = mapped_column(nullable=False)
    tracking_number: Mapped[str] = mapped_column(nullable=True)
    total_price: Mapped[int] = mapped_column(nullable=False)
    is_self_pickup: Mapped[bool] = mapped_column(nullable=False)
    status: Mapped[OrderStatus] = mapped_column(nullable=False)

    order_items: Mapped[list["OrderItemModel"]] = relationship(
        back_populates="order",
    )

    def __str__(self) -> str:
        return f"Почта клиента: {self.customer_email}\nСоздан: {self.created_at}\nОбновлен: {self.updated_at}\n"

    def __repr__(self) -> str:
        return f"OrderModel({self.__dict__})"


def map_to_order(entity: OrderModel, with_relations: bool = False) -> Order:
    order = Order(
        id=entity.id,
        customer_email=entity.customer_email,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
        shipping_address=entity.shipping_address,
        operation_id=entity.operation_id,
        tracking_number=entity.tracking_number,
        total_price=entity.total_price,
        status=entity.status,
        is_self_pickup=entity.is_self_pickup,
    )
    if with_relations:
        order.items = [
            map_to_order_item(order_item, with_relations=with_relations)
            for order_item in entity.order_items
        ]
    return order


class OrderItemModel(Base):
    __tablename__ = "order_items"

    order_id: Mapped[UUID] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    quantity: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)

    order: Mapped["OrderModel"] = relationship(
        back_populates="order_items",
    )

    order_product: Mapped["ProductModel"] = relationship()

    def __str__(self) -> str:
        return f"Order ID: {self.order_id}\nProduct ID: {self.product_id}\nQuantity: {self.quantity}\n"

    def __repr__(self) -> str:
        return f"OrderItemModel: {self.__dict__})"


def map_to_order_item(
    entity: OrderItemModel,
    with_relations: bool = True,
) -> OrderItem:
    order_item = OrderItem(
        order_id=entity.order_id,
        product_id=entity.product_id,
        quantity=entity.quantity,
        price=ProductPrice(entity.price),
        product=None,
    )

    if with_relations:
        order_item.product = map_to_product(entity.order_product)

    return order_item
