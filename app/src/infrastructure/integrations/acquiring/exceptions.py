from dataclasses import dataclass

from src.domain.common.exceptions.base import ApplicationException


@dataclass
class CreatePaymentOperationWithReceiptException(ApplicationException):
    status_code: int = 500
    message: str = "Something went wrong while creating payment operation with receipt"
