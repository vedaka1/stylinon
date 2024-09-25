from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass
class ChatOut:
    id: UUID
    owner_id: UUID
    title: str
    created_at: datetime
    updated_at: datetime

    messages: list["MessageOut"] = field(default_factory=list)


@dataclass
class MessageOut:
    id: UUID
    user_id: UUID
    content: str
    created_at: datetime
    updated_at: datetime
