from dataclasses import dataclass

from src.domain.common.exceptions.base import ApplicationException


@dataclass
class OrderItemIncorrectQuantityException(ApplicationException):
    status_code: int = 400
    message: str = "Quantity must be greater than 0"

    def __init__(
        self,
        *args: object,
    ) -> None:
        super().__init__(self.status_code, self.message, *args)


@dataclass
class OrderNotFoundException(ApplicationException):
    status_code: int = 404
    message: str = "Order not found"

    def __init__(
        self,
        *args: object,
    ) -> None:
        super().__init__(self.status_code, self.message, *args)
