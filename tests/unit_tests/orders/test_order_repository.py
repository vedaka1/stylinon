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


class TestOrderRepository:
    async def test_create_order(self, container: AsyncContainer):
        async with container() as di_container:
            order_repository = await di_container.get(OrderRepositoryInterface)
            # Create order
            order = Order.create(
                user_email="test@test.com",
                transaction_id=uuid4(),
                shipping_address="test_address",
            )
            await order_repository.create(order)
            # Check it
            order_data = await order_repository.get_by_id(order.id)
            assert order_data
            assert order_data.user_email == order.user_email
            assert order_data.transaction_id == order.transaction_id
            assert order_data.shipping_address == order.shipping_address

    async def test_delete_order(self, container: AsyncContainer):
        async with container() as di_container:
            order_repository = await di_container.get(OrderRepositoryInterface)
            # Create order
            order = Order.create(
                user_email="test@test.com",
                transaction_id=uuid4(),
                shipping_address="test_address",
            )
            await order_repository.create(order)
            # Delete order
            await order_repository.delete(order.id)
            # Check it
            result = await order_repository.get_by_id(order.id)
            assert result is None

    async def test_get_order_by_email(self, container: AsyncContainer):
        async with container() as di_container:
            order_repository = await di_container.get(OrderRepositoryInterface)
            # Create order
            order = Order.create(
                user_email="test@test.com",
                transaction_id=uuid4(),
                shipping_address="test_address",
            )
            await order_repository.create(order)
            # Check it and get it
            orders = await order_repository.get_by_user_email(order.user_email)
            assert len(orders) == 1

    async def test_get_all_orders(self, container: AsyncContainer):
        async with container() as di_container:
            order_repository = await di_container.get(OrderRepositoryInterface)
            # Create orders
            orders: list[Order] = [
                Order.create(
                    user_email=f"test{i}@test.com",
                    transaction_id=uuid4(),
                    shipping_address=f"test{i}_address",
                )
                for i in range(3)
            ]
            for order in orders:
                await order_repository.create(order)
            order_2 = orders[2]
            order_2.status = OrderStatus.PROCESSING
            await order_repository.update(order_2)
            # Check orders
            orders = await order_repository.get_many()
            assert len(orders) == 3
            orders = await order_repository.get_many(status=OrderStatus.PROCESSING)
            assert len(orders) == 1

    async def test_get_order_by_id_with_products(self, container: AsyncContainer):
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
            # Check it and get it
            order_data = await order_repository.get_by_id_with_products(order.id)
            assert order_data
            assert order_data.user_email == order.user_email
            assert order_data.transaction_id == order.transaction_id
            assert order_data.shipping_address == order.shipping_address
            assert len(order_data.order_items) == 1
            order_product = order_data.order_items[0]
            assert order_product.product.name == product.name
            assert order_product.product.description == product.description
            assert order_product.product.category == product.category
            assert order_product.product.price == product.price
