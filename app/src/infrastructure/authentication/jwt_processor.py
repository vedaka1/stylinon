from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID

import jwt
from src.application.common.jwt_processor import JwtTokenProcessorInterface, TokenType
from src.application.contracts.common.token import UserTokenData
from src.domain.exceptions.auth import TokenExpiredException, WrongTokenTypeException
from src.domain.exceptions.base import ApplicationException
from src.domain.users.entities import UserRole
from src.infrastructure.settings import settings


class JwtTokenProcessor(JwtTokenProcessorInterface):

    def create_access_token(
        self,
        user_id: UUID,
        user_role: UserRole,
        email: str,
    ) -> str:
        payload = {
            "sub": str(user_id),
            "role": str(user_role),
            "email": str(email),
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        return self._generate_token(
            token_type=TokenType.ACCESS,
            payload=payload,
        )

    def create_refresh_token(self, user_id: UUID) -> str:
        payload = {
            "sub": str(user_id),
            "exp": datetime.now(timezone.utc)
            + timedelta(days=settings.jwt.REFRESH_TOKEN_EXPIRE_DAYS),
        }
        return self._generate_token(
            token_type=TokenType.REFRESH,
            payload=payload,
        )

    def _generate_token(self, token_type: TokenType, payload: dict[str, Any]) -> str:
        payload["type"] = token_type.value
        encoded_jwt = jwt.encode(
            payload=payload,
            key=settings.jwt.PRIVATE_KEY,
            algorithm=settings.jwt.ALGORITHM,
        )
        return f"Bearer {encoded_jwt}"

    def validate_access_token(self, token: str) -> UserTokenData:
        """Returns a user id from token."""
        try:
            payload = jwt.decode(
                token,
                settings.jwt.PUBLIC_KEY,
                algorithms=[settings.jwt.ALGORITHM],
            )
            user_id = payload.get("sub")
            user_role = payload.get("role")
            user_email = payload.get("email")
            token_type = payload.get("type")
            if token_type == TokenType.REFRESH.value:
                raise WrongTokenTypeException
            if datetime.fromtimestamp(payload.get("exp")) <= datetime.now():
                raise TokenExpiredException
            return UserTokenData(
                user_id=UUID(user_id),
                email=user_email,
                role=user_role,
            )

        except jwt.ExpiredSignatureError:
            raise TokenExpiredException
        except (jwt.DecodeError, ValueError, KeyError):
            raise ApplicationException

    def validate_refresh_token(self, token: str) -> UUID:
        """Returns a user id from token."""
        try:
            payload = jwt.decode(
                token,
                settings.jwt.PUBLIC_KEY,
                algorithms=[settings.jwt.ALGORITHM],
            )
            user_id = payload.get("sub")
            token_type = payload.get("type")
            if token_type == TokenType.ACCESS.value:
                raise WrongTokenTypeException
            if datetime.fromtimestamp(payload.get("exp")) <= datetime.now():
                raise TokenExpiredException
            return UUID(user_id)

        except jwt.ExpiredSignatureError:
            raise TokenExpiredException
        except (jwt.DecodeError, ValueError, KeyError):
            raise ApplicationException
