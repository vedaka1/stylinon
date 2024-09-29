from src.domain.chats.entities import Chat
from src.infrastructure.persistence.postgresql.models.chat import (
    ChatModel,
    MessageModel,
    map_to_message,
)


def map_to_chat_with_messages(entity: ChatModel, messages: list[MessageModel]) -> Chat:
    return Chat(
        id=entity.id,
        owner_id=entity.owner_id,
        title=entity.title,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
        messages=[map_to_message(message) for message in messages],
    )
