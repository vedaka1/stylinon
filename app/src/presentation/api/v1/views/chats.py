from typing import Annotated
from uuid import UUID

from dishka import AsyncContainer
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from src.application.auth.exceptions import NotAuthorizedException
from src.application.chats.commands import CreateMessageCommand
from src.application.chats.interface import WebsocketManagerInterface
from src.application.chats.usecases.post import SendMessageUseCase
from src.application.common.response import APIResponse
from src.infrastructure.di.container import get_container
from src.presentation.dependencies.auth import (
    get_current_user_data,
    get_current_user_from_websocket,
)

router = APIRouter(
    tags=["Chats"],
    prefix="/chats",
    route_class=DishkaRoute,
)


@router.post("/{chat_id}", dependencies=[Depends(get_current_user_data)])
async def send_message(
    command: CreateMessageCommand,
    chat_id: UUID,
    send_message_interactor: FromDishka[SendMessageUseCase],
) -> APIResponse[None]:
    await send_message_interactor.execute(command=command, chat_id=chat_id)
    return APIResponse()


@router.websocket("/ws/{chat_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    chat_id: UUID,
    container: Annotated[AsyncContainer, Depends(get_container)],
) -> None:
    websocket_manager = await container.get(WebsocketManagerInterface)

    try:
        await get_current_user_from_websocket(websocket=websocket, container=container)
    except NotAuthorizedException as exc:
        await websocket.accept()
        await websocket.send_json(data={"error": exc.message})
        await websocket.close()

    await websocket_manager.accept_connection(websocket=websocket, key=chat_id)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await websocket_manager.remove_connection(websocket=websocket, key=chat_id)
