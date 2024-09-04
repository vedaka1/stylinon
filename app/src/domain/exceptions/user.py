from dataclasses import dataclass

from src.domain.exceptions.base import ApplicationException


@dataclass
class UserNotFoundException(ApplicationException):
    status_code: int = 404
    message: str = "User not found"

    def __init__(
        self,
        *args: object,
    ) -> None:
        super().__init__(self.status_code, self.message, *args)


@dataclass
class UserInvalidCredentialsException(ApplicationException):
    status_code: int = 400
    message: str = "Email or password are incorrect"

    def __init__(
        self,
        *args: object,
    ) -> None:
        super().__init__(self.status_code, self.message, *args)


@dataclass
class UserAlreadyExistsException(ApplicationException):
    status_code: int = 409
    message: str = "User with this email already exists"

    def __init__(
        self,
        *args: object,
    ) -> None:
        super().__init__(self.status_code, self.message, *args)


@dataclass
class UserConfirmationCodeNotFound(ApplicationException):
    status_code: int = 404
    message: str = "Confirmation code not found"

    def __init__(
        self,
        *args: object,
    ) -> None:
        super().__init__(self.status_code, self.message, *args)


@dataclass
class UserConfirmationCodeExpired(ApplicationException):
    status_code: int = 401
    message: str = "Confirmation code has expired"

    def __init__(
        self,
        *args: object,
    ) -> None:
        super().__init__(self.status_code, self.message, *args)


@dataclass
class UserConfirmationCodeInvalid(ApplicationException):
    status_code: int = 400
    message: str = "Confirmation code is invalid"

    def __init__(
        self,
        *args: object,
    ) -> None:
        super().__init__(self.status_code, self.message, *args)
