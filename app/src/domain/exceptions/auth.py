from .base import ApplicationException


class UserIsNotAuthorizedException(ApplicationException):
    def __init__(
        self,
        status_code: int = 401,
        message: str = "Not authorized",
        *args: object,
    ) -> None:
        super().__init__(status_code, message, *args)


class TokenExpiredException(ApplicationException):
    def __init__(
        self,
        status_code: int = 401,
        message: str = "Your access token has expired",
        *args: object,
    ) -> None:
        super().__init__(status_code, message, *args)


class WrongTokenTypeException(ApplicationException):
    def __init__(
        self,
        status_code: int = 401,
        message: str = "Wrong token type",
        *args: object,
    ) -> None:
        super().__init__(status_code, message, *args)
