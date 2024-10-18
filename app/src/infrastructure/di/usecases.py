from dishka import Provider, Scope, provide
from src.application.auth.usecases import (
    LoginWithJWTUseCase,
    LogoutWithJWTUseCase,
    PasswordRecoveryUseCase,
    RefreshTokenUseCase,
    RegisterUseCase,
    ResetPasswordUseCase,
)
from src.application.auth.usecases.login import (
    LoginWithSessionUseCase,
    LogoutWithSessionUseCase,
)
from src.application.chats.usecases.create import (
    CreateChatUseCase,
    CreateMessageUseCase,
)
from src.application.chats.usecases.get import (
    GetChatsListUseCase,
    GetChatUseCase,
    GetUserChatsUseCase,
)
from src.application.orders.usecases import (
    CreateOrderUseCase,
    GetManyOrdersUseCase,
    GetOrderUseCase,
    UpdateOrderByWebhookUseCase,
    UpdateOrderUseCase,
)
from src.application.products.usecases import (
    CreateProductUseCase,
    GetManyProductsUseCase,
    GetProductUseCase,
)
from src.application.products.usecases.create import CreateCategoryUseCase
from src.application.products.usecases.delete import DeleteCategoryUseCase
from src.application.products.usecases.get import GetCategoriesListUseCase
from src.application.products.usecases.update import UpdateProductUseCase
from src.application.users.usecases import (
    GetUserOrdersUseCase,
    GetUsersListUseCase,
    GetUserUseCase,
)


class UseCasesProvider(Provider):
    scope = Scope.REQUEST

    register = provide(RegisterUseCase)
    login_with_jwt = provide(LoginWithJWTUseCase)
    logout_with_jwt = provide(LogoutWithJWTUseCase)
    login_with_session = provide(LoginWithSessionUseCase)
    logout_with_session = provide(LogoutWithSessionUseCase)
    refresh_token = provide(RefreshTokenUseCase)
    send_recovery_email = provide(PasswordRecoveryUseCase)
    reset_password = provide(ResetPasswordUseCase)

    get_user = provide(GetUserUseCase)
    get_users_list = provide(GetUsersListUseCase)
    get_user_orders_list = provide(GetUserOrdersUseCase)
    get_user_chats = provide(GetUserChatsUseCase)

    get_order = provide(GetOrderUseCase)
    create_order = provide(CreateOrderUseCase)
    get_many_orders = provide(GetManyOrdersUseCase)
    update_order = provide(UpdateOrderUseCase)
    update_order_by_webhook = provide(UpdateOrderByWebhookUseCase)

    get_product = provide(GetProductUseCase)
    create_product = provide(CreateProductUseCase)
    get_many_products = provide(GetManyProductsUseCase)
    update_product = provide(UpdateProductUseCase)

    create_message = provide(CreateMessageUseCase)
    create_chat = provide(CreateChatUseCase)
    get_chat = provide(GetChatUseCase)
    get_chats_list = provide(GetChatsListUseCase)

    create_category = provide(CreateCategoryUseCase)
    delete_category = provide(DeleteCategoryUseCase)
    get_categories_list = provide(GetCategoriesListUseCase)
