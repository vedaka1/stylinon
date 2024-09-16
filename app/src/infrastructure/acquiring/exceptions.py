from dataclasses import dataclass

from src.domain.exceptions.base import ApplicationException


@dataclass
class CreatePaymentOperationWithReceiptException(ApplicationException):
    status_code: int = 500
    message: str = "Something went wrong while creating payment operation with receipt"

    def __init__(
        self,
        *args: object,
    ) -> None:
        super().__init__(self.status_code, self.message, *args)


@dataclass
class IncorrectAcqioringWebhookTypeException(ApplicationException):
    status_code: int = 500
    message: str = "Wrong webhook type"

    def __init__(
        self,
        *args: object,
    ) -> None:
        super().__init__(self.status_code, self.message, *args)
