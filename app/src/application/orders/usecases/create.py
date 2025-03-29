import logging
from dataclasses import dataclass

from src.application.acquiring.interface import AcquiringGatewayInterface
from src.application.common.interfaces.transaction import ICommiter
from src.application.orders.commands import CreateOrderCommand
from src.application.orders.dto import CreateOrderOut
from src.application.orders.utils import (
    calculate_order_total_price,
    calculate_order_total_weight,
    create_product_in_payment_list,
)
from src.domain.orders.entities import Order, OrderItem
from src.domain.orders.exceptions import DuplicateOrderPositionsException
from src.domain.orders.repository import (
    OrderItemRepositoryInterface,
    OrderRepositoryInterface,
)
from src.domain.products.exceptions import ManyProductsNotFoundException
from src.domain.products.repository import ProductRepositoryInterface
from src.domain.products.value_objects import ProductPrice

logger = logging.getLogger()


@dataclass
class CreateOrderUseCase:
    order_repository: OrderRepositoryInterface
    order_item_repository: OrderItemRepositoryInterface
    product_repository: ProductRepositoryInterface
    acquiring_gateway: AcquiringGatewayInterface
    commiter: ICommiter

    async def execute(self, command: CreateOrderCommand) -> CreateOrderOut:
        products_ids = set()
        for product_item in command.items:
            if product_item.id in products_ids:
                raise DuplicateOrderPositionsException(product_item.id)
            products_ids.add(product_item.id)

        products, missing_products = await self.product_repository.get_many_by_ids(product_ids=products_ids)
        if missing_products:
            raise ManyProductsNotFoundException(missing_products)

        products_count = len(products)
        order_weight = calculate_order_total_weight(products=products, order_products=command.items)
        products_in_payment = create_product_in_payment_list(
            products=products,
            order_products=command.items,
            products_count=products_count,
            order_weight=order_weight,
            is_self_pickup=command.is_self_pickup,
            payment_method=command.payment_method,
        )
        total_price = calculate_order_total_price(products_in_payment)

        payment_data = await self.acquiring_gateway.create_payment_operation_with_receipt(
            client_email=command.customer_email,
            items=products_in_payment,
            total_price=total_price.in_rubles(),
        )

        order = Order.create(
            customer_email=command.customer_email,
            operation_id=payment_data['operationId'],
            shipping_address=command.shipping_address,
            is_self_pickup=command.is_self_pickup,
            total_price=total_price.value,
        )
        order_items = [
            OrderItem.create(
                order_id=order.id,
                product_id=item.id,
                quantity=item.quantity,
                price=ProductPrice(product_in_payment.amount),
            )
            for item, product_in_payment in zip(command.items, products_in_payment)
        ]

        await self.order_repository.create(order=order)
        await self.order_item_repository.create_many(order_items)
        await self.commiter.commit()

        logger.info('CreateOrderUseCase', extra={'order_id': order.id, 'customer_email': command.customer_email})

        return CreateOrderOut(
            id=order.id,
            customer_email=order.customer_email,
            created_at=order.created_at,
            payment_link=payment_data['paymentLink'],
            shipping_address=order.shipping_address,
            operation_id=order.operation_id,
            total_price=ProductPrice(order.total_price).in_rubles(),
            status=order.status,
        )
