from dataclasses import dataclass

from src.domain.common.exceptions.base import ApplicationException


@dataclass
class UserNotFoundException(ApplicationException):
    status_code: int = 404
    message: str = "User not found"


@dataclass
class UserInvalidCredentialsException(ApplicationException):
    status_code: int = 400
    message: str = "Email or password are incorrect"


@dataclass
class UserAlreadyExistsException(ApplicationException):
    status_code: int = 409
    message: str = "User with this email already exists"


@dataclass
class UserConfirmationCodeNotFound(ApplicationException):
    status_code: int = 404
    message: str = "Confirmation code not found"


@dataclass
class UserConfirmationCodeExpired(ApplicationException):
    status_code: int = 401
    message: str = "Confirmation code has expired"


@dataclass
class UserConfirmationCodeInvalid(ApplicationException):
    status_code: int = 400
    message: str = "Confirmation code is invalid"
