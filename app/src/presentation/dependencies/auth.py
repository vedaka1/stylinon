from typing import Annotated, Dict, Optional
from uuid import UUID

from dishka import AsyncContainer
from fastapi import Depends, Request
from fastapi.openapi.models import OAuthFlowPassword
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from src.application.common.jwt_processor import JwtTokenProcessorInterface
from src.application.common.token import UserTokenData
from src.domain.exceptions.auth import UserIsNotAuthorizedException
from src.infrastructure.di.container import get_container


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
                raise UserIsNotAuthorizedException
            else:
                return None
        return param


oauth2_scheme = OAuth2PasswordBearerWithCookie("/api/v1/auth/login")


async def get_refresh_token(
    request: Request,
) -> str:
    refresh_token: str | None = request.cookies.get("refresh_token")
    print(request.cookies)
    scheme, param = get_authorization_scheme_param(refresh_token)
    if not refresh_token or scheme.lower() != "bearer":
        raise UserIsNotAuthorizedException
    return param


async def auth_required(
    request: Request,
    token: Annotated[
        str,
        Depends(oauth2_scheme),
    ],
) -> None:
    if not token:
        raise UserIsNotAuthorizedException

    request.scope["auth"] = token


async def get_current_user_data(
    token: Annotated[
        str,
        Depends(oauth2_scheme),
    ],
    container: AsyncContainer = Depends(get_container),
) -> UserTokenData:
    if not token:
        raise UserIsNotAuthorizedException
    async with container() as di_container:
        jwt_processor = await di_container.get(JwtTokenProcessorInterface)
        user_data = jwt_processor.validate_access_token(token=token)
        return user_data
