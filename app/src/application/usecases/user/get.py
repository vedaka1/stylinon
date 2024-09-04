from dataclasses import dataclass
from uuid import UUID

from src.application.contracts.commands.user import GetUsersListCommand
from src.application.contracts.common.pagination import (
    ListPaginatedResponse,
    PaginationOutSchema,
)
from src.application.contracts.responses.order import OrderItemOut, OrderOut
from src.application.contracts.responses.user import UserOut
from src.domain.orders.service import OrderServiceInterface
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


@dataclass
class GetUserOrdersUseCase:
    order_service: OrderServiceInterface

    async def execute(self, email: str) -> list[OrderOut]:
        orders = await self.order_service.get_by_user_email(user_email=email)
        return [
            OrderOut(
                id=order.id,
                user_email=order.user_email,
                created_at=order.created_at,
                updated_at=order.updated_at,
                shipping_address=order.shipping_address,
                transaction_id=order.transaction_id,
                tracking_number=order.tracking_number,
                status=order.status,
                items=[
                    OrderItemOut(
                        name=order_item.product.name,
                        category=order_item.product.category,
                        description=order_item.product.description,
                        price=order_item.product.price,
                        quantity=order_item.quantity,
                        units_of_measurement=order_item.product.units_of_measurement,
                    )
                    for order_item in order.items
                    if order_item.product
                ],
            )
            for order in orders
        ]
