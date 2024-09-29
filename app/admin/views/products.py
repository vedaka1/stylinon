from typing import Any
from uuid import uuid4

from sqladmin import ModelView
from src.infrastructure.persistence.postgresql.models.product import ProductModel


class ProductAdmin(ModelView, model=ProductModel):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    name = "Товар"
    name_plural = "Товары"

    column_searchable_list = [
        ProductModel.name,
        ProductModel.category,
        ProductModel.description,
    ]
    column_list = [
        ProductModel.name,
        ProductModel.category,
        ProductModel.description,
        ProductModel.price,
        ProductModel.units_of_measurement,
        ProductModel.photo_url,
    ]

    column_labels = {
        "name": "Наименование",
        "category": "Категория",
        "description": "Описание",
        "price": "Цена",
        "units_of_measurement": "Единицы измерения",
        "photo_url": "Фото",
    }

    column_details_exclude_list = ["order_item"]
    form_excluded_columns = ["id", "order_item"]

    async def on_model_change(
        self,
        data: dict[str, Any],
        model: Any,
        is_created: bool,
        request: Any,
    ) -> None:
        if is_created:
            data["id"] = uuid4()
            data["photo_url"] = (
                "/images/not_found.png" if not data["photo_url"] else data["photo_url"]
            )
