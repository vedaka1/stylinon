from dataclasses import dataclass
from uuid import UUID

from src.application.chats.commands import GetChatsListCommand
from src.application.chats.dto import ChatOut, MessageOut
from src.application.common.pagination import ListPaginatedResponse, PaginationOutSchema
from src.domain.chats.exceptions import ChatNotFoundException
from src.domain.chats.repository import ChatRepositoryInterface


@dataclass
class GetUserChatsUseCase:
    chat_repository: ChatRepositoryInterface

    async def execute(self, user_id: UUID) -> list[ChatOut]:
        chats = await self.chat_repository.get_many(owner_id=user_id)

        return [
            ChatOut(
                id=chat.id,
                title=chat.title,
                owner_id=chat.owner_id,
                created_at=chat.created_at,
                updated_at=chat.updated_at,
                messages=[
                    MessageOut(
                        id=message.id,
                        user_id=message.user_id,
                        content=message.content,
                        created_at=message.created_at,
                        updated_at=message.updated_at,
                    )
                    for message in chat.messages
                ],
            )
            for chat in chats
        ]


@dataclass
class GetChatUseCase:
    chat_repository: ChatRepositoryInterface

    async def execute(self, chat_id: UUID) -> ChatOut:
        chat = await self.chat_repository.get_by_id(chat_id=chat_id)

        if not chat:
            raise ChatNotFoundException

        return ChatOut(
            id=chat.id,
            title=chat.title,
            owner_id=chat.owner_id,
            created_at=chat.created_at,
            updated_at=chat.updated_at,
            messages=[
                MessageOut(
                    id=message.id,
                    user_id=message.user_id,
                    content=message.content,
                    created_at=message.created_at,
                    updated_at=message.updated_at,
                )
                for message in chat.messages
            ],
        )


@dataclass
class GetChatsListUseCase:
    chat_repository: ChatRepositoryInterface

    async def execute(
        self,
        command: GetChatsListCommand,
    ) -> ListPaginatedResponse[ChatOut]:
        chats = await self.chat_repository.get_many(
            search=command.search,
            limit=command.pagination.limit,
            offset=command.pagination.offset,
        )

        count = await self.chat_repository.count(search=command.search)

        return ListPaginatedResponse(
            items=[
                ChatOut(
                    id=chat.id,
                    title=chat.title,
                    owner_id=chat.owner_id,
                    created_at=chat.created_at,
                    updated_at=chat.updated_at,
                    messages=[
                        MessageOut(
                            id=message.id,
                            user_id=message.user_id,
                            content=message.content,
                            created_at=message.created_at,
                            updated_at=message.updated_at,
                        )
                        for message in chat.messages
                    ],
                )
                for chat in chats
            ],
            pagination=PaginationOutSchema(
                limit=command.pagination.limit,
                page=command.pagination.page,
                total=count,
            ),
        )
