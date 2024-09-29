from uuid import uuid4

from sqladmin import ModelView
from src.infrastructure.persistence.postgresql.models.order import OrderModel


class OrderAdmin(ModelView, model=OrderModel):
    can_create = False
    can_edit = True
    can_delete = True
    can_view_details = True

    name = "Заказ"
    name_plural = "Заказы"

    column_searchable_list = [
        OrderModel.user_email,
        OrderModel.shipping_address,
        OrderModel.tracking_number,
        OrderModel.status,
    ]
    column_list = [
        OrderModel.user_email,
        OrderModel.operation_id,
        OrderModel.shipping_address,
        OrderModel.tracking_number,
        OrderModel.status,
        OrderModel.created_at,
        OrderModel.updated_at,
    ]
    column_details_list = [
        OrderModel.user_email,
        OrderModel.operation_id,
        OrderModel.shipping_address,
        OrderModel.tracking_number,
        OrderModel.status,
        OrderModel.created_at,
        OrderModel.updated_at,
        OrderModel.order_items,
    ]
    column_labels = {
        "user_email": "Email клиента",
        "operation_id": "ID платежной операции",
        "shipping_address": "Адрес доставки",
        "tracking_number": "Номер отправления",
        "status": "Статус заказа",
        "created_at": "Дата создания",
        "updated_at": "Дата обновления",
        "order_items": "Список товаров",
    }
    form_ajax_refs = {
        "order_items": {
            "fields": ("order_id",),
            "order_by": "id",
        },
    }
    # column_details_exclude_list = ["order_item"]
    form_excluded_columns = ["id"]
