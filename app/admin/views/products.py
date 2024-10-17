from typing import Any
from uuid import uuid4

from sqladmin import ModelView
from src.infrastructure.persistence.postgresql.models.product import ProductModel


class ProductAdmin(ModelView, model=ProductModel):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    column_formatters = {
        ProductModel.description: lambda m, a: m.description[:60] + "...",  # type: ignore
    }
    # column_formatters_detail = {}
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
        ProductModel.units_of_measurement,
        ProductModel.variants,
    ]

    column_labels = {
        "name": "Наименование",
        "category": "Категория",
        "description": "Описание",
        "price": "Цена",
        "units_of_measurement": "Единицы измерения",
        "photo_url": "Фото",
        "product_variants": "Варианты товара",
    }
    form_columns = [
        ProductModel.name,
        ProductModel.category,
        ProductModel.description,
        ProductModel.units_of_measurement,
        # ProductModel.product_variants,
        ProductModel.status,
    ]

    async def on_model_change(
        self,
        data: dict[str, Any],
        model: Any,
        is_created: bool,
        request: Any,
    ) -> None:
        if is_created:
            data["id"] = uuid4()
