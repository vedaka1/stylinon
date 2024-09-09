from typing import Any


def map_object_to_dict(item: object) -> dict[str, Any]:
    data: dict[str, Any] = {
        key: value for key, value in item.__dict__.items() if value != None
    }
    return data
    # if item.vat_type:
    #     data["vatType"] = item.vat_type.value
    # if item.payment_object:
    #     data["paymentObject"] = item.payment_object.value
    # if item.payment_method:
    #     data["paymentMethod"] = item.payment_method.value
    # data["name"] = item.name
    # data["amount"] = item.amount
    # data["quantity"] = item.quantity
    # data["measure"] = item.measure
    # return data
