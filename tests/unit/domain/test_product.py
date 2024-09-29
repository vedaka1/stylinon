import pytest
from src.application.products.dto import PaymentMethod, ProductInPaymentDTO
from src.domain.orders.exceptions import OrderItemIncorrectQuantityException
from src.domain.products.entities import Product, UnitsOfMesaurement
from src.domain.products.exceptions import ProductIncorrectPriceException
from src.domain.products.value_objects import ProductPrice


def test_success_create_product() -> None:
    product = Product.create(
        name="Test Product",
        category="Test Category",
        description="This is a test product",
        price=900,
        units_of_measurement=UnitsOfMesaurement.PIECES,
    )
    assert product.name == "Test Product"
    assert product.category == "Test Category"
    assert product.description == "This is a test product"
    assert product.price == ProductPrice(900)
    assert product.units_of_measurement == UnitsOfMesaurement.PIECES


def test_fail_create_product_with_incorrect_price() -> None:
    with pytest.raises(ProductIncorrectPriceException):
        Product.create(
            name="Test Product",
            category="Test Category",
            description="This is a test product",
            price=0,
            units_of_measurement=UnitsOfMesaurement.PIECES,
        )


def test_success_create_product_in_payment_dto() -> None:
    product_in_payment = ProductInPaymentDTO(
        name="test_item",
        amount=999,
        quantity=1,
        payment_method=PaymentMethod.FULL_PAYMENT,
        measure=UnitsOfMesaurement.PIECES,
    )
    assert product_in_payment.name == "test_item"
    assert product_in_payment.amount == 999
    assert product_in_payment.quantity == 1
    assert product_in_payment.payment_method == PaymentMethod.FULL_PAYMENT
    assert product_in_payment.measure == UnitsOfMesaurement.PIECES


def test_fail_create_product_in_payment_dto_with_incorrect_quantity() -> None:
    with pytest.raises(OrderItemIncorrectQuantityException):
        ProductInPaymentDTO(
            name="test_item",
            amount=1,
            quantity=0,
            payment_method=PaymentMethod.FULL_PAYMENT,
            measure=UnitsOfMesaurement.PIECES,
        )
