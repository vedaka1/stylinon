from dataclasses import dataclass

from src.domain.common.exceptions.base import ApplicationException


@dataclass
class IncorrectAcqioringWebhookTypeException(ApplicationException):
    status_code: int = 500
    message: str = "Wrong webhook type"
