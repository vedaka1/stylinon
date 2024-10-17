from uuid import uuid4

import pytest
from src.application.orders.dto import ProductInOrder
from src.application.products.dto import PaymentMethod, ProductInPaymentDTO
from src.domain.orders.exceptions import OrderItemIncorrectQuantityException
from src.domain.products.entities import (
    ProductStatus,
    ProductVariant,
    UnitsOfMesaurement,
)
from src.domain.products.exceptions import ProductIncorrectPriceException


def test_success_create_product() -> None:
    product_variant = ProductVariant.create(
        product_id=uuid4(),
        name="test_product_variant",
        sku="test_sku",
        bag_weight=10,
        pallet_weight=100,
        bags_per_pallet=10,
        retail_price=100,
        wholesale_delivery_price=100,
        d2_delivery_price=100,
        d2_self_pickup_price=100,
        d1_delivery_price=100,
        d1_self_pickup_price=100,
        status=ProductStatus.INSTOCK,
    )
    assert product_variant.name == "test_product_variant"
    assert product_variant.sku == "test_sku"
    assert product_variant.bag_weight == 10
    assert product_variant.pallet_weight == 100
    assert product_variant.bags_per_pallet == 10
    assert product_variant.retail_price.value == 100
    assert product_variant.wholesale_delivery_price.value == 100
    assert product_variant.d2_delivery_price.value == 100
    assert product_variant.d2_self_pickup_price.value == 100
    assert product_variant.d1_delivery_price.value == 100
    assert product_variant.d1_self_pickup_price.value == 100
    assert product_variant.status == ProductStatus.INSTOCK


def test_fail_create_product_variant_with_incorrect_price() -> None:
    with pytest.raises(ProductIncorrectPriceException):
        ProductVariant.create(
            product_id=uuid4(),
            name="test_product_variant",
            sku="test_sku",
            bag_weight=10,
            pallet_weight=100,
            bags_per_pallet=10,
            retail_price=0,
            wholesale_delivery_price=100,
            d2_delivery_price=100,
            d2_self_pickup_price=100,
            d1_delivery_price=100,
            d1_self_pickup_price=100,
            status=ProductStatus.INSTOCK,
        )


def test_success_create_product_in_payment_dto() -> None:
    product_in_payment = ProductInPaymentDTO(
        name="test_item",
        amount=999,
        quantity=1,
        payment_method=PaymentMethod.FULL_PAYMENT,
        measure=UnitsOfMesaurement.PIECE,
    )
    assert product_in_payment.name == "test_item"
    assert product_in_payment.amount == 999
    assert product_in_payment.quantity == 1
    assert product_in_payment.payment_method == PaymentMethod.FULL_PAYMENT
    assert product_in_payment.measure == UnitsOfMesaurement.PIECE


def test_fail_create_product_in_order_with_incorrect_quantity() -> None:
    with pytest.raises(OrderItemIncorrectQuantityException):
        ProductInOrder(id=uuid4(), quantity=0)
