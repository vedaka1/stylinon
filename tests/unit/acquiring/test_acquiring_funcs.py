import pytest
from src.application.acquiring.interface import AcquiringGatewayInterface
from src.application.products.dto import PaymentMethod, ProductInPaymentDTO
from src.domain.products.entities import UnitsOfMesaurement
from src.infrastructure.acquiring.mappers import map_product_in_payment_to_dict

test_products_params_1 = (
    [
        ProductInPaymentDTO(
            name="test_item1",
            amount=5678,
            quantity=1,
            payment_method=PaymentMethod.FULL_PAYMENT,
            measure=UnitsOfMesaurement.PIECES,
        ),
        ProductInPaymentDTO(
            name="test_item2",
            amount=1234,
            quantity=3,
            payment_method=PaymentMethod.FULL_PAYMENT,
            measure=UnitsOfMesaurement.PIECES,
        ),
    ],
    9380,
)
test_products_params_2 = (
    [
        ProductInPaymentDTO(
            name="test_item1",
            amount=5678,
            quantity=2,
            payment_method=PaymentMethod.FULL_PAYMENT,
            measure=UnitsOfMesaurement.PIECES,
        ),
    ],
    11356,
)


@pytest.mark.parametrize(
    "products,expected",
    [test_products_params_1, test_products_params_2],
)
async def test_success_calculate_order_amount(
    products: list[ProductInPaymentDTO],
    expected: int,
) -> None:
    amount = AcquiringGatewayInterface._calculate_order_amount(products=products)
    assert amount == expected


def test_map_product_in_payment_to_dict() -> None:
    item = ProductInPaymentDTO(
        name="test_item1",
        amount=5678,
        quantity=2,
        payment_method=PaymentMethod.FULL_PAYMENT,
        measure=UnitsOfMesaurement.PIECES,
    )
    result = map_product_in_payment_to_dict(item=item)
    expected = {
        "name": "test_item1",
        "amount": 5678,
        "quantity": 2,
        "paymentMethod": PaymentMethod.FULL_PAYMENT.value,
        "measure": UnitsOfMesaurement.PIECES.value,
    }
    assert result == expected