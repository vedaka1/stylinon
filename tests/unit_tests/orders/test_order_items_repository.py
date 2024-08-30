from uuid import UUID, uuid4

import pytest
from dishka import AsyncContainer
from src.application.common.password_hasher import PasswordHasherInterface
from src.domain.orders.entities import Order, OrderItem, OrderStatus
from src.domain.orders.repository import (
    OrderItemRepositoryInterface,
    OrderRepositoryInterface,
)
from src.domain.products.entities import Product
from src.domain.products.repository import ProductRepositoryInterface

# pytestmark = pytest.mark.asyncio(loop_scope="session")


class TestOrderItemRepository:
    async def test_create_order_item(self, container: AsyncContainer):
        async with container() as di_container:
            order_repository = await di_container.get(OrderRepositoryInterface)
            product_repository = await di_container.get(ProductRepositoryInterface)
            order_item_repository = await di_container.get(OrderItemRepositoryInterface)

            product = Product.create(
                name="test_product",
                description="test_description",
                category="test_category",
                price=100,
                units_of_measurement="шт.",
            )
            order = Order.create(
                user_email="test@test.com",
                transaction_id=uuid4(),
                shipping_address="test_address",
            )
            order_item = OrderItem.create(
                order_id=order.id,
                product_id=product.id,
                quantity=1,
                product=product,
            )
            await product_repository.create(product)
            await order_repository.create(order)
            await order_item_repository.create(order_item)
            # Check it
            order_items = await order_item_repository.get_by_order_id(order.id)
            assert len(order_items) == 1
            assert order_items[0].product_id == product.id
            assert order_items[0].quantity == 1

    async def test_delete_order_item(self, container: AsyncContainer):
        async with container() as di_container:
            order_repository = await di_container.get(OrderRepositoryInterface)
            product_repository = await di_container.get(ProductRepositoryInterface)
            order_item_repository = await di_container.get(OrderItemRepositoryInterface)

            product = Product.create(
                name="test_product",
                description="test_description",
                category="test_category",
                price=100,
                units_of_measurement="шт.",
            )
            order = Order.create(
                user_email="test@test.com",
                transaction_id=uuid4(),
                shipping_address="test_address",
            )
            order_item = OrderItem.create(
                order_id=order.id,
                product_id=product.id,
                quantity=1,
                product=product,
            )
            await product_repository.create(product)
            await order_repository.create(order)
            await order_item_repository.create(order_item)
            # Delete order_item
            await order_item_repository.delete(order.id, product.id)
            # Check it
            order_items = await order_item_repository.get_by_order_id(order.id)
            assert len(order_items) == 0
