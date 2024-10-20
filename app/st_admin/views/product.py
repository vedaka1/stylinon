from typing import Any, Dict
from uuid import uuid4

from fastapi import Request, UploadFile
from src.domain.products.entities import ProductStatus, UnitsOfMesaurement
from src.infrastructure.di.container import get_container
from src.infrastructure.utils.common import StorageBackend
from starlette_admin import (
    BooleanField,
    EnumField,
    ImageField,
    IntegerField,
    StringField,
)
from starlette_admin.contrib.sqla import ModelView


class ProductView(ModelView):
    fields = [
        StringField("id", label="ID"),
        StringField("name", label="Наименование", required=True),
        StringField("sku", label="Артикул, код товара", required=True),
        StringField("collection", label="Коллекция"),
        StringField("size", label="Размер"),
        "product_category",  # type: ignore
        StringField("description", label="Описание", required=True),
        IntegerField("weight", label="Вес одной единицы"),
        IntegerField("retail_price", label="Розничная цена", required=True),
        IntegerField("wholesale_price", label="Оптовая цена"),
        IntegerField("d1_delivery_price", label="Д1 цена доставка"),
        IntegerField("d1_self_pickup_price", label="Д1 цена самовывоз"),
        EnumField(
            "units_of_measurement",
            label="Единицы изменения",
            enum=UnitsOfMesaurement,
            required=True,
        ),
        ImageField("image", label="Изображение", exclude_from_list=True),
        EnumField("status", label="Статус", enum=ProductStatus, required=True),
        BooleanField("is_available", label="Доступно"),
    ]

    searchable_fields = [
        "id",
        "name",
        "description",
        "sku",
        "category",
    ]

    exclude_fields_from_edit = ["id"]
    exclude_fields_from_create = ["id"]
    icon = "fa-lite"
    name = "Товар"
    label = "Товары"

    async def before_create(
        self,
        request: Request,
        data: Dict[str, Any],
        obj: Any,
    ) -> None:
        container = get_container()
        storage_backend = await container.get(StorageBackend)
        image: UploadFile | None = data["image"][0]
        if image:
            image_path = storage_backend.write(file=image)
        else:
            image_path = "/images/no_image.png"
        data["image"] = image_path
        obj.id = uuid4()
        obj.image = image_path
