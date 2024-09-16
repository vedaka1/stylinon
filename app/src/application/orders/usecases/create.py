from dataclasses import dataclass
from uuid import uuid4

from src.application.acquiring.interface import AcquiringGatewayInterface
from src.application.common.transaction import TransactionManagerInterface
from src.application.orders.commands import CreateOrderCommand
from src.application.orders.responses import CreateOrderResponse
from src.application.products.dto import PaymentMethod, ProductInPaymentDTO
from src.domain.exceptions.products import ManyProductsNotFoundException
from src.domain.orders.entities import Order, OrderItem
from src.domain.orders.service import OrderItemServiceInterface, OrderServiceInterface
from src.domain.products.service import ProductServiceInterface

# from src.infrastructure.acquiring.interface import AcquiringGatewayInterface


@dataclass
class CreateOrderUseCase:
    order_service: OrderServiceInterface
    order_item_service: OrderItemServiceInterface
    products_service: ProductServiceInterface
    acquiring_gateway: AcquiringGatewayInterface
    transaction_manager: TransactionManagerInterface

    async def execute(self, command: CreateOrderCommand) -> CreateOrderResponse:
        # raise Exception("Not implemented")
        products, missing_products = await self.products_service.get_many_by_ids(
            product_ids=[item.id for item in command.items],
        )
        if missing_products:
            raise ManyProductsNotFoundException(missing_products)
        products_in_payment = [
            ProductInPaymentDTO(
                name=product.name,
                amount=product.price,
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
            user_email=command.customer_email,
            operation_id=payment_data["operationId"],
            shipping_address=command.shipping_address,
        )
        order_items = [
            OrderItem.create(
                order_id=order.id,
                product_id=item.id,
                quantity=item.quantity,
            )
            for item in command.items
        ]
        await self.order_service.create(order=order)
        await self.order_item_service.create_many(order_items)
        await self.transaction_manager.commit()
        return CreateOrderResponse(
            id=order.id,
            customer_email=order.user_email,
            created_at=order.created_at,
            payment_link=payment_data["paymentLink"],
            shipping_address=order.shipping_address,
            operation_id=order.operation_id,
            status=order.status,
        )
