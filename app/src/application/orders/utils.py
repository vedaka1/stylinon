from src.application.products.dto import PaymentMethod, ProductInPaymentDTO
from src.domain.products.entities import Product
from src.domain.products.value_objects import ProductPrice


def calculate_product_price(
    product: Product,
    payment_method: PaymentMethod,
    is_self_pickup: bool,
    order_weight: int,
    products_count: int,
) -> int:
    """
    Принимает товар и опции заказа, в зависимости от опций возвращает цену товара в копейках
    ### Args:
        product: ProductVariant - товар
        payment_method: PaymentMethod - тип оплаты
        is_self_pickup: bool - самовывоз
        order_weight: int - общий вес заказа в килограммах
        products_count: int - общее количество товаров в заказе
    ### Returns:
        int: в копейках
    """
    # рыночная цена по умолчанию
    price = product.retail_price

    # вес заказа меньше 20 тонн
    if order_weight <= 20000:
        return price.value

    # в заказе один товар и вес заказа больше 20 тонн
    if products_count == 1 and product.wholesale_delivery_price:
        return product.wholesale_delivery_price.value

    # предоплата и вес заказа больше 20 тонн
    if payment_method == PaymentMethod.FULL_PREPAYMENT:

        if is_self_pickup and product.d1_self_pickup_price is not None:
            price = product.d1_self_pickup_price

        elif product.d1_delivery_price is not None:
            price = product.d1_delivery_price

    # отсрочка платежа и вес заказа больше 20 тонн
    # if payment_method == PaymentMethod.DELAYED_PAYMENT:

    #     if is_self_pickup and product.d2_self_pickup_price is not None:
    #         price = product.d2_self_pickup_price

    #     elif product.d2_delivery_price is not None:
    #         price = product.d2_delivery_price

    return price.value


def calculate_total_price(
    products: list[ProductInPaymentDTO],
) -> ProductPrice:
    """
    Принимает список товаров в заказе и возвращает итоговую цену заказа в копейках
    ### Args:
        products: list[ProductInPaymentDTO] - список товаров в заказе
    ### Returns:
        ProductPrice - цена в копейках
    """
    total_price = sum([product.amount * product.quantity for product in products])
    return ProductPrice(total_price)
