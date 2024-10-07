import asyncio
import logging
from typing import Any
from uuid import UUID

from fastapi import WebSocket
from src.application.chats.interface import WebsocketManagerInterface

logger = logging.getLogger()


class WebsocketManager(WebsocketManagerInterface):

    async def accept_connection(self, websocket: WebSocket, key: UUID) -> None:
        await websocket.accept()
        if key not in self.connections_map:
            self.connections_map[key] = set()
        async with asyncio.Lock():
            self.connections_map[key].add(websocket)
            await websocket.send_json(
                {
                    "message": "Connected",
                },
            )

    async def remove_connection(self, websocket: WebSocket, key: UUID) -> None:
        async with asyncio.Lock():
            self.connections_map[key].remove(websocket)

    async def send_all(self, key: UUID, data: dict[str, Any]) -> None:
        if key not in self.connections_map:
            return None
        async with asyncio.Lock():
            for websocket in self.connections_map[key]:
                await websocket.send_json(data)

    async def disconnect_all(self, key: UUID) -> None:
        for websocket in self.connections_map[key]:
            await websocket.send_json(
                {
                    "message": "Connection closed",
                },
            )
            await websocket.close()
