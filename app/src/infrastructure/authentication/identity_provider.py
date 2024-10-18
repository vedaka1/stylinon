from uuid import UUID

from src.application.auth.dto import UserData
from src.application.auth.exceptions import NotAuthorizedException
from src.application.auth.roles import get_role_restrictions
from src.application.common.interfaces.identity_provider import (
    IdentityProviderInterface,
)

# from src.application.common.interfaces.jwt_processor import JWTProcessorInterface
from src.domain.users.repository import (
    UserRepositoryInterface,
    UserSessionRepositoryInterface,
)


class SessionIdentityProvider(IdentityProviderInterface):

    __slots__ = (
        "user_repository",
        "session_repository",
    )

    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        session_repository: UserSessionRepositoryInterface,
    ) -> None:
        self.user_repository = user_repository
        self.session_repository = session_repository

    async def get_current_user(
        self,
        authorization: str | None,
    ) -> UserData:
        if not authorization:
            raise NotAuthorizedException
        print(authorization)
        session = await self.session_repository.get_by_id(UUID(authorization))
        if not session or not session.user:
            raise NotAuthorizedException

        role_scopes = get_role_restrictions(role=session.user.role)

        return UserData(
            user_id=session.user.id,
            email=session.user.email,
            mobile_phone=session.user.mobile_phone,
            first_name=session.user.first_name,
            last_name=session.user.last_name,
            is_verified=session.user.is_verified,
            role=session.user.role,
            scopes=role_scopes,
        )


# class TokenIdentityProvider(IdentityProviderInterface):

#     __slots__ = ("jwt_processor",)

#     def __init__(
#         self,
#         jwt_processor: JWTProcessorInterface,
#     ) -> None:
#         self.jwt_processor = jwt_processor

#     async def get_current_user(
#         self,
#         authorization: str | None,
#     ) -> UserData:
#         if not authorization:
#             raise NotAuthorizedException

#         user_data = self.jwt_processor.validate_access_token(token=authorization)

#         return user_data
