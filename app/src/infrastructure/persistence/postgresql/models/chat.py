from datetime import datetime
from uuid import UUID

from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.domain.chats.entities import Chat, Message
from src.infrastructure.persistence.postgresql.models.base import Base


class ChatModel(Base):

    __tablename__ = "chats"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True)
    owner_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False),
        nullable=False,
    )
    last_messages: Mapped[list["MessageModel"]] = relationship(back_populates="chat")


def map_to_chat(entity: ChatModel, with_relations: bool = False) -> Chat:
    chat = Chat(
        id=entity.id,
        owner_id=entity.owner_id,
        title=entity.title,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )
    if with_relations:
        chat.messages = [map_to_message(message) for message in entity.last_messages]
    return chat


class MessageModel(Base):

    __tablename__ = "messages"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    chat_id: Mapped[UUID] = mapped_column(
        ForeignKey("chats.id", ondelete="CASCADE"),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False),
        nullable=False,
    )

    chat: Mapped["ChatModel"] = relationship(back_populates="last_messages")


def map_to_message(entity: MessageModel) -> Message:
    message = Message(
        id=entity.id,
        user_id=entity.user_id,
        chat_id=entity.chat_id,
        content=entity.content,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )
    return message
