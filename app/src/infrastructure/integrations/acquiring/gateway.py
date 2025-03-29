from typing import Any, cast

import aiohttp
from src.application.acquiring.interface import AcquiringGatewayInterface
from src.application.products.dto import ProductInPaymentDTO
from src.infrastructure.integrations.acquiring.exceptions import (
    CreatePaymentOperationWithReceiptException,
)
from src.infrastructure.integrations.acquiring.mappers import map_product_in_payment_to_dict
from src.infrastructure.settings import settings


class TochkaAcquiringGateway(AcquiringGatewayInterface):
    def __init__(self, session: aiohttp.ClientSession) -> None:
        self.session = session
        self.base_url = settings.acquiring.ACQUIRING_URL
        self.api_version = settings.acquiring.ACQUIRING_API_VERSION
        self.redirect_url = settings.DOMAIN_URL

    async def create_payment_operation_with_receipt(
        self,
        client_email: str,
        items: list[ProductInPaymentDTO],
        total_price: float,
        purpose: str = 'Перевод за оказанные услуги',
        payment_mode: list[str] = ['sbp', 'card'],
        save_card: bool = True,
        consumer_id: str | None = None,
    ) -> dict[str, Any]:
        request_data = {
            'Data': {
                'customerCode': 123456789,
                'amount': total_price,
                'purpose': purpose,
                'redirectUrl': 'https://example.com',
                'failRedirectUrl': 'https://example.com/fail',
                'paymentMode': payment_mode,
                'saveCard': save_card,
                'taxSystemCode': 'osn',
                'merchantId': '200000000001056',
                'Client': {
                    'email': client_email,
                },
                'Items': [map_product_in_payment_to_dict(item) for item in items],
            },
        }
        if consumer_id:
            request_data['Data']['consumerId'] = consumer_id
        response = await self.session.post(
            f'{self.base_url}/acquiring/{self.api_version}/payments_with_receipt',
            json=request_data,
        )
        if response.status == 200:
            response_data = await response.json()
            return cast(dict[str, Any], response_data['Data'])
        else:
            raise CreatePaymentOperationWithReceiptException
