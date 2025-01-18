from datetime import datetime, timedelta, timezone
from typing import Any, cast
from uuid import UUID

import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from src.application.auth.dto import UserTokenData
from src.application.auth.exceptions import (
    TokenExpiredException,
    WrongTokenTypeException,
)
from src.application.auth.roles import get_role_restrictions
from src.application.common.interfaces.jwt_processor import (
    JWTProcessorInterface,
    TokenType,
)
from src.domain.common.exceptions.base import ApplicationException
from src.domain.users.entities import UserRole
from src.infrastructure.settings import settings


def load_rsa_private_key() -> RSAPrivateKey:
    key = settings.jwt.PRIVATE_KEY
    formatted_key = key.replace('\\n', '\n')
    rsa_key = serialization.load_pem_private_key(data=formatted_key.encode(), password=None, backend=default_backend())
    return cast(RSAPrivateKey, rsa_key)


class JWTProcessor(JWTProcessorInterface):
    private_key: RSAPrivateKey = load_rsa_private_key()
    acquiring_key: jwt.PyJWK = jwt.PyJWK.from_json(settings.tochka.PUBLIC_KEY)

    def create_access_token(self, user_id: UUID, user_role: UserRole, email: str) -> str:
        user_scopes = get_role_restrictions(role=user_role)
        payload: dict[str, Any] = {
            'sub': str(user_id),
            'scopes': user_scopes,
            'email': str(email),
            'exp': datetime.now(timezone.utc) + timedelta(minutes=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        return self._generate_token(token_type=TokenType.ACCESS, payload=payload)

    def create_refresh_token(self, user_id: UUID) -> str:
        payload: dict[str, str | datetime] = {
            'sub': str(user_id),
            'exp': datetime.now(timezone.utc) + timedelta(days=settings.jwt.REFRESH_TOKEN_EXPIRE_DAYS),
        }
        return self._generate_token(token_type=TokenType.REFRESH, payload=payload)

    def create_reset_password_token(self, email: str) -> str:
        payload: dict[str, Any] = {'email': str(email), 'exp': datetime.now(timezone.utc) + timedelta(minutes=5)}
        return self._generate_token(token_type=TokenType.RESET, payload=payload)

    def _generate_token(self, token_type: TokenType, payload: dict[str, str | datetime]) -> str:
        payload['type'] = token_type.value
        encoded_jwt = jwt.encode(payload=payload, key=self.private_key, algorithm=settings.jwt.ALGORITHM)
        return encoded_jwt

    def validate_access_token(self, token: str) -> UserTokenData:
        """Returns a user id from token."""
        try:
            payload = jwt.decode(jwt=token, key=settings.jwt.PUBLIC_KEY, algorithms=[settings.jwt.ALGORITHM])
            user_id: str = payload.get('sub')
            user_scopes: str = payload.get('scopes')
            user_email: str = payload.get('email')
            token_type: str = payload.get('type')

            if token_type == TokenType.REFRESH.value:
                raise WrongTokenTypeException

            return UserTokenData(user_id=UUID(user_id), email=user_email, scopes=user_scopes)
        except jwt.ExpiredSignatureError:
            raise TokenExpiredException
        except (jwt.DecodeError, ValueError, KeyError):
            raise ApplicationException

    def validate_refresh_token(self, token: str) -> UUID:
        """Returns a user id from token."""
        try:
            payload = jwt.decode(jwt=token, key=settings.jwt.PUBLIC_KEY, algorithms=[settings.jwt.ALGORITHM])
            user_id = payload.get('sub')
            token_type = payload.get('type')
            if token_type == TokenType.ACCESS.value:
                raise WrongTokenTypeException

            return UUID(user_id)
        except jwt.ExpiredSignatureError:
            raise TokenExpiredException
        except (jwt.DecodeError, ValueError, KeyError):
            raise ApplicationException

    def validate_reset_password_token(self, token: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(jwt=token, key=settings.jwt.PUBLIC_KEY, algorithms=[settings.jwt.ALGORITHM])
            return cast(dict[str, Any], payload)
        except (jwt.DecodeError, ValueError, KeyError):
            raise ApplicationException

    def validate_acquiring_token(self, token: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(jwt=token, key=self.acquiring_key, algorithms=[settings.tochka.ALGORITHM])
            return cast(dict[str, Any], payload)
        except (jwt.DecodeError, ValueError, KeyError):
            raise ApplicationException
