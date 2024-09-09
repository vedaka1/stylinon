from abc import ABC, abstractmethod
from typing import Any

from src.application.contracts.common.product import ProductInPayment


class AcquiringGatewayInterface(ABC):

    @abstractmethod
    async def create_payment_operation_with_receipt(
        self,
        client_email: str,
        items: list[ProductInPayment],
        purpose: str = "Перевод за оказанные услуги",
        payment_mode: list[str] = ["sbp", "card"],
        save_card: bool = True,
    ) -> dict[str, Any] | None: ...
