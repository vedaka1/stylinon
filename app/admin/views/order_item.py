from sqladmin import ModelView
from src.infrastructure.persistence.postgresql.models.order import OrderItemModel


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
        "product.name",
        OrderItemModel.quantity,
    ]
    column_details_list = [
        # OrderItemModel.order_id,
        # OrderItemModel.product_id,
        "order",
        "product.name",
        "quantity",
    ]
    column_labels = {
        "order": "Заказ",
        "order_id": "ID заказа",
        "order.id": "ID заказа",
        "product": "Товар",
        "product_id": "ID товара",
        "product.id": "ID товара",
        "product.name": "Наименование товара",
        "quantity": "Количество",
    }
    # column_details_exclude_list = ["order_item"]
