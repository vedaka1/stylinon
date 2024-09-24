from dataclasses import dataclass

from src.domain.common.exceptions.base import ApplicationException


@dataclass
class OrderItemIncorrectQuantityException(ApplicationException):
    status_code: int = 400
    message: str = "Quantity must be greater than 0"


@dataclass
class OrderNotFoundException(ApplicationException):
    status_code: int = 404
    message: str = "Order not found"
