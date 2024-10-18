import logging
from typing import Annotated, Dict, Optional
from uuid import UUID

from dishka import AsyncContainer
from fastapi import Depends, Request, WebSocket
from fastapi.openapi.models import OAuthFlowPassword
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2, SecurityScopes
from fastapi.security.utils import get_authorization_scheme_param
from src.application.auth.dto import UserTokenData
from src.application.auth.exceptions import (
    NotAuthorizedException,
    NotEnoughPermissionsException,
)
from src.application.common.interfaces.identity_provider import (
    IdentityProviderInterface,
)
from src.infrastructure.di.container import get_container

logger = logging.getLogger()

AUTH_COOKIE = "session"


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        auto_error: bool = False,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(
            password=OAuthFlowPassword(tokenUrl=tokenUrl, scopes=scopes),
        )
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str | None = request.cookies.get(AUTH_COOKIE)

        # scheme, param = get_authorization_scheme_param(authorization)
        if not authorization:
            if self.auto_error:
                raise NotAuthorizedException
            else:
                return None
        return authorization


oauth2_scheme = OAuth2PasswordBearerWithCookie(
    tokenUrl="/api/v1/auth/login",
    scopes={
        "user": "Basic rights",
        "admin": "Admin rights",
    },
)


def _get_authorization_data(value: str | None) -> str:
    scheme, param = get_authorization_scheme_param(value)

    if not value:
        raise NotAuthorizedException

    return param


async def get_refresh_token(
    request: Request,
) -> str:
    refresh_token: str | None = request.cookies.get("refresh_token")

    return _get_authorization_data(value=refresh_token)


async def get_current_session(
    request: Request,
) -> UUID:
    authorization: str | None = request.cookies.get(AUTH_COOKIE)

    return UUID(authorization)


async def auth_required(
    request: Request,
    authorization: Annotated[
        str,
        Depends(oauth2_scheme),
    ],
) -> None:
    if not authorization:
        raise NotAuthorizedException

    request.scope["auth"] = authorization


async def get_current_user_data(
    security_scopes: SecurityScopes,
    authorization: Annotated[
        str,
        Depends(oauth2_scheme),
    ],
    container: AsyncContainer = Depends(get_container),
) -> UserTokenData:
    if not authorization:
        raise NotAuthorizedException

    async with container() as container:
        identity_provider = await container.get(IdentityProviderInterface)

        user_data = await identity_provider.get_current_user(
            authorization=authorization,
        )

        for scope in security_scopes.scopes:
            if scope not in user_data.scopes:
                raise NotEnoughPermissionsException

        return user_data


async def get_current_user_from_websocket(
    websocket: WebSocket,
    container: AsyncContainer,
) -> UserTokenData:
    authorization: str | None = websocket.cookies.get(AUTH_COOKIE)
    if not authorization:
        raise NotAuthorizedException
    # authorization = _get_authorization_data(value=session)

    async with container() as container:
        identity_provider = await container.get(IdentityProviderInterface)

        user_data = await identity_provider.get_current_user(
            authorization=authorization,
        )
        return user_data
