from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine
from src.infrastructure.persistence.postgresql.models.order import (
    OrderItemModel,
    OrderModel,
)
from src.infrastructure.persistence.postgresql.models.product import (
    CategoryModel,
    ProductModel,
)
from src.infrastructure.persistence.postgresql.models.user import (
    UserModel,
    UserSessionModel,
)
from starlette_admin import I18nConfig
from starlette_admin.contrib.sqla import Admin

from admin.auth import UsernameAndPasswordProvider
from admin.views.category import CategoryView
from admin.views.order import OrderItemView, OrderView
from admin.views.product import ProductView
from admin.views.user import UserSessionsView, UserView


def init_admin(app: FastAPI, engine: AsyncEngine) -> None:
    admin = Admin(
        engine,
        title='ТехСтрой-Сити',
        auth_provider=UsernameAndPasswordProvider(),
        i18n_config=I18nConfig(default_locale='ru'),
    )
    admin.add_view(OrderView(OrderModel))
    admin.add_view(OrderItemView(OrderItemModel))
    admin.add_view(UserView(UserModel))
    admin.add_view(UserSessionsView(UserSessionModel))
    admin.add_view(CategoryView(CategoryModel))
    admin.add_view(ProductView(ProductModel))
    admin.mount_to(app)
