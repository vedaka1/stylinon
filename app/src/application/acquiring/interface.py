from abc import ABC, abstractmethod
from typing import Any

from src.application.products.dto import ProductInPaymentDTO


class AcquiringGatewayInterface(ABC):
    @abstractmethod
    async def create_payment_operation_with_receipt(
        self,
        client_email: str,
        items: list[ProductInPaymentDTO],
        total_price: float,
        purpose: str = 'Перевод за оказанные услуги',
        payment_mode: list[str] = ['sbp', 'card'],
        save_card: bool = True,
        consumer_id: str | None = None,
    ) -> dict[str, Any]: ...
