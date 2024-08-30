from typing import Annotated, Dict, Optional
from uuid import UUID

from dishka import AsyncContainer
from fastapi import Depends, Request
from fastapi.openapi.models import OAuthFlowPassword
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from src.domain.exceptions.auth import UserIsNotAuthorizedException
from src.infrastructure.authentication.jwt_processor import JwtTokenProcessorInterface
from src.infrastructure.di.container import get_container


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(
            password=OAuthFlowPassword(tokenUrl=tokenUrl, scopes=scopes)
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


async def get_current_user_id(
    token: Annotated[
        str,
        Depends(oauth2_scheme),
    ],
    container: AsyncContainer = Depends(get_container),
) -> UUID | None:
    if not token:
        raise UserIsNotAuthorizedException
    async with container() as di_container:
        jwt_processor = await di_container.get(JwtTokenProcessorInterface)
        user_id = jwt_processor.validate_token(token=token)
        if not user_id:
            raise UserIsNotAuthorizedException
        return user_id
