from dishka import Provider, Scope, provide
from src.application.auth.usecases import (
    LoginUseCase,
    LogoutUseCase,
    PasswordRecoveryUseCase,
    RefreshTokenUseCase,
    RegisterUseCase,
    ResetPasswordUseCase,
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
from src.application.products.usecases.update import UpdateProductUseCase
from src.application.users.usecases import (
    GetUserOrdersUseCase,
    GetUsersListUseCase,
    GetUserUseCase,
)


class UseCasesProvider(Provider):
    scope = Scope.REQUEST

    register = provide(RegisterUseCase)
    login = provide(LoginUseCase)
    logout = provide(LogoutUseCase)
    refresh_token = provide(RefreshTokenUseCase)
    get_user = provide(GetUserUseCase)
    get_users_list = provide(GetUsersListUseCase)
    get_user_orders_list = provide(GetUserOrdersUseCase)
    get_order = provide(GetOrderUseCase)
    create_order = provide(CreateOrderUseCase)
    get_many_orders = provide(GetManyOrdersUseCase)
    update_order = provide(UpdateOrderUseCase)
    update_order_by_webhook = provide(UpdateOrderByWebhookUseCase)
    get_product = provide(GetProductUseCase)
    create_product = provide(CreateProductUseCase)
    get_many_products = provide(GetManyProductsUseCase)
    send_recovery_email = provide(PasswordRecoveryUseCase)
    reset_password = provide(ResetPasswordUseCase)
    create_message = provide(CreateMessageUseCase)
    create_chat = provide(CreateChatUseCase)
    get_user_chats = provide(GetUserChatsUseCase)
    get_chat = provide(GetChatUseCase)
    get_chats_list = provide(GetChatsListUseCase)
    update_product = provide(UpdateProductUseCase)
