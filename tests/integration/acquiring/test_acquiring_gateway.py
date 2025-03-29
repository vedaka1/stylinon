import pytest
from dishka import AsyncContainer
from src.application.acquiring.interface import AcquiringGatewayInterface
from src.application.orders.utils import calculate_order_total_price
from src.application.products.dto import PaymentMethod, ProductInPaymentDTO
from src.domain.products.entities import UnitsOfMesaurement

pytestmark = pytest.mark.asyncio(loop_scope='session')


class TestAcquiringGateway:
    async def test_success_create_payment_operation_with_receipt(
        self,
        container: AsyncContainer,
    ) -> None:
        products = (
            ProductInPaymentDTO(
                name='test_item1',
                amount=567800,
                quantity=1,
                payment_method=PaymentMethod.FULL_PAYMENT,
                measure=UnitsOfMesaurement.PIECE,
            ),
            ProductInPaymentDTO(
                name='test_item2',
                amount=123400,
                quantity=3,
                payment_method=PaymentMethod.FULL_PAYMENT,
                measure=UnitsOfMesaurement.PIECE,
            ),
        )
        async with container() as di_container:
            acquiring_gateway = await di_container.get(AcquiringGatewayInterface)
            total_price = calculate_order_total_price(products)
            assert total_price.value == 567800 * 1 + 123400 * 3
            assert total_price.in_rubles() == (567800 * 1 + 123400 * 3) / 100
            response = await acquiring_gateway.create_payment_operation_with_receipt(
                client_email='test@gmail.com',
                items=products,
                total_price=total_price.in_rubles(),
            )
            expected = {
                'purpose': 'Тестовый платеж',
                'status': 'CREATED',
                'amount': 1234.12,
                'operationId': 'e08aa797-3d6d-3834-b8d4-8a90d8fd1244',
                'paymentLink': 'https://merch.bank24.int/order/?uuid=e08aa797-3d6d-3834-b8d4-8a90d8fd1244',
                'customerCode': '123456789',
                'redirectUrl': 'https://example.com',
                'failRedirectUrl': 'https://example.com/fail',
                'paymentMode': ['sbp', 'card'],
                'merchantId': '200000000001056',
                'taxSystemCode': 'osn',
                'Client': {'email': 'test@gmail.com'},
                'Items': [
                    {
                        'name': 'test_item1',
                        'amount': 5678.00,
                        'quantity': 1,
                        'paymentMethod': 'full_payment',
                        'measure': 'шт.',
                    },
                    {
                        'name': 'test_item2',
                        'amount': 1234.00,
                        'quantity': 3,
                        'paymentMethod': 'full_payment',
                        'measure': 'шт.',
                    },
                ],
            }
            assert response == expected
