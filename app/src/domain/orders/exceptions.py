from dataclasses import dataclass
from uuid import UUID

from src.domain.common.exceptions.base import ApplicationException


@dataclass
class OrderItemIncorrectQuantityException(ApplicationException):
    status_code: int = 400
    message: str = 'Quantity must be greater than 0'


@dataclass
class OrderNotFoundException(ApplicationException):
    status_code: int = 404
    message: str = 'Order not found'


@dataclass
class DuplicateOrderPositionsException(ApplicationException):
    status_code: int = 400
    message: str = 'Duplicate order positions are not allowed'

    def __init__(self, product_id: UUID, *args: object) -> None:
        self.message = (
            f'Duplicate order positions are not allowed. Product with id {product_id} is already in the order'
        )
        super().__init__(self.status_code, self.message, *args)
