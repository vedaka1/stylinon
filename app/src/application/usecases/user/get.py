from dataclasses import dataclass
from uuid import UUID

from src.application.contracts.commands.user import GetUsersListCommand
from src.application.contracts.common.pagination import (
    ListPaginatedResponse,
    PaginationOutSchema,
)
from src.application.contracts.responses.user import UserOut
from src.domain.users.service import UserServiceInterface


@dataclass
class GetUserUseCase:
    user_service: UserServiceInterface

    async def execute(self, user_id: UUID) -> UserOut:
        user = await self.user_service.get_by_id(user_id=user_id)
        return UserOut(
            id=str(user.id),
            email=user.email,
            mobile_phone=user.mobile_phone,
            first_name=user.first_name,
            last_name=user.last_name,
            is_verified=user.is_verified,
            role=user.role,
        )


@dataclass
class GetUsersListUseCase:
    user_service: UserServiceInterface

    async def execute(
        self,
        command: GetUsersListCommand,
    ) -> ListPaginatedResponse[UserOut]:
        users = await self.user_service.get_many(
            offset=command.pagiantion.offset,
            limit=command.pagiantion.limit,
            search=command.search,
        )
        total = await self.user_service.count(search=command.search)
        return ListPaginatedResponse(
            items=[
                UserOut(
                    id=str(user.id),
                    email=user.email,
                    mobile_phone=user.mobile_phone,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    is_verified=user.is_verified,
                    role=user.role,
                )
                for user in users
            ],
            pagination=PaginationOutSchema(
                limit=command.pagiantion.limit,
                page=command.pagiantion.page,
                total=total,
            ),
        )
