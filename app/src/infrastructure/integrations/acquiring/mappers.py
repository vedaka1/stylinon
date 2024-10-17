from typing import Any

from src.application.products.dto import ProductInPaymentDTO
from src.domain.products.value_objects import ProductPrice


def map_product_in_payment_to_dict(item: ProductInPaymentDTO) -> dict[str, Any]:
    data: dict[str, Any] = dict()
    if item.vat_type:
        data["vatType"] = item.vat_type.value
    if item.payment_object:
        data["paymentObject"] = item.payment_object.value
    if item.payment_method:
        data["paymentMethod"] = item.payment_method.value
    data["name"] = item.name
    data["amount"] = ProductPrice(item.amount).in_rubles()
    data["quantity"] = item.quantity
    data["measure"] = item.measure
    return data
