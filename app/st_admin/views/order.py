from starlette_admin.contrib.sqla import ModelView


class OrderView(ModelView):
    name = "Заказ"
    label = "Заказы"


class OrderItemView(ModelView):
    name = "Позиция заказа"
    label = "Позиции заказа"
