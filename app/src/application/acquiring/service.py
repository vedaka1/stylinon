from typing import Any

from src.application.acquiring.interface import AcquiringGatewayInterface
from src.application.common.interfaces.acquiring import AcquiringServiceInterface
from src.application.common.interfaces.jwt_processor import JWTProcessorInterface
from src.application.products.dto import ProductInPaymentDTO


class AcquiringService(AcquiringServiceInterface):
    __slots__ = ("acquiring_gateway", "jwt_processor")

    def __init__(
        self,
        acquiring_gateway: AcquiringGatewayInterface,
        jwt_processor: JWTProcessorInterface,
    ):
        self.acquiring_gateway = acquiring_gateway
        self.jwt_processor = jwt_processor

    async def create_payment_operation_with_receipt(
        self,
        client_email: str,
        items: list[ProductInPaymentDTO],
        purpose: str = "Перевод за оказанные услуги",
        payment_mode: list[str] = ["sbp", "card"],
        save_card: bool = True,
        consumerId: str | None = None,
    ) -> dict[str, Any]:
        return await self.acquiring_gateway.create_payment_operation_with_receipt(
            client_email=client_email,
            items=items,
            purpose=purpose,
            payment_mode=payment_mode,
            save_card=save_card,
            consumerId=consumerId,
        )

    def handle_webhook(self, token: str) -> dict[str, Any]:
        return self.jwt_processor.validate_acquiring_token(token=token)
