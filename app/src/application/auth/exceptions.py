from dataclasses import dataclass

from src.domain.common.exceptions.base import ApplicationException


@dataclass
class AuthException(ApplicationException):
    def __init__(
        self,
        status_code: int = 500,
        message: str = "Unknown auth error occured",
        *args: object,
    ) -> None:
        self.status_code = status_code
        self.message = message
        super().__init__(status_code, message, *args)


@dataclass
class NotAuthorizedException(AuthException):
    status_code: int = 401
    message: str = "Not authorized"


@dataclass
class RefreshTokenNotFoundException(AuthException):
    status_code: int = 404
    message: str = "Refresh token not found"


@dataclass
class TokenExpiredException(AuthException):
    status_code: int = 401
    message: str = "Your access token has expired"


@dataclass
class WrongTokenTypeException(AuthException):
    status_code: int = 400
    message: str = "Wrong token type"


@dataclass
class NotEnoughPermissionsException(AuthException):
    status_code: int = 403
    message: str = "Not enough permissions"
