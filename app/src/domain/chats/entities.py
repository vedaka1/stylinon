from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Chat:
    id: UUID
    owner_id: UUID
    title: str
    created_at: datetime
    updated_at: datetime

    messages: list["Message"] = field(default_factory=list)

    @staticmethod
    def create(
        owner_id: UUID,
        title: str,
    ) -> "Chat":
        current_date = datetime.now()
        return Chat(
            id=uuid4(),
            owner_id=owner_id,
            title=title,
            created_at=current_date,
            updated_at=current_date,
        )


@dataclass
class Message:
    id: UUID
    user_id: UUID
    chat_id: UUID
    content: str
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(
        user_id: UUID,
        chat_id: UUID,
        content: str,
    ) -> "Message":
        current_date = datetime.now()
        return Message(
            id=uuid4(),
            user_id=user_id,
            chat_id=chat_id,
            content=content,
            created_at=current_date,
            updated_at=current_date,
        )
