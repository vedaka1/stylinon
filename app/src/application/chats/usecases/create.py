from dataclasses import dataclass
from uuid import UUID

from src.application.chats.commands import CreateChatCommand, CreateMessageCommand
from src.application.chats.interface import WebsocketManagerInterface
from src.application.common.interfaces.transaction import TransactionManagerInterface
from src.domain.chats.entities import Chat, Message
from src.domain.chats.service import ChatServiceInterface, MessageServiceInterface


@dataclass
class CreateChatUseCase:

    chat_service: ChatServiceInterface
    transaction_manager: TransactionManagerInterface

    async def execute(self, command: CreateChatCommand, user_id: UUID) -> None:
        chat = Chat.create(
            owner_id=user_id,
            title=command.title,
        )
        await self.chat_service.create(chat=chat)
        await self.transaction_manager.commit()
        return None


@dataclass
class CreateMessageUseCase:
    websocket_manager: WebsocketManagerInterface
    message_service: MessageServiceInterface
    transaction_manager: TransactionManagerInterface

    async def execute(
        self,
        command: CreateMessageCommand,
        chat_id: UUID,
        user_id: UUID,
    ) -> None:
        message = Message.create(
            user_id=user_id,
            chat_id=chat_id,
            content=command.message,
        )
        await self.message_service.create(message=message)
        data = {"user_id": str(user_id), "message": command.message}
        await self.websocket_manager.send_all(key=chat_id, data=data)
        await self.transaction_manager.commit()
        return None
