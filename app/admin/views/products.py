from typing import Any
from uuid import uuid4

from sqladmin import ModelView
from src.domain.products.value_objects import ProductPrice
from src.infrastructure.persistence.postgresql.models.product import ProductModel


def convert_price_to_float(price: int | None) -> float | None:
    return ProductPrice(price).in_rubles() if price else None


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
        ProductModel.id,
        ProductModel.name,
        ProductModel.category,
        ProductModel.description,
    ]
    column_list = [
        ProductModel.name,
        ProductModel.category,
        ProductModel.description,
        ProductModel.units_of_measurement,
    ]

    column_labels = {
        "name": "Наименование",
        "category": "Категория",
        "description": "Описание",
        "units_of_measurement": "Единицы измерения",
        "image": "Фото",
        "sku": "Артикул / Код товара",
        "status": "Статус",
        "weight": "Вес мешка",
        "retail_price": "Рыночная цена (в копейках)",
        "wholesale_price": "Цена оптовой доставки (в копейках)",
        "d1_delivery_price": "Цена доставки Д1 (в копейках)",
        "d1_self_pickup_price": "Цена самовывоза Д1 (в копейках)",
    }
    form_columns = [
        ProductModel.name,
        ProductModel.category,
        ProductModel.sku,
        ProductModel.description,
        ProductModel.weight,
        ProductModel.collection,
        ProductModel.size,
        ProductModel.retail_price,
        ProductModel.wholesale_price,
        ProductModel.d1_delivery_price,
        ProductModel.d1_self_pickup_price,
        ProductModel.units_of_measurement,
        ProductModel.image,
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
