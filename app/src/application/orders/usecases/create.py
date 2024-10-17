import logging
from dataclasses import dataclass

from src.application.acquiring.interface import AcquiringGatewayInterface
from src.application.common.interfaces.transaction import TransactionManagerInterface
from src.application.orders.commands import CreateOrderCommand
from src.application.orders.dto import CreateOrderOut
from src.application.products.dto import PaymentMethod, ProductInPaymentDTO
from src.domain.orders.entities import Order, OrderItem
from src.domain.orders.exceptions import DuplicateOrderPositionsException
from src.domain.orders.repository import (
    OrderItemRepositoryInterface,
    OrderRepositoryInterface,
)
from src.domain.products.entities import ProductVariant, UnitsOfMesaurement
from src.domain.products.exceptions import ManyProductsNotFoundException
from src.domain.products.repository import (
    ProductRepositoryInterface,
    ProductVariantRepositoryInterface,
)
from src.domain.products.value_objects import ProductPrice

logger = logging.getLogger()


def calculate_product_price(
    product: ProductVariant,
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
    if products_count == 1:
        return product.wholesale_delivery_price.value

    # предоплата и вес заказа больше 20 тонн
    if payment_method == PaymentMethod.FULL_PREPAYMENT:
        if is_self_pickup:
            price = product.d1_self_pickup_price
        else:
            price = product.d1_delivery_price

    # отсрочка платежа и вес заказа больше 20 тонн
    if payment_method == PaymentMethod.DELAYED_PAYMENT:
        if is_self_pickup:
            price = product.d2_self_pickup_price
        else:
            price = product.d2_delivery_price

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


@dataclass
class CreateOrderUseCase:

    order_repository: OrderRepositoryInterface
    order_item_repository: OrderItemRepositoryInterface
    products_repository: ProductRepositoryInterface
    product_variant_repository: ProductVariantRepositoryInterface
    acquiring_gateway: AcquiringGatewayInterface
    transaction_manager: TransactionManagerInterface

    async def execute(self, command: CreateOrderCommand) -> CreateOrderOut:
        products_ids = set()

        for product_item in command.items:
            if product_item.id not in products_ids:
                products_ids.add(product_item.id)
            else:
                raise DuplicateOrderPositionsException(product_item.id)

        products, missing_products = (
            await self.product_variant_repository.get_many_by_ids(
                product_variant_ids=products_ids,
            )
        )

        if missing_products:
            raise ManyProductsNotFoundException(missing_products)

        products_count = len(products)

        order_weight = sum(
            product.bag_weight * item.quantity
            for product, item in zip(products, command.items)
        )

        products_in_payment = [
            ProductInPaymentDTO(
                name=product.name,
                amount=calculate_product_price(
                    product=product,
                    is_self_pickup=command.is_self_pickup,
                    payment_method=command.payment_method,
                    products_count=products_count,
                    order_weight=order_weight,
                ),
                quantity=item.quantity,
                payment_method=PaymentMethod.FULL_PAYMENT,
                measure=(
                    product.parent_product.units_of_measurement
                    if product.parent_product
                    else UnitsOfMesaurement.PIECE
                ),
            )
            for product, item in zip(products, command.items)
        ]

        total_price = calculate_total_price(products_in_payment)
        print("order total:", total_price)

        payment_data = (
            await self.acquiring_gateway.create_payment_operation_with_receipt(
                client_email=command.customer_email,
                items=products_in_payment,
                total_price=total_price.in_rubles(),
            )
        )

        order = Order.create(
            customer_email=command.customer_email,
            operation_id=payment_data["operationId"],
            shipping_address=command.shipping_address,
            is_self_pickup=command.is_self_pickup,
            total_price=total_price.value,
        )
        order_items = [
            OrderItem.create(
                order_id=order.id,
                product_variant_id=item.id,
                quantity=item.quantity,
            )
            for item in command.items
        ]

        await self.order_repository.create(order=order)
        await self.order_item_repository.create_many(order_items)
        await self.transaction_manager.commit()

        logger.info(
            "CreateOrderUseCase",
            extra={"order_id": order.id, "customer_email": command.customer_email},
        )

        return CreateOrderOut(
            id=order.id,
            customer_email=order.customer_email,
            created_at=order.created_at,
            payment_link=payment_data["paymentLink"],
            shipping_address=order.shipping_address,
            operation_id=order.operation_id,
            total_price=ProductPrice(order.total_price).in_rubles(),
            status=order.status,
        )
