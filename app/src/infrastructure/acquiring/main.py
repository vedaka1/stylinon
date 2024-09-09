from dataclasses import asdict
from http import client
from typing import Any, cast

import aiohttp
import httpx
from src.application.contracts.common.product import ProductInPayment
from src.domain.products.entities import Product
from src.infrastructure.acquiring.interface import AcquiringGatewayInterface
from src.infrastructure.acquiring.mappers import map_object_to_dict


class TochkaAcquiringGateway(AcquiringGatewayInterface):

    error_codes: set[int] = {400, 401, 403, 404, 500}

    def __init__(
        self,
        session: aiohttp.ClientSession,
        base_url: str = "https://enter.tochka.com/sandbox/v2",
    ):
        self.base_url = base_url
        self.session = session

    async def get_customer_info(self) -> dict[str, Any]:
        response = await self.session.get(
            f"{self.base_url}/open-banking/v1.0/customers/123456789",
        )
        if response.status == 200:
            response_data = await response.json()
            return cast(dict[str, Any], response_data["Data"])
        else:
            raise Exception("test")

    async def create_payment_operation_with_receipt(
        self,
        client_email: str,
        items: list[ProductInPayment],
        purpose: str = "Перевод за оказанные услуги",
        payment_mode: list[str] = ["sbp", "card"],
        save_card: bool = True,
    ) -> dict[str, Any]:
        amount = sum([item.amount * item.quantity for item in items]) * 100
        request_data = {
            "Data": {
                "customerCode": 123456789,
                "amount": amount,
                "purpose": purpose,
                "redirectUrl": "https://example.com",
                "failRedirectUrl": "https://example.com/fail",
                "paymentMode": payment_mode,
                "saveCard": save_card,
                # "consumerId": "fedac807-078d-45ac-a43b-5c01c57edbf8",
                # "taxSystemCode": "osn",
                # "merchantId": "200000000001056",
                "Client": {
                    "email": client_email,
                },
                "Items": [map_object_to_dict(item=item) for item in items],
            },
        }
        response = await self.session.post(
            f"{self.base_url}/acquiring/v1.0/payments_with_receipt",
            json=request_data,
        )
        if response.status == 200:
            response_data = await response.json()
            return cast(dict[str, Any], response_data["Data"])
        else:
            raise Exception("test")
