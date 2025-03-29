from src.application.orders.dto import ProductInOrder
from src.application.products.dto import PaymentMethod, ProductInPaymentDTO
from src.domain.products.entities import Product
from src.domain.products.value_objects import ProductPrice


def calculate_order_product_price(
    product: Product,
    payment_method: PaymentMethod,
    is_self_pickup: bool,
    order_weight: int | None,
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
    if order_weight and order_weight <= 20000:
        return price.value

    # в заказе один товар и вес заказа больше 20 тонн
    if products_count == 1 and product.wholesale_price:
        return product.wholesale_price.value

    # предоплата и вес заказа больше 20 тонн
    if payment_method == PaymentMethod.FULL_PREPAYMENT:
        if is_self_pickup and product.d1_self_pickup_price is not None:
            price = product.d1_self_pickup_price

        elif product.d1_delivery_price is not None:
            price = product.d1_delivery_price

    return price.value


def calculate_order_total_price(products: tuple[ProductInPaymentDTO, ...]) -> ProductPrice:
    """
    Принимает кортеж товаров в заказе и возвращает итоговую цену заказа в копейках
    Args:
        products:  список товаров в заказе
    Returns:
        ValueObject - итоговая цена заказа в копейках
    """
    total_price = sum([product.amount * product.quantity for product in products])
    return ProductPrice(total_price)


def calculate_order_total_weight(products: list[Product], order_products: list[ProductInOrder]) -> int:
    order_weight = 0
    order_products_dict = {product.id: product for product in order_products}

    for product in products:
        if product.weight:
            order_weight += product.weight * order_products_dict[product.id].quantity

    return order_weight


def create_product_in_payment_list(
    products: list[Product],
    order_products: list[ProductInOrder],
    products_count: int,
    order_weight: int,
    is_self_pickup: bool,
    payment_method: PaymentMethod,
) -> tuple[ProductInPaymentDTO, ...]:
    return tuple(
        ProductInPaymentDTO(
            name=product.name,
            amount=calculate_order_product_price(
                product=product,
                is_self_pickup=is_self_pickup,
                payment_method=payment_method,
                products_count=products_count,
                order_weight=order_weight,
            ),
            quantity=item.quantity,
            payment_method=PaymentMethod.FULL_PAYMENT,
            measure=product.units_of_measurement,
        )
        for product, item in zip(products, order_products)
    )
