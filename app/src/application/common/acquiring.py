from abc import ABC, abstractmethod
from typing import Any

from src.application.products.dto import ProductInPaymentDTO


class AcquiringServiceInterface(ABC):

    @abstractmethod
    async def create_payment_operation_with_receipt(
        self,
        client_email: str,
        items: list[ProductInPaymentDTO],
        purpose: str = "Перевод за оказанные услуги",
        payment_mode: list[str] = ["sbp", "card"],
        save_card: bool = True,
        consumerId: str | None = None,
    ) -> dict[str, Any]: ...

    @abstractmethod
    def handle_webhook(self, token: str) -> dict[str, Any]: ...

    @staticmethod
    def _calculate_order_amount(products: list[ProductInPaymentDTO]) -> int:
        amount = sum([product.amount * product.quantity for product in products])
        if amount <= 0:
            raise ValueError("Amount can't be less than 0")
        return amount
