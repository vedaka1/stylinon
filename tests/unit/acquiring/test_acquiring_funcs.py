import pytest
from src.application.orders.utils import calculate_order_total_price
from src.application.products.dto import PaymentMethod, ProductInPaymentDTO
from src.domain.products.entities import UnitsOfMesaurement
from src.infrastructure.integrations.acquiring.mappers import (
    map_product_in_payment_to_dict,
)

test_products_params_1 = (
    [
        ProductInPaymentDTO(
            name='test_item1',
            amount=5678,
            quantity=1,
            payment_method=PaymentMethod.FULL_PAYMENT,
            measure=UnitsOfMesaurement.PIECE,
        ),
        ProductInPaymentDTO(
            name='test_item2',
            amount=1234,
            quantity=3,
            payment_method=PaymentMethod.FULL_PAYMENT,
            measure=UnitsOfMesaurement.PIECE,
        ),
    ],
    9380,
)
test_products_params_2 = (
    [
        ProductInPaymentDTO(
            name='test_item1',
            amount=5678,
            quantity=2,
            payment_method=PaymentMethod.FULL_PAYMENT,
            measure=UnitsOfMesaurement.PIECE,
        ),
    ],
    11356,
)


@pytest.mark.parametrize(
    'products,expected',
    (test_products_params_1, test_products_params_2),
)
async def test_success_calculate_order_total_price(
    products: tuple[ProductInPaymentDTO, ...],
    expected: int,
) -> None:
    total_price = calculate_order_total_price(products=products)
    assert total_price.value == expected


def test_map_product_in_payment_to_dict() -> None:
    item = ProductInPaymentDTO(
        name='test_item1',
        amount=5678,
        quantity=2,
        payment_method=PaymentMethod.FULL_PAYMENT,
        measure=UnitsOfMesaurement.PIECE,
    )
    result = map_product_in_payment_to_dict(item=item)
    expected = {
        'name': 'test_item1',
        'amount': 56.78,
        'quantity': 2,
        'paymentMethod': PaymentMethod.FULL_PAYMENT.value,
        'measure': UnitsOfMesaurement.PIECE.value,
    }
    assert result == expected
