from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.domain.products.entities import (
    Category,
    Product,
    ProductStatus,
    ProductVariant,
    UnitsOfMesaurement,
)
from src.domain.products.value_objects import ProductPrice
from src.infrastructure.persistence.postgresql.models.base import Base

if TYPE_CHECKING:
    from src.infrastructure.persistence.postgresql.models.order import OrderItemModel


class CategoryModel(Base):

    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(primary_key=True)
    is_available: Mapped[bool] = mapped_column(nullable=False)


def map_to_category(entity: CategoryModel) -> Category:
    category = Category(
        name=entity.name,
        is_available=entity.is_available,
    )

    return category


# class SkuModel(Base):

#     __tablename__ = "sku"

#     id: Mapped[UUID] = mapped_column(primary_key=True, index=True)
#     code: Mapped[str] = mapped_column(nullable=False)
#     retail_price: Mapped[int] = mapped_column(nullable=False)
#     wholesale_delivery_price: Mapped[int] = mapped_column(nullable=False)
#     d2_delivery_price: Mapped[int] = mapped_column(nullable=False)
#     d2_self_pickup_price: Mapped[int] = mapped_column(nullable=False)
#     d1_delivery_price: Mapped[int] = mapped_column(nullable=False)
#     d1_self_pickup_price: Mapped[int] = mapped_column(nullable=False)
#     status: Mapped[ProductStatus] = mapped_column(nullable=False)

#     sku_product: Mapped["ProductVariantModel"] = relationship(
#         back_populates="product_sku"
#     )


# def map_to_sku(entity: SkuModel) -> Sku:
#     sku = Sku(
#         id=entity.id,
#         code=entity.code,
#         retail_price=ProductPrice(entity.retail_price),
#         wholesale_delivery_price=ProductPrice(entity.wholesale_delivery_price),
#         d2_delivery_price=ProductPrice(entity.d2_delivery_price),
#         d2_self_pickup_price=ProductPrice(entity.d2_self_pickup_price),
#         d1_delivery_price=ProductPrice(entity.d1_delivery_price),
#         d1_self_pickup_price=ProductPrice(entity.d1_self_pickup_price),
#         status=entity.status,
#     )

#     return sku


class ProductModel(Base):

    __tablename__ = "products"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    category: Mapped[str] = mapped_column(
        ForeignKey("categories.name", ondelete="CASCADE"),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(nullable=False)
    units_of_measurement: Mapped[UnitsOfMesaurement] = mapped_column(nullable=False)
    status: Mapped[ProductStatus] = mapped_column(nullable=False)

    variants: Mapped[list["ProductVariantModel"]] = relationship(
        back_populates="parent_product",
    )

    def __repr__(self) -> str:
        return f"ProductModel({self.__dict__})"


def map_to_product(entity: ProductModel, with_relations: bool = False) -> Product:
    product = Product(
        id=entity.id,
        name=entity.name,
        category=entity.category,
        description=entity.description,
        units_of_measurement=entity.units_of_measurement,
        status=entity.status,
    )
    if with_relations:
        product.product_variants = [
            map_to_product_variant(variant) for variant in entity.variants
        ]
    return product


class ProductVariantModel(Base):

    __tablename__ = "product_variants"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(nullable=False)
    sku: Mapped[str] = mapped_column(nullable=False, unique=True)
    bag_weight: Mapped[int] = mapped_column(nullable=False)
    pallet_weight: Mapped[int] = mapped_column(nullable=False)
    bags_per_pallet: Mapped[int] = mapped_column(nullable=False)
    retail_price: Mapped[int] = mapped_column(nullable=False)
    wholesale_delivery_price: Mapped[int] = mapped_column(nullable=False)
    d2_delivery_price: Mapped[int] = mapped_column(nullable=False)
    d2_self_pickup_price: Mapped[int] = mapped_column(nullable=False)
    d1_delivery_price: Mapped[int] = mapped_column(nullable=False)
    d1_self_pickup_price: Mapped[int] = mapped_column(nullable=False)
    image: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[ProductStatus] = mapped_column(nullable=False)

    parent_product: Mapped["ProductModel"] = relationship(
        back_populates="variants",
    )
    order_item: Mapped["OrderItemModel"] = relationship(
        back_populates="order_product",
    )


def map_to_product_variant(
    entity: ProductVariantModel,
    with_relations: bool = False,
) -> ProductVariant:
    product_variant = ProductVariant(
        id=entity.id,
        product_id=entity.product_id,
        name=entity.name,
        sku=entity.sku,
        bag_weight=entity.bag_weight,
        pallet_weight=entity.pallet_weight,
        bags_per_pallet=entity.bags_per_pallet,
        retail_price=ProductPrice(entity.retail_price),
        wholesale_delivery_price=ProductPrice(entity.wholesale_delivery_price),
        d2_delivery_price=ProductPrice(entity.d2_delivery_price),
        d2_self_pickup_price=ProductPrice(entity.d2_self_pickup_price),
        d1_delivery_price=ProductPrice(entity.d1_delivery_price),
        d1_self_pickup_price=ProductPrice(entity.d1_self_pickup_price),
        image=entity.image,
        status=entity.status,
    )

    if with_relations:
        product_variant.parent_product = map_to_product(entity.parent_product)

    return product_variant
