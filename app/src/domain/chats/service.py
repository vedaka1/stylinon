from abc import ABC, abstractmethod
from enum import Enum
from uuid import UUID

from src.domain.chats.entities import Chat, Message


class ChatServiceInterface(ABC):

    @abstractmethod
    async def create(self, chat: Chat) -> None: ...

    @abstractmethod
    async def update(self, chat_id: UUID, owner_id: UUID, title: str) -> None: ...

    @abstractmethod
    async def delete(self, user_id: UUID) -> None: ...

    @abstractmethod
    async def get_by_id(self, chat_id: UUID) -> Chat: ...

    @abstractmethod
    async def get_by_owner_id(self, owner_id: UUID) -> list[Chat]: ...

    @abstractmethod
    async def get_many(
        self,
        search: str | None = None,
        owner_id: UUID | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> list[Chat]: ...

    @abstractmethod
    async def count(self, search: str | None = None) -> int: ...


class MessageServiceInterface(ABC):

    @abstractmethod
    async def create(self, message: Message) -> None: ...

    @abstractmethod
    async def update(self, message_id: UUID, content: str) -> None: ...

    @abstractmethod
    async def delete(self, message_id: UUID) -> None: ...

    @abstractmethod
    async def get_by_id(self, message_id: UUID) -> Message: ...

    @abstractmethod
    async def get_by_chat_id(
        self,
        chat_id: UUID,
        offset: int = 0,
        limit: int = 10,
    ) -> list[Message]: ...

    @abstractmethod
    async def get_many(
        self,
        chat_id: UUID | None = None,
        user_id: UUID | None = None,
        offset: int = 0,
        limit: int = 10,
    ) -> list[Message]: ...

    @abstractmethod
    async def count(
        self,
        chat_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> int: ...
