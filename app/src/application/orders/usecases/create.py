import logging
from dataclasses import dataclass

from src.application.acquiring.interface import AcquiringGatewayInterface
from src.application.common.interfaces.transaction import TransactionManagerInterface
from src.application.orders.commands import CreateOrderCommand
from src.application.orders.dto import CreateOrderOut
from src.application.orders.utils import calculate_product_price, calculate_total_price
from src.application.products.dto import PaymentMethod, ProductInPaymentDTO
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
    transaction_manager: TransactionManagerInterface

    async def execute(self, command: CreateOrderCommand) -> CreateOrderOut:
        products_ids = set()

        for product_item in command.items:
            if product_item.id not in products_ids:
                products_ids.add(product_item.id)
            else:
                raise DuplicateOrderPositionsException(product_item.id)

        products, missing_products = await self.product_repository.get_many_by_ids(
            product_ids=products_ids,
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
                measure=product.units_of_measurement,
            )
            for product, item in zip(products, command.items)
        ]

        total_price = calculate_total_price(products_in_payment)

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
                product_id=item.id,
                quantity=item.quantity,
                price=ProductPrice(product_in_payment.amount),
            )
            for item, product_in_payment in zip(command.items, products_in_payment)
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
