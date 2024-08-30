from src.domain.exceptions.base import ApplicationException


class ProductIncorrectPriceException(ApplicationException):
    def __init__(
        self,
        status_code: int = 400,
        message: str = "Price must be greater than 0",
        *args: object,
    ) -> None:
        super().__init__(status_code, message, *args)
