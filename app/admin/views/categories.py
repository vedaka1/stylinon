from sqladmin import ModelView
from src.infrastructure.persistence.postgresql.models.product import CategoryModel


class CategoryAdmin(ModelView, model=CategoryModel):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    # column_formatters = {
    #     ProductModel.description: lambda m, a: m.description[:60] + "...",  # type: ignore
    # }
    # column_formatters_detail = {}
    name = "Категория"
    name_plural = "Категории"

    # column_searchable_list = [
    #     ProductModel.name,
    #     ProductModel.category,
    #     ProductModel.description,
    # ]
    column_list = [
        CategoryModel.name,
        CategoryModel.is_available,
    ]
    form_include_pk = True
    form_columns = [
        CategoryModel.name,
        CategoryModel.is_available,
    ]
    # column_labels = {
    #     "name": "Наименование",
    #     "category": "Категория",
    #     "description": "Описание",
    #     "price": "Цена",
    #     "units_of_measurement": "Единицы измерения",
    #     "photo_url": "Фото",
    # }

    # column_details_exclude_list = ["order_item"]
    # form_excluded_columns = ["id", "order_item"]
