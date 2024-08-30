from src.domain.exceptions.base import ApplicationException


class UserNotFoundException(ApplicationException):
    def __init__(
        self,
        status_code: int = 404,
        message: str = "User not found",
        *args: object,
    ) -> None:
        super().__init__(status_code, message, *args)


class UserInvalidCredentialsException(ApplicationException):
    def __init__(
        self,
        status_code: int = 400,
        message: str = "Email or password are incorrect",
        *args: object,
    ) -> None:
        super().__init__(status_code, message, *args)


class UserAlreadyExistsException(ApplicationException):
    def __init__(
        self,
        status_code: int = 409,
        message: str = "User with this email already exists",
        *args: object,
    ) -> None:
        super().__init__(status_code, message, *args)


class UserConfirmationCodeNotFound(ApplicationException):
    def __init__(
        self,
        status_code: int = 404,
        message: str = "Confirmation code not found",
        *args: object,
    ) -> None:
        super().__init__(status_code, message, *args)


class UserConfirmationCodeExpired(ApplicationException):
    def __init__(
        self,
        status_code: int = 401,
        message: str = "Confirmation code has expired",
        *args: object,
    ) -> None:
        super().__init__(status_code, message, *args)


class UserConfirmationCodeInvalid(ApplicationException):
    def __init__(
        self,
        status_code: int = 400,
        message: str = "Confirmation code is invalid",
        *args: object,
    ) -> None:
        super().__init__(status_code, message, *args)
