from re import T
from uuid import UUID

from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, joinedload, selectinload, subqueryload
from src.domain.chats.entities import Chat
from src.domain.chats.repository import ChatPrimaryKey, ChatRepositoryInterface
from src.infrastructure.persistence.postgresql.models.chat import (
    ChatModel,
    MessageModel,
    map_to_chat,
)
from src.infrastructure.persistence.postgresql.repositories.mappers import (
    map_to_chat_with_messages,
)


class SqlalchemyChatRepository(ChatRepositoryInterface):

    __slots__ = "session"

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, chat: Chat) -> None:
        query = insert(ChatModel).values(
            id=chat.id,
            owner_id=chat.owner_id,
            title=chat.title,
            created_at=chat.created_at,
            updated_at=chat.updated_at,
        )

        await self.session.execute(query)

        return None

    async def update(self, chat: Chat) -> None:
        query = (
            update(ChatModel)
            .where(ChatModel.id == chat.id)
            .values(
                {
                    "owner_id": chat.owner_id,
                    "title": chat.title,
                    "updated_at": chat.updated_at,
                },
            )
        )

        await self.session.execute(query)

        return None

    async def delete(self, chat_id: UUID) -> None:
        query = delete(ChatModel).where(ChatModel.id == chat_id)

        await self.session.execute(query)

        return None

    async def _get_by(
        self,
        key: ChatPrimaryKey,
        value: UUID,
        with_relations: bool = False,
    ) -> Chat | None:
        if with_relations:
            query_with_join = (
                select(ChatModel, MessageModel)
                .join(ChatModel, ChatModel.id == MessageModel.chat_id)
                .where(ChatModel.id == value)
                .limit(10)
            )

            cursor = await self.session.execute(query_with_join)

            entities = cursor.all()

            if not entities or not entities[0]:
                return None

            chat = entities[0][0]
            messages = [row[1] for row in entities]

            return map_to_chat_with_messages(entity=chat, messages=messages)

        else:
            query = select(ChatModel).where(ChatModel.id == value)

            cursor = await self.session.execute(query)

            entity = cursor.scalar_one_or_none()

            return map_to_chat(entity=entity) if entity else None

    async def get_by_id(self, chat_id: UUID) -> Chat | None:
        return await self._get_by(
            key=ChatPrimaryKey.ID,
            value=chat_id,
            with_relations=True,
        )

    async def get_many(
        self,
        search: str | None = None,
        owner_id: UUID | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> list[Chat]:
        query = select(ChatModel)

        if search:
            query = query.where(ChatModel.title.ilike(f"%{search}%"))
        if owner_id:
            query = query.where(ChatModel.owner_id == owner_id)

        query = query.limit(limit).offset(offset)

        cursor = await self.session.execute(query)

        entities = cursor.scalars().all()

        return [map_to_chat(entity) for entity in entities]

    async def count(
        self,
        search: str | None = None,
        owner_id: UUID | None = None,
    ) -> int:
        query = select(func.count()).select_from(ChatModel)

        if search:
            query = query.where(ChatModel.title.ilike(f"%{search}%"))
        if owner_id:
            query = query.where(ChatModel.owner_id == owner_id)

        cursor = await self.session.execute(query)

        count = cursor.scalar_one_or_none()

        return count if count else 0
