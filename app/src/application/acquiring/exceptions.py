from dataclasses import dataclass

from src.domain.common.exceptions.base import ApplicationException


@dataclass
class IncorrectAcqioringWebhookTypeException(ApplicationException):
    status_code: int = 400
    message: str = "Wrong webhook type"


@dataclass
class IncorrectAmountException(ApplicationException):
    status_code: int = 400
    message: str = "Amount can't be less than 0"
