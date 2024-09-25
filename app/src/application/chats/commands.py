from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreateMessageCommand:
    message: str


@dataclass
class CreateChatCommand:
    title: str
