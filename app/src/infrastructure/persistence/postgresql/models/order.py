from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.domain.orders.entities import Order, OrderItem, OrderStatus
from src.infrastructure.persistence.postgresql.models.base import Base
from src.infrastructure.persistence.postgresql.models.product import map_to_product

if TYPE_CHECKING:
    from src.infrastructure.persistence.postgresql.models.product import ProductModel


class OrderModel(Base):
    __tablename__ = "orders"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True)
    user_email: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
    )
    shipping_address: Mapped[str] = mapped_column(nullable=False)
    transaction_id: Mapped[UUID] = mapped_column(nullable=False)
    tracking_number: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[OrderStatus] = mapped_column(nullable=False)

    order_items: Mapped[list["OrderItemModel"]] = relationship(
        back_populates="order",
    )

    def __repr__(self) -> str:
        return f"OrderModel({self.__dict__})"


def map_to_order(entity: OrderModel, with_products: bool = False) -> Order:
    order = Order(
        id=entity.id,
        user_email=entity.user_email,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
        shipping_address=entity.shipping_address,
        transaction_id=entity.transaction_id,
        tracking_number=entity.tracking_number,
        status=entity.status,
    )
    if with_products:
        order.items = [
            map_to_order_item(order_item) for order_item in entity.order_items
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

    order: Mapped["OrderModel"] = relationship(
        back_populates="order_items",
    )

    product: Mapped["ProductModel"] = relationship(
        back_populates="order_item",
    )

    def __repr__(self) -> str:
        return f"OrderItemModel({self.__dict__})"


def map_to_order_item(entity: OrderItemModel, with_product: bool = False) -> OrderItem:
    order_item = OrderItem(
        order_id=entity.order_id,
        product_id=entity.product_id,
        quantity=entity.quantity,
        product=map_to_product(entity.product),
    )
    if with_product:
        order_item.product = map_to_product(entity.product)
    return order_item
