from dataclasses import dataclass
from uuid import UUID

from src.domain.exceptions.base import ApplicationException


@dataclass
class ProductIncorrectPriceException(ApplicationException):
    status_code: int = 400
    message: str = "Price must be greater than 0"

    def __init__(
        self,
        *args: object,
    ) -> None:
        super().__init__(self.status_code, self.message, *args)


@dataclass
class ProductNotFoundException(ApplicationException):
    status_code: int = 404
    message: str = "Product not found"

    def __init__(
        self,
        *args: object,
    ) -> None:
        super().__init__(self.status_code, self.message, *args)


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
