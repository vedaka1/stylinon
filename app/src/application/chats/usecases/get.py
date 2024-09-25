from dataclasses import dataclass
from uuid import UUID

from src.application.chats.dto import ChatOut, MessageOut
from src.domain.chats.entities import Chat
from src.domain.chats.service import ChatServiceInterface


@dataclass
class GetUserChatsUseCase:
    chat_service: ChatServiceInterface

    async def execute(self, user_id: UUID) -> list[Chat]:
        return await self.chat_service.get_by_owner_id(user_id)


@dataclass
class GetChatUseCase:
    chat_service: ChatServiceInterface

    async def execute(self, chat_id: UUID) -> ChatOut:
        chat_data = await self.chat_service.get_by_id(chat_id=chat_id)
        return ChatOut(
            id=chat_data.id,
            title=chat_data.title,
            owner_id=chat_data.owner_id,
            created_at=chat_data.created_at,
            updated_at=chat_data.updated_at,
            messages=[
                MessageOut(
                    id=message.id,
                    user_id=message.user_id,
                    content=message.content,
                    created_at=message.created_at,
                    updated_at=message.updated_at,
                )
                for message in chat_data.messages
            ],
        )
