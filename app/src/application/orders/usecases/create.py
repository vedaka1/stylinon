import logging
from dataclasses import dataclass

from src.application.acquiring.interface import AcquiringGatewayInterface
from src.application.common.interfaces.transaction import TransactionManagerInterface
from src.application.orders.commands import CreateOrderCommand
from src.application.orders.dto import CreateOrderResponse
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
    products_repository: ProductRepositoryInterface
    acquiring_gateway: AcquiringGatewayInterface
    transaction_manager: TransactionManagerInterface

    async def execute(self, command: CreateOrderCommand) -> CreateOrderResponse:
        products_set = set()

        for product in command.items:
            if product.id not in products_set:
                products_set.add(product.id)
            else:
                raise DuplicateOrderPositionsException(product.id)

        products, missing_products = await self.products_repository.get_many_by_ids(
            product_ids=products_set,
        )

        if missing_products:
            raise ManyProductsNotFoundException(missing_products)

        products_in_payment = [
            ProductInPaymentDTO(
                name=product.name,
                amount=product.price.value,
                quantity=item.quantity,
                payment_method=PaymentMethod.FULL_PAYMENT,
                measure=product.units_of_measurement,
            )
            for product, item in zip(products, command.items)
        ]

        payment_data = (
            await self.acquiring_gateway.create_payment_operation_with_receipt(
                client_email=command.customer_email,
                items=products_in_payment,
            )
        )

        order = Order.create(
            customer_email=command.customer_email,
            operation_id=payment_data["operationId"],
            shipping_address=command.shipping_address,
            total_price=AcquiringGatewayInterface._calculate_order_amount(
                products=products_in_payment,
            ),
        )
        order_items = [
            OrderItem.create(
                order_id=order.id,
                product_id=item.id,
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

        return CreateOrderResponse(
            id=order.id,
            customer_email=order.customer_email,
            created_at=order.created_at,
            payment_link=payment_data["paymentLink"],
            shipping_address=order.shipping_address,
            operation_id=order.operation_id,
            total_price=ProductPrice(order.total_price).in_rubles(),
            status=order.status,
        )
