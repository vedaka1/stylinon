from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.domain.products.entities import Product
from src.infrastructure.persistence.postgresql.models.base import Base

if TYPE_CHECKING:
    from src.infrastructure.persistence.postgresql.models.order import (
        OrderItemModel,
        OrderModel,
    )


class ProductModel(Base):
    __tablename__ = "products"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    category: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    units_of_measurement: Mapped[str] = mapped_column(nullable=False)

    order_item: Mapped["OrderItemModel"] = relationship(
        back_populates="product",
    )

    def __repr__(self) -> str:
        return f"ProductModel({self.__dict__})"


def map_to_product(entity: ProductModel) -> Product:
    return Product(
        id=entity.id,
        name=entity.name,
        category=entity.category,
        description=entity.description,
        price=entity.price,
        units_of_measurement=entity.units_of_measurement,
    )
