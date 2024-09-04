from dataclasses import dataclass

from .base import ApplicationException


@dataclass
class UserIsNotAuthorizedException(ApplicationException):
    status_code: int = 401
    message: str = "Not authorized"

    def __init__(
        self,
        *args: object,
    ) -> None:
        super().__init__(self.status_code, self.message, *args)


@dataclass
class TokenExpiredException(ApplicationException):
    status_code: int = 401
    message: str = "Your access token has expired"

    def __init__(
        self,
        *args: object,
    ) -> None:
        super().__init__(self.status_code, self.message, *args)


@dataclass
class WrongTokenTypeException(ApplicationException):
    status_code: int = 400
    message: str = "Wrong token type"

    def __init__(
        self,
        *args: object,
    ) -> None:
        super().__init__(self.status_code, self.message, *args)
