from abc import ABC, abstractmethod
from typing import Any

from src.application.acquiring.exceptions import IncorrectAmountException
from src.application.products.dto import ProductInPaymentDTO


class AcquiringGatewayInterface(ABC):

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

    @staticmethod
    def _calculate_order_amount(products: list[ProductInPaymentDTO]) -> int:
        amount = sum([product.amount * product.quantity for product in products])
        if amount <= 0:
            raise IncorrectAmountException
        return amount
