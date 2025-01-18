from dataclasses import dataclass

from src.domain.common.exceptions.base import ApplicationException


@dataclass
class ChatNotFoundException(ApplicationException):
    status_code: int = 404
    message: str = 'Chat not found'


@dataclass
class MessageNotFoundException(ApplicationException):
    status_code: int = 404
    message: str = 'Message not found'
