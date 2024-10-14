from datetime import datetime
from uuid import UUID

from src.domain.chats.entities import Chat, Message
from src.domain.chats.exceptions import ChatNotFoundException, MessageNotFoundException
from src.domain.chats.repository import (
    ChatRepositoryInterface,
    MessageRepositoryInterface,
)
from src.domain.chats.service import ChatServiceInterface, MessageServiceInterface


class ChatService(ChatServiceInterface):

    __slots__ = "chat_repository"

    def __init__(self, chat_repository: ChatRepositoryInterface) -> None:
        self.chat_repository = chat_repository

    async def create(self, chat: Chat) -> None:
        return await self.chat_repository.create(chat)

    async def update(
        self,
        chat_id: UUID,
        owner_id: UUID | None = None,
        title: str | None = None,
    ) -> None:
        chat = await self.get_by_id(chat_id)
        if owner_id:
            chat.owner_id = owner_id
        if title:
            chat.title = title
        chat.updated_at = datetime.now()
        return await self.chat_repository.update(chat)

    async def delete(self, user_id: UUID) -> None:
        return await self.chat_repository.delete(user_id)

    async def get_by_id(self, chat_id: UUID) -> Chat:
        chat = await self.chat_repository.get_by_id(chat_id)
        if not chat:
            raise ChatNotFoundException
        return chat

    async def get_by_owner_id(self, owner_id: UUID) -> list[Chat]:
        return await self.chat_repository.get_many(owner_id=owner_id)

    async def get_many(
        self,
        search: str | None = None,
        owner_id: UUID | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> list[Chat]:
        return await self.chat_repository.get_many(
            search=search,
            owner_id=owner_id,
            offset=offset,
            limit=limit,
        )

    async def count(
        self,
        search: str | None = None,
        owner_id: UUID | None = None,
    ) -> int:
        return await self.chat_repository.count(
            search=search,
            owner_id=owner_id,
        )


class MessageService(MessageServiceInterface):

    __slots__ = "message_repository"

    def __init__(self, message_repository: MessageRepositoryInterface) -> None:
        self.message_repository = message_repository

    async def create(self, message: Message) -> None:
        return await self.message_repository.create(message=message)

    async def update(self, message_id: UUID, content: str) -> None:
        message = await self.get_by_id(message_id=message_id)
        message.content = content
        message.updated_at = datetime.now()
        return await self.message_repository.update(message=message)

    async def delete(self, message_id: UUID) -> None:
        return await self.message_repository.delete(message_id=message_id)

    async def get_by_id(self, message_id: UUID) -> Message:
        message = await self.message_repository.get_by_id(message_id=message_id)
        if not message:
            raise MessageNotFoundException
        return message

    async def get_by_chat_id(
        self,
        chat_id: UUID,
        offset: int = 0,
        limit: int = 10,
    ) -> list[Message]:
        return await self.message_repository.get_by_chat_id(
            chat_id=chat_id,
            offset=offset,
            limit=limit,
        )

    async def get_many(
        self,
        chat_id: UUID | None = None,
        user_id: UUID | None = None,
        offset: int = 0,
        limit: int = 10,
    ) -> list[Message]:
        return await self.message_repository.get_many(
            chat_id=chat_id,
            user_id=user_id,
            offset=offset,
            limit=limit,
        )

    async def count(
        self,
        chat_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> int:
        return await self.message_repository.count(
            chat_id=chat_id,
            user_id=user_id,
        )

    async def get_last_messages(self, chat_id: UUID) -> list[Message]:
        return await self.message_repository.get_many(
            chat_id=chat_id,
            offset=0,
            limit=5,
        )
