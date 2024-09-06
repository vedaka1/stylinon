from uuid import uuid4

import pytest
from dishka import AsyncContainer
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.application.common.transaction import TransactionManagerInterface
from src.domain.orders.entities import Order, OrderItem, OrderStatus
from src.domain.orders.repository import (
    OrderItemRepositoryInterface,
    OrderRepositoryInterface,
)
from src.domain.products.entities import Product, UnitsOfMesaurement
from src.domain.products.repository import ProductRepositoryInterface
from src.infrastructure.persistence.postgresql.models.order import (
    OrderModel,
    map_to_order,
)

pytestmark = pytest.mark.asyncio(loop_scope="session")


class TestOrderRepository:
    async def test_create_order(self, container: AsyncContainer) -> None:
        async with container() as di_container:
            order_repository = await di_container.get(OrderRepositoryInterface)
            sessionmaker = await di_container.get(async_sessionmaker[AsyncSession])
            transaction_manager = await di_container.get(TransactionManagerInterface)
            # Create order
            order = Order.create(
                user_email="test@test.com",
                transaction_id=uuid4(),
                shipping_address="test_address",
            )
            await order_repository.create(order)
            await transaction_manager.commit()
            # Check it
            async with sessionmaker() as session:
                query = select(OrderModel).where(OrderModel.id == order.id)
                cursor = await session.execute(query)
                entity = cursor.scalar_one_or_none()
                assert entity
                order_data = map_to_order(entity)
                assert order_data.user_email == order.user_email
                assert order_data.transaction_id == order.transaction_id
                assert order_data.shipping_address == order.shipping_address

                delete_query = delete(OrderModel).where(OrderModel.id == order.id)
                await session.execute(delete_query)
                await session.commit()
                await session.close()

    async def test_get_order_by_id(self, container: AsyncContainer) -> None:
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
            assert order_data.status == order.status

    async def test_delete_order(self, container: AsyncContainer) -> None:
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

    async def test_get_order_by_email(self, container: AsyncContainer) -> None:
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

    async def test_get_all_orders(self, container: AsyncContainer) -> None:
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

    async def test_get_order_by_id_with_products(
        self,
        container: AsyncContainer,
    ) -> None:
        async with container() as di_container:
            order_repository = await di_container.get(OrderRepositoryInterface)
            product_repository = await di_container.get(ProductRepositoryInterface)
            order_item_repository = await di_container.get(OrderItemRepositoryInterface)

            product = Product.create(
                name="test_product",
                description="test_description",
                category="test_category",
                price=100,
                units_of_measurement=UnitsOfMesaurement.PIECES,
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
            assert len(order_data.items) == 1
            order_item = order_data.items[0]
            assert order_item.product
            assert order_item.product.name == product.name
            assert order_item.product.description == product.description
            assert order_item.product.category == product.category
            assert order_item.product.price == product.price
            assert order_item.quantity == 1
