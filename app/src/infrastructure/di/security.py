from dishka import Provider, Scope, provide
from src.application.common.interfaces import (
    JWTProcessorInterface,
    PasswordHasherInterface,
)
from src.application.common.interfaces.identity_provider import (
    IdentityProviderInterface,
)
from src.infrastructure.authentication.identity_provider import TokenIdentityProvider
from src.infrastructure.authentication.jwt_processor import JWTProcessor
from src.infrastructure.authentication.password_hasher import PasswordHasher


class SecurityProvider(Provider):
    password_hasher = provide(
        PasswordHasher,
        provides=PasswordHasherInterface,
        scope=Scope.APP,
    )
    jwt_processor = provide(
        JWTProcessor,
        provides=JWTProcessorInterface,
        scope=Scope.APP,
    )
    identity_provider = provide(
        TokenIdentityProvider,
        provides=IdentityProviderInterface,
        scope=Scope.APP,
    )
