import logging
from typing import Annotated, Dict, Optional

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
from src.application.common.interfaces.jwt_processor import JWTProcessorInterface
from src.infrastructure.di.container import get_container

logger = logging.getLogger()


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
        authorization: str | None = request.cookies.get("access_token")

        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise NotAuthorizedException
            else:
                return None
        return param


oauth2_scheme = OAuth2PasswordBearerWithCookie(
    tokenUrl="/api/v1/auth/login",
    scopes={
        "user": "Basic rights",
        "admin": "Admin rights",
    },
)


async def get_refresh_token(
    request: Request,
) -> str:
    refresh_token: str | None = request.cookies.get("refresh_token")
    scheme, param = get_authorization_scheme_param(refresh_token)
    if not refresh_token or scheme.lower() != "bearer":
        raise NotAuthorizedException
    return param


async def auth_required(
    request: Request,
    token: Annotated[
        str,
        Depends(oauth2_scheme),
    ],
) -> None:
    if not token:
        raise NotAuthorizedException

    request.scope["auth"] = token


async def get_current_user_data(
    security_scopes: SecurityScopes,
    token: Annotated[
        str,
        Depends(oauth2_scheme),
    ],
    container: AsyncContainer = Depends(get_container),
) -> UserTokenData:
    if not token:
        raise NotAuthorizedException

    jwt_processor = await container.get(JWTProcessorInterface)
    user_data = jwt_processor.validate_access_token(token=token)

    for scope in security_scopes.scopes:
        if scope not in user_data.scopes:
            raise NotEnoughPermissionsException

    return user_data


async def get_current_user_from_websocket(
    websocket: WebSocket,
    container: AsyncContainer,
) -> UserTokenData:
    authorization: str | None = websocket.cookies.get("access_token")
    scheme, param = get_authorization_scheme_param(authorization)

    if not authorization or scheme.lower() != "bearer":
        raise NotAuthorizedException

    jwt_processor = await container.get(JWTProcessorInterface)
    user_data = jwt_processor.validate_access_token(token=param)

    return user_data
