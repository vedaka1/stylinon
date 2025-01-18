from typing import TYPE_CHECKING
from uuid import UUID

from fastapi import Request
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.application.common.utils import parse_price
from src.domain.products.entities import (
    Category,
    Product,
    ProductStatus,
    UnitsOfMesaurement,
)
from src.domain.products.value_objects import ProductPrice
from src.infrastructure.persistence.postgresql.models.base import Base

if TYPE_CHECKING:
    pass


class CategoryModel(Base):
    __tablename__ = 'categories'

    name: Mapped[str] = mapped_column(primary_key=True)
    is_available: Mapped[bool] = mapped_column(nullable=False)


def map_to_category(entity: CategoryModel) -> Category:
    category = Category(name=entity.name, is_available=entity.is_available)

    return category


class ProductModel(Base):
    __tablename__ = 'products'

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    category: Mapped[str] = mapped_column(ForeignKey('categories.name', ondelete='CASCADE'), nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    collection: Mapped[str | None] = mapped_column(nullable=True)
    size: Mapped[str | None] = mapped_column(nullable=True)
    sku: Mapped[str] = mapped_column(nullable=False, unique=True)
    weight: Mapped[int] = mapped_column(nullable=True)
    retail_price: Mapped[int] = mapped_column(nullable=False)
    wholesale_price: Mapped[int | None] = mapped_column(nullable=True)
    d1_delivery_price: Mapped[int | None] = mapped_column(nullable=True)
    d1_self_pickup_price: Mapped[int | None] = mapped_column(nullable=True)
    units_of_measurement: Mapped[UnitsOfMesaurement] = mapped_column(nullable=False)
    image: Mapped[str] = mapped_column(nullable=False, default='/images/not_found.jpg')
    status: Mapped[ProductStatus] = mapped_column(nullable=False)
    is_available: Mapped[bool] = mapped_column(nullable=False, default=True)

    product_category: Mapped['CategoryModel'] = relationship()

    def __admin_repr__(self, request: Request) -> str:
        return f'{self.name}'

    def __repr__(self) -> str:
        return f'ProductModel({self.__dict__})'


def map_to_product(entity: ProductModel) -> Product:
    product = Product(
        id=entity.id,
        name=entity.name,
        category=entity.category,
        description=entity.description,
        collection=entity.collection,
        size=entity.size,
        sku=entity.sku,
        weight=entity.weight,
        retail_price=ProductPrice(entity.retail_price),
        wholesale_price=parse_price(entity.wholesale_price),
        d1_delivery_price=parse_price(entity.d1_delivery_price),
        d1_self_pickup_price=parse_price(entity.d1_self_pickup_price),
        units_of_measurement=entity.units_of_measurement,
        image=entity.image,
        status=entity.status,
        is_available=entity.is_available,
    )

    return product
