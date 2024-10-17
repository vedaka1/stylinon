from uuid import uuid4

import pytest
from src.application.orders.dto import ProductInOrder
from src.application.products.dto import PaymentMethod, ProductInPaymentDTO
from src.domain.orders.exceptions import OrderItemIncorrectQuantityException
from src.domain.products.entities import Product, ProductStatus, UnitsOfMesaurement
from src.domain.products.exceptions import ProductIncorrectPriceException
from src.domain.products.value_objects import ProductPrice


def test_success_create_product() -> None:
    product = Product.create(
        category="test_category",
        description="test_description",
        name="test_product_variant",
        sku="test_sku",
        bag_weight=10,
        pallet_weight=100,
        bags_per_pallet=10,
        retail_price=ProductPrice(100),
        status=ProductStatus.INSTOCK,
    )

    assert product.name == "test_product_variant"
    assert product.sku == "test_sku"
    assert product.bag_weight == 10
    assert product.pallet_weight == 100
    assert product.bags_per_pallet == 10
    assert product.retail_price.value == 100
    assert product.wholesale_delivery_price == None
    assert product.d2_delivery_price == None
    assert product.d2_self_pickup_price == None
    assert product.d1_delivery_price == None
    assert product.d1_self_pickup_price == None
    assert product.status == ProductStatus.INSTOCK


def test_fail_create_product_variant_with_incorrect_price() -> None:
    with pytest.raises(ProductIncorrectPriceException):
        Product.create(
            category="test_category",
            description="test_description",
            name="test_product_variant",
            sku="test_sku",
            bag_weight=10,
            pallet_weight=100,
            bags_per_pallet=10,
            retail_price=ProductPrice(0),
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
