from uuid import uuid4

import pytest
from dishka import AsyncContainer
from src.domain.orders.entities import Order, OrderItem
from src.domain.orders.repository import (
    OrderItemRepositoryInterface,
    OrderRepositoryInterface,
)
from src.domain.products.entities import (
    Category,
    Product,
    ProductStatus,
    UnitsOfMesaurement,
)
from src.domain.products.repository import (
    CategoryRepositoryInterface,
    ProductRepositoryInterface,
)
from src.domain.products.value_objects import ProductPrice

pytestmark = pytest.mark.asyncio(loop_scope="session")


class TestOrderItemRepository:
    async def test_create_order_item(self, container: AsyncContainer) -> None:
        async with container() as di_container:
            order_repository = await di_container.get(OrderRepositoryInterface)
            product_repository = await di_container.get(ProductRepositoryInterface)
            order_item_repository = await di_container.get(OrderItemRepositoryInterface)
            category_repository = await di_container.get(CategoryRepositoryInterface)
            category = Category.create(name="test_category")
            await category_repository.create(category)

            product = Product.create(
                name="test_product",
                description="test_description",
                category="test_category",
                units_of_measurement=UnitsOfMesaurement.PIECE,
                sku="test_sku",
                bag_weight=10,
                pallet_weight=100,
                bags_per_pallet=10,
                retail_price=ProductPrice(100),
                status=ProductStatus.INSTOCK,
            )
            order = Order.create(
                customer_email="test@test.com",
                operation_id=uuid4(),
                shipping_address="test_address",
                total_price=1234,
                is_self_pickup=False,
            )
            order_item = OrderItem.create(
                order_id=order.id,
                product_id=product.id,
                quantity=1,
                price=product.retail_price,
            )
            await product_repository.create(product)
            await order_repository.create(order)
            await order_item_repository.create(order_item)
            # Check it
            order_items = await order_item_repository.get_by_order_id(order.id)
            assert len(order_items) == 1
            assert order_items[0].product_id == product.id
            assert order_items[0].quantity == 1

    async def test_create_many_order_items(self, container: AsyncContainer) -> None:
        async with container() as di_container:
            order_repository = await di_container.get(OrderRepositoryInterface)
            product_repository = await di_container.get(ProductRepositoryInterface)
            order_item_repository = await di_container.get(OrderItemRepositoryInterface)
            category_repository = await di_container.get(CategoryRepositoryInterface)
            category = Category.create(name="test_category")
            await category_repository.create(category)

            products = [
                Product.create(
                    name=f"test_product{i}",
                    description=f"test_description{i}",
                    category=f"test_category",
                    units_of_measurement=UnitsOfMesaurement.PIECE,
                    sku=f"test_sku{i}",
                    bag_weight=10,
                    pallet_weight=100,
                    bags_per_pallet=10,
                    retail_price=ProductPrice(100),
                    status=ProductStatus.INSTOCK,
                )
                for i in range(2)
            ]

            order = Order.create(
                customer_email="test@test.com",
                operation_id=uuid4(),
                shipping_address="test_address",
                total_price=1234,
                is_self_pickup=False,
            )

            order_items = [
                OrderItem.create(
                    order_id=order.id,
                    product_id=products[i].id,
                    quantity=1,
                    price=products[i].retail_price,
                )
                for i in range(2)
            ]
            for i in range(len(products)):
                await product_repository.create(products[i])

            products_data = await product_repository.get_many()

            assert len(products_data) == len(products)

            await order_repository.create(order)
            await order_item_repository.create_many(order_items)

            order_items_data = await order_item_repository.get_by_order_id(order.id)

            assert len(order_items_data) == len(order_items)

    async def test_delete_order_item(self, container: AsyncContainer) -> None:
        async with container() as di_container:
            order_repository = await di_container.get(OrderRepositoryInterface)
            product_repository = await di_container.get(ProductRepositoryInterface)
            order_item_repository = await di_container.get(OrderItemRepositoryInterface)
            category_repository = await di_container.get(CategoryRepositoryInterface)
            category = Category.create(name="test_category")
            await category_repository.create(category)

            product = Product.create(
                name="test_product",
                description="test_description",
                category="test_category",
                units_of_measurement=UnitsOfMesaurement.PIECE,
                sku="test_sku",
                bag_weight=10,
                pallet_weight=100,
                bags_per_pallet=10,
                retail_price=ProductPrice(100),
                status=ProductStatus.INSTOCK,
            )

            order = Order.create(
                customer_email="test@test.com",
                operation_id=uuid4(),
                shipping_address="test_address",
                total_price=1234,
                is_self_pickup=False,
            )

            order_item = OrderItem.create(
                order_id=order.id,
                product_id=product.id,
                quantity=1,
                price=product.retail_price,
            )
            await product_repository.create(product)
            await order_repository.create(order)
            await order_item_repository.create(order_item)
            # Delete order_item
            await order_item_repository.delete(order.id, product.id)
            # Check it
            order_items = await order_item_repository.get_by_order_id(order.id)
            assert len(order_items) == 0
