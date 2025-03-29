from src.application.orders.calculation import calculate_order_product_price
from src.application.orders.dto import ProductInOrder
from src.application.products.dto import PaymentMethod, ProductInPaymentDTO
from src.domain.products.entities import Product


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
