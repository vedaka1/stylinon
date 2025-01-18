from abc import ABC, abstractmethod
from enum import Enum
from uuid import UUID

from src.domain.chats.entities import Chat, Message


class ChatPrimaryKey(Enum):
    ID = 'id'
    # OWNER_ID = "owner_id"


class MessagePrimaryKey(Enum):
    ID = 'id'
    USER_ID = 'user_id'
    CHAT_ID = 'chat_id'


class ChatRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, chat: Chat) -> None: ...

    @abstractmethod
    async def update(self, chat: Chat) -> None: ...

    @abstractmethod
    async def delete(self, chat_id: UUID) -> None: ...

    @abstractmethod
    async def _get_by(self, key: ChatPrimaryKey, value: UUID, with_relations: bool = False) -> Chat | None: ...

    @abstractmethod
    async def get_by_id(self, chat_id: UUID) -> Chat | None: ...

    @abstractmethod
    async def get_many(
        self,
        search: str | None = None,
        owner_id: UUID | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> list[Chat]: ...

    @abstractmethod
    async def count(self, search: str | None = None, owner_id: UUID | None = None) -> int: ...


class MessageRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, message: Message) -> None: ...

    @abstractmethod
    async def update(self, message: Message) -> None: ...

    @abstractmethod
    async def delete(self, message_id: UUID) -> None: ...

    @abstractmethod
    async def _get_by(self, key: MessagePrimaryKey, value: UUID) -> Message | None: ...

    @abstractmethod
    async def get_by_id(self, message_id: UUID) -> Message | None: ...

    @abstractmethod
    async def get_by_chat_id(self, chat_id: UUID, offset: int = 0, limit: int = 10) -> list[Message]: ...

    @abstractmethod
    async def get_many(
        self,
        chat_id: UUID | None = None,
        user_id: UUID | None = None,
        offset: int = 0,
        limit: int = 10,
    ) -> list[Message]: ...

    @abstractmethod
    async def count(self, chat_id: UUID | None = None, user_id: UUID | None = None) -> int: ...
