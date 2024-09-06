from http import client
from typing import Any

import aiohttp
import httpx
from src.domain.products.entities import Product
from src.infrastructure.acquiring.interface import AcquiringGatewayInterface


class TochkaAcquiringGateway(AcquiringGatewayInterface):

    error_codes: set[int] = {400, 401, 403, 404, 500}

    def __init__(
        self,
        token: str,
        base_url: str = "https://enter.tochka.com/sandbox/v2",
    ):
        self.headers = {"Authorization": f"Bearer {token}"}
        self.base_url = base_url

    async def get_customer_info(self) -> dict[str, Any] | None:
        async with aiohttp.ClientSession(
            headers=self.headers,
            base_url=self.base_url,
        ) as session:
            data = None
            response = await session.get("/open-banking/v1.0/customers/123456789")
            if response.status == 200:
                data = await response.json()
            elif response.status in self.error_codes:
                raise Exception("test")
            return data["Data"] if data else None

    async def create_payment_operation_with_receipt(
        self,
        client_email: str,
        items: list[Product],
        purpose: str = "Перевод за оказанные услуги",
        payment_mode: list[str] = ["sbp", "card"],
        save_card: bool = True,
    ) -> dict[str, Any] | None:
        amount = sum([item.price for item in items]) * 100
        data = None
        body = {
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
                "Items": [item for item in items],
            },
        }
        async with aiohttp.ClientSession(
            headers=self.headers,
            base_url=self.base_url,
        ) as session:
            response = await session.post(
                "/acquiring/v1.0/payments_with_receipt",
                json=body,
            )
            if response.status == 200:
                data = await response.json()
            elif response.status in self.error_codes:
                raise Exception("test")
            return data["Data"] if data else None
