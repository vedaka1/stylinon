from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from fastapi import WebSocket


class WebsocketManagerInterface(ABC):
    connections_map: dict[UUID, set[WebSocket]] = {}

    @abstractmethod
    async def accept_connection(self, websocket: WebSocket, key: UUID) -> None: ...

    @abstractmethod
    async def remove_connection(self, websocket: WebSocket, key: UUID) -> None: ...

    @abstractmethod
    async def send_all(self, key: UUID, data: dict[str, Any]) -> None: ...

    @abstractmethod
    async def disconnect_all(self, key: UUID) -> None: ...
