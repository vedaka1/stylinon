from uuid import uuid4

from sqladmin import ModelView
from src.infrastructure.persistence.postgresql.models.order import (
    OrderItemModel,
    OrderModel,
)


class OrderItemAdmin(ModelView, model=OrderItemModel):
    can_create = False
    can_edit = True
    can_delete = True
    can_view_details = True

    name = "Позиция заказа"
    name_plural = "Позиции заказа"
    column_searchable_list = [
        OrderItemModel.order_id,
    ]
    column_list = [
        OrderItemModel.order_id,
        OrderItemModel.product_id,
        OrderItemModel.quantity,
    ]
    column_details_list = [
        OrderItemModel.order_id,
        OrderItemModel.product_id,
        "quantity",
    ]
    column_labels = {
        "order_id": "ID заказа",
        "product_id": "ID товара",
        "quantity": "Количество",
        "order.id": "Заказ",
        "product.id": "Товар",
    }
    # column_details_exclude_list = ["order_item"]
