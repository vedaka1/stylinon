from starlette_admin import BooleanField, StringField
from starlette_admin.contrib.sqla import ModelView


class CategoryView(ModelView):
    fields = [
        StringField("name", label="Название"),
        BooleanField("is_available", label="доступно"),
    ]
    name = "Категория товара"
    label = "Категории товаров"
    pk_attr = "name"
