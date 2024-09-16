import json
from datetime import datetime, timedelta, timezone
from typing import Any, cast
from uuid import UUID

import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.asymmetric.types import (
    PrivateKeyTypes,
    PublicKeyTypes,
)
from src.application.auth.dto import UserTokenData
from src.application.auth.exceptions import (
    TokenExpiredException,
    WrongTokenTypeException,
)
from src.application.common.jwt_processor import JwtTokenProcessorInterface, TokenType
from src.domain.common.exceptions.base import ApplicationException
from src.domain.users.entities import UserRole
from src.infrastructure.settings import settings


def load_rsa_private_key() -> RSAPrivateKey:
    key = settings.jwt.PRIVATE_KEY
    formatted_key = key.replace("\\n", "\n")
    rsa_key = serialization.load_pem_private_key(
        data=formatted_key.encode(),
        password=None,
        backend=default_backend(),
    )
    return cast(RSAPrivateKey, rsa_key)


class JwtTokenProcessor(JwtTokenProcessorInterface):

    private_key: RSAPrivateKey = load_rsa_private_key()
    jwk_key: jwt.PyJWK = jwt.PyJWK.from_json(settings.tochka.PUBLIC_KEY)

    def create_access_token(
        self,
        user_id: UUID,
        user_role: UserRole,
        email: str,
    ) -> str:
        payload = {
            "sub": str(user_id),
            "role": str(user_role.value),
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
            key=self.private_key,
            algorithm=settings.jwt.ALGORITHM,
        )
        return encoded_jwt

        # try:
        #     with ThreadPoolExecutor(max_workers=7) as executor:
        #         token = executor.submit(
        #             jwt.encode,
        #             payload=payload,
        #             key=self.key,
        #             algorithm=settings.jwt.ALGORITHM,
        #         ).result(5)
        #         return token
        # except:
        #     raise ApplicationException

    def validate_access_token(self, token: str) -> UserTokenData:
        """Returns a user id from token."""
        try:
            payload = jwt.decode(
                jwt=token,
                key=settings.jwt.PUBLIC_KEY,
                algorithms=[settings.jwt.ALGORITHM],
            )
            user_id = payload.get("sub")
            user_role = payload.get("role")
            user_email = payload.get("email")
            token_type = payload.get("type")
            if token_type == TokenType.REFRESH.value:
                raise WrongTokenTypeException
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
                jwt=token,
                key=settings.jwt.PUBLIC_KEY,
                algorithms=[settings.jwt.ALGORITHM],
            )
            user_id = payload.get("sub")
            token_type = payload.get("type")
            if token_type == TokenType.ACCESS.value:
                raise WrongTokenTypeException
            return UUID(user_id)

        except jwt.ExpiredSignatureError:
            raise TokenExpiredException
        except (jwt.DecodeError, ValueError, KeyError):
            raise ApplicationException

    def validate_acquiring_token(self, token: str) -> dict[str, Any]:
        try:

            payload = jwt.decode(
                jwt=token,
                key=self.jwk_key,
                algorithms=[settings.tochka.ALGORITHM],
            )
            return cast(dict[str, Any], payload)
        except (jwt.DecodeError, ValueError, KeyError):
            raise ApplicationException
