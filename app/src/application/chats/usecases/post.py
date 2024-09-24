from dataclasses import dataclass
from uuid import UUID

from src.application.chats.commands import CreateMessageCommand
from src.application.chats.interface import WebsocketManagerInterface


@dataclass
class SendMessageUseCase:
    websocket_manager: WebsocketManagerInterface

    async def execute(self, command: CreateMessageCommand, chat_id: UUID) -> None:
        data = {"message": command.message}
        await self.websocket_manager.send_all(key=chat_id, data=data)
