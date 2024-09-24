from uuid import UUID

import pytest
from dishka import AsyncContainer
from src.application.acquiring.interface import AcquiringGatewayInterface
from src.application.products.dto import PaymentMethod, ProductInPaymentDTO
from src.domain.products.entities import UnitsOfMesaurement

pytestmark = pytest.mark.asyncio(loop_scope="session")


class TestAcquiringGateway:

    async def test_success_create_payment_operation_with_receipt(
        self,
        container: AsyncContainer,
    ) -> None:
        products = [
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
        ]
        async with container() as di_container:
            acquiring_gateway = await di_container.get(AcquiringGatewayInterface)
            response = await acquiring_gateway.create_payment_operation_with_receipt(
                client_email="test@gmail.com",
                items=products,
            )
            expected = {
                "purpose": "Тестовый платеж",
                "status": "CREATED",
                "amount": 1234.12,
                "operationId": "e08aa797-3d6d-3834-b8d4-8a90d8fd1244",
                "paymentLink": "https://merch.bank24.int/order/?uuid=e08aa797-3d6d-3834-b8d4-8a90d8fd1244",
                "customerCode": "123456789",
                "redirectUrl": "https://example.com",
                "failRedirectUrl": "https://example.com/fail",
                "paymentMode": ["sbp", "card"],
                "merchantId": "200000000001056",
                "taxSystemCode": "osn",
                "Client": {"email": "test@gmail.com"},
                "Items": [
                    {
                        "name": "test_item1",
                        "amount": 5678,
                        "quantity": 1,
                        "paymentMethod": "full_payment",
                        "measure": "шт.",
                    },
                    {
                        "name": "test_item2",
                        "amount": 1234,
                        "quantity": 3,
                        "paymentMethod": "full_payment",
                        "measure": "шт.",
                    },
                ],
            }
            assert response == expected
