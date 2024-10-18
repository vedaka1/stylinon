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
        "order_product.name",
        OrderItemModel.quantity,
        OrderItemModel.price,
    ]
    column_details_list = [
        # OrderItemModel.order_id,
        # OrderItemModel.product_id,
        "order",
        "order_product.name",
        "quantity",
        "price",
    ]
    column_labels = {
        "order": "Заказ",
        "product": "Товар",
        "product.id": "ID товара",
        "order_product.name": "Наименование товара",
        "quantity": "Количество",
        "price": "Расчетная цена за товар (в копейках)",
    }
    # column_details_exclude_list = ["order_item"]
