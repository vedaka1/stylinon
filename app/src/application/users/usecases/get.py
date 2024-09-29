from dataclasses import dataclass
from uuid import UUID

from src.application.common.pagination import ListPaginatedResponse, PaginationOutSchema
from src.application.orders.dto import OrderItemOut, OrderOut
from src.application.users.commands import GetUsersListCommand
from src.application.users.dto import UserOut
from src.domain.orders.repository import OrderRepositoryInterface
from src.domain.users.exceptions import UserNotFoundException
from src.domain.users.repository import UserRepositoryInterface


@dataclass
class GetUserUseCase:
    user_repository: UserRepositoryInterface

    async def execute(self, user_id: UUID) -> UserOut:
        user = await self.user_repository.get_by_id(user_id=user_id)
        if not user:
            raise UserNotFoundException
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
    user_repository: UserRepositoryInterface

    async def execute(
        self,
        command: GetUsersListCommand,
    ) -> ListPaginatedResponse[UserOut]:
        users = await self.user_repository.get_many(
            offset=command.pagiantion.offset,
            limit=command.pagiantion.limit,
            search=command.search,
        )
        total = await self.user_repository.count(search=command.search)
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
    order_repository: OrderRepositoryInterface

    async def execute(self, email: str) -> list[OrderOut]:
        orders = await self.order_repository.get_by_user_email(user_email=email)
        return [
            OrderOut(
                id=order.id,
                user_email=order.user_email,
                created_at=order.created_at,
                updated_at=order.updated_at,
                shipping_address=order.shipping_address,
                operation_id=order.operation_id,
                tracking_number=order.tracking_number,
                total_price=order.total_price,
                status=order.status,
                items=[
                    OrderItemOut(
                        product_id=order_item.product.id,
                        name=order_item.product.name,
                        category=order_item.product.category,
                        description=order_item.product.description,
                        price=order_item.product.price.value,
                        quantity=order_item.quantity,
                        units_of_measurement=order_item.product.units_of_measurement,
                    )
                    for order_item in order.items
                    if order_item.product
                ],
            )
            for order in orders
        ]
