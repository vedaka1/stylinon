from uuid import UUID

from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.chats.entities import Message
from src.domain.chats.repository import MessagePrimaryKey, MessageRepositoryInterface
from src.infrastructure.persistence.postgresql.models.chat import (
    MessageModel,
    map_to_message,
)


class SqlalchemyMessageRepository(MessageRepositoryInterface):
    __slots__ = 'session'

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, message: Message) -> None:
        query = insert(MessageModel).values(
            id=message.id,
            user_id=message.user_id,
            chat_id=message.chat_id,
            content=message.content,
            created_at=message.created_at,
            updated_at=message.updated_at,
        )
        await self.session.execute(query)
        return None

    async def update(self, message: Message) -> None:
        query = (
            update(MessageModel)
            .where(MessageModel.id == message.id)
            .values(content=message.content, created_at=message.created_at, updated_at=message.updated_at)
        )
        await self.session.execute(query)
        return None

    async def delete(self, message_id: UUID) -> None:
        query = delete(MessageModel).where(MessageModel.id == message_id)
        await self.session.execute(query)
        return None

    async def _get_by(self, key: MessagePrimaryKey, value: UUID) -> Message | None:
        query = select(MessageModel)
        if key == MessagePrimaryKey.ID:
            query = query.where(MessageModel.id == value)
        cursor = await self.session.execute(query)
        entity = cursor.scalar_one_or_none()
        return map_to_message(entity) if entity else None

    async def get_by_id(self, message_id: UUID) -> Message | None:
        return await self._get_by(key=MessagePrimaryKey.ID, value=message_id)

    async def get_by_chat_id(self, chat_id: UUID, offset: int = 0, limit: int = 10) -> list[Message]:
        query = select(MessageModel).where(MessageModel.chat_id == chat_id).limit(limit).offset(offset)
        cursor = await self.session.execute(query)
        entities = cursor.scalars().all()
        return [map_to_message(entity) for entity in entities]

    async def get_many(
        self, chat_id: UUID | None = None, user_id: UUID | None = None, offset: int = 0, limit: int = 10,
    ) -> list[Message]:
        query = select(MessageModel)
        if chat_id:
            query = query.where(MessageModel.chat_id == chat_id)
        if user_id:
            query = query.where(MessageModel.user_id == user_id)
        query = query.limit(limit).offset(offset)
        cursor = await self.session.execute(query)
        entities = cursor.scalars().all()
        return [map_to_message(entity) for entity in entities]

    async def count(self, chat_id: UUID | None = None, user_id: UUID | None = None) -> int:
        query = select(func.count()).select_from(MessageModel)
        if chat_id:
            query = query.where(MessageModel.chat_id == chat_id)
        if user_id:
            query = query.where(MessageModel.user_id == user_id)
        cursor = await self.session.execute(query)
        count = cursor.scalar_one_or_none()
        return count if count else 0
