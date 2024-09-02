from src.domain.exceptions.base import ApplicationException


class OrderItemIncorrectQuantityException(ApplicationException):
    def __init__(
        self,
        status_code: int = 400,
        message: str = "Quantity must be greater than 0",
        *args: object,
    ) -> None:
        super().__init__(status_code, message, *args)


class OrderNotFoundException(ApplicationException):
    def __init__(
        self,
        status_code: int = 404,
        message: str = "Order not found",
        *args: object,
    ) -> None:
        super().__init__(status_code, message, *args)
