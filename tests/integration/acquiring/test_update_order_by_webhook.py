from uuid import UUID

import pytest
from dishka import AsyncContainer
from httpx import AsyncClient
from src.application.common.interfaces.transaction import ICommiter
from src.domain.orders.entities import Order, OrderStatus
from src.domain.orders.repository import OrderRepositoryInterface

webhook_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJjdXN0b21lckNvZGUiOiAiMzAwMTIzMTIzIiwgImFtb3VudCI6ICIwLjMzIiwgInBheW1lbnRUeXBlIjogImNhcmQiLCAib3BlcmF0aW9uSWQiOiAiYmVlYWM4YTQtNjA0Ny0zZjM4LTg5MjItYTY2NGU2YjVjNDNiIiwgInB1cnBvc2UiOiAiXHUwNDFlXHUwNDNmXHUwNDNiXHUwNDMwXHUwNDQyXHUwNDMwIFx1MDQzZlx1MDQzZSBcdTA0NDFcdTA0NDdcdTA0MzVcdTA0NDJcdTA0NDMgXHUyMTE2IDEgXHUwNDNlXHUwNDQyIDAxLjAxLjIwMjEuIFx1MDQxMVx1MDQzNVx1MDQzNyBcdTA0MWRcdTA0MTRcdTA0MjEiLCAid2ViaG9va1R5cGUiOiAiYWNxdWlyaW5nSW50ZXJuZXRQYXltZW50In0.FJfaan8N1OWxLRipfsMuxmYyE69mA7yhp3uP2ycImzmT3UpSXtgdedGKP8RoVDq-r4nOiiXLMCYO7bsH0L8660wZvnCMuqZzmE_K3vbczTBdFiWhp7ExFTNX-rALuYemmdjIk4iSc7nDU4DwWvTaQGh8_yJlm9MOqa9RSFXnHpfKElNRea0rNonk02KqGdPz_zRVF7MXPjr970tEATibR52hrZCFWYZxA6FiggFsrqOykGAPX6uZyR7OD_TP0oZM5v3KxNFcnSsIxb_G8UJpdGk2GvDWDx9Px7tjkROu_ja47-N8StlY54DxDmzpaqfl35mYnLv8awGmfaZXOWYZySADRG2MDAi-iii4TPKdUtPeZga-mo0T9Vv_Jqeg9O-glFufLjCvm4dEPl36ccdpBTcvpfLthQEwa60Eb_fiyrYhIVBmjucxJZOgiATuEiXbMXPe9Z7wXYlS6tilEzBPpjy8glUcH_WDMCkK5Lylu7SCERr1Uc0PFF8M93TCTnJB'
pytestmark = pytest.mark.asyncio(loop_scope='session')


class TestOrders:
    @pytest.mark.usefixtures('clean_orders_table')
    async def test_update_order_by_webhook(
        self,
        client: AsyncClient,
        container: AsyncContainer,
    ) -> None:
        async with container() as container:
            order_repository = await container.get(OrderRepositoryInterface)
            commiter = await container.get(ICommiter)

            test_operation_id = UUID('beeac8a4-6047-3f38-8922-a664e6b5c43b')

            order = Order.create(
                customer_email='test@test.com',
                operation_id=test_operation_id,
                shipping_address='test_address',
                total_price=1234,
                is_self_pickup=False,
            )

            await order_repository.create(order)
            await commiter.commit()

            response = await client.post(
                '/orders/webhooks/payment',
                content=webhook_token,
            )

            assert response.status_code == 200

            order_data = await order_repository.get_by_id(order.id)

            assert order_data
            assert order_data.status == OrderStatus.APPROVED
