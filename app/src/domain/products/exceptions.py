from dataclasses import dataclass
from uuid import UUID

from src.domain.common.exceptions.base import ApplicationException


@dataclass
class ProductIncorrectPriceException(ApplicationException):
    status_code: int = 400
    message: str = "Price must be greater than 0"


@dataclass
class ProductNotFoundException(ApplicationException):
    status_code: int = 404
    message: str = "Product not found"


@dataclass
class ManyProductsNotFoundException(ApplicationException):
    status_code: int = 404
    message: str = "Product not found"

    def __init__(
        self,
        missing_products: set[UUID],
        *args: object,
    ) -> None:
        self.message = f"Products not found: {missing_products}"
        super().__init__(self.status_code, self.message, *args)
