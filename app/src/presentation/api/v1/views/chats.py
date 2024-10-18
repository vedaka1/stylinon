import logging
from typing import Annotated
from uuid import UUID

from dishka import AsyncContainer
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, Security, WebSocket, WebSocketDisconnect
from src.application.auth.dto import UserData
from src.application.auth.exceptions import (
    NotAuthorizedException,
    TokenExpiredException,
)
from src.application.chats.commands import (
    CreateChatCommand,
    CreateMessageCommand,
    GetChatsListCommand,
)
from src.application.chats.dto import ChatOut
from src.application.chats.interface import WebsocketManagerInterface
from src.application.chats.usecases.create import (
    CreateChatUseCase,
    CreateMessageUseCase,
)
from src.application.chats.usecases.get import GetChatsListUseCase, GetChatUseCase
from src.application.common.pagination import ListPaginatedResponse, PaginationQuery
from src.application.common.response import APIResponse
from src.domain.users.entities import UserRole
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


def get_pagination(limit: int = 100, page: int = 0) -> PaginationQuery:
    return PaginationQuery(page=page, limit=limit)


def get_chats_list_command(
    search: str | None = None,
    pagination: PaginationQuery = Depends(get_pagination),
) -> GetChatsListCommand:
    return GetChatsListCommand(
        search=search,
        pagination=pagination,
    )


@router.post("")
async def create_chat(
    command: CreateChatCommand,
    create_chat_interactor: FromDishka[CreateChatUseCase],
    user_data: Annotated[UserData, Depends(get_current_user_data)],
) -> APIResponse[None]:
    await create_chat_interactor.execute(
        command=command,
        user_id=user_data.user_id,
    )

    return APIResponse()


@router.get(
    "",
    summary="Возвращает список существующих чатов",
    dependencies=[
        Security(
            get_current_user_data,
            scopes=[
                UserRole.ADMIN.value,
                UserRole.MANAGER.value,
            ],
        ),
    ],
)
async def get_chats_list(
    command: Annotated[GetChatsListCommand, Depends(get_chats_list_command)],
    get_chats_interactor: FromDishka[GetChatsListUseCase],
) -> APIResponse[ListPaginatedResponse[ChatOut]]:
    response = await get_chats_interactor.execute(command=command)

    return APIResponse(data=response)


@router.get("/{chat_id}", dependencies=[Depends(get_current_user_data)])
async def get_chat(
    chat_id: UUID,
    get_chat_interactor: FromDishka[GetChatUseCase],
) -> APIResponse[ChatOut]:
    response = await get_chat_interactor.execute(chat_id=chat_id)

    return APIResponse(data=response)


@router.post("/{chat_id}")
async def create_message(
    command: CreateMessageCommand,
    chat_id: UUID,
    create_message_interactor: FromDishka[CreateMessageUseCase],
    user_data: Annotated[UserData, Depends(get_current_user_data)],
) -> APIResponse[None]:
    await create_message_interactor.execute(
        command=command,
        chat_id=chat_id,
        user_id=user_data.user_id,
    )
    return APIResponse()


logger = logging.getLogger()


@router.websocket("/ws/{chat_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    chat_id: UUID,
    container: Annotated[AsyncContainer, Depends(get_container)],
) -> None:
    websocket_manager = await container.get(WebsocketManagerInterface)

    await websocket_manager.accept_connection(websocket=websocket, key=chat_id)

    try:

        await get_current_user_from_websocket(websocket=websocket, container=container)

        while True:
            await websocket.receive_text()

    except (NotAuthorizedException, TokenExpiredException) as exc:
        await websocket.send_json(data={"message": exc.message})

        await websocket_manager.remove_connection(websocket=websocket, key=chat_id)

        await websocket.close()

    except WebSocketDisconnect:
        await websocket_manager.remove_connection(websocket=websocket, key=chat_id)
