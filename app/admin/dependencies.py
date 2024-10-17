from admin.views.categories import CategoryAdmin
from admin.views.order import OrderAdmin
from admin.views.order_item import OrderItemAdmin
from admin.views.products import ProductAdmin
from admin.views.user import UserAdmin
from fastapi import FastAPI
from sqladmin import Admin
from sqlalchemy.ext.asyncio import AsyncEngine


def init_admin(app: FastAPI, engine: AsyncEngine) -> None:
    admin = Admin(app=app, engine=engine)
    admin.add_view(UserAdmin)
    admin.add_view(ProductAdmin)
    admin.add_view(OrderAdmin)
    admin.add_view(OrderItemAdmin)
    admin.add_view(CategoryAdmin)
