import pytest
from dishka import AsyncContainer
from src.application.common.password_hasher import PasswordHasherInterface
from src.domain.products.entities import Product
from src.domain.products.repository import ProductRepositoryInterface

# pytestmark = pytest.mark.asyncio(loop_scope="session")


class TestProduct:
    @staticmethod
    def create_product() -> Product:
        return Product.create(
            name="test_product",
            description="test_description",
            price=100,
            category="test_category",
            units_of_measurement="test_units",
        )

    @staticmethod
    def check_product(product_data: Product | None) -> None:
        assert product_data
        assert product_data.name == "test_product"
        assert product_data.description == "test_description"
        assert product_data.price == 100
        assert product_data.category == "test_category"
        assert product_data.units_of_measurement == "test_units"


class TestProductRepository:
    async def test_create_product(self, container: AsyncContainer):
        async with container() as di_container:
            product_repository = await di_container.get(ProductRepositoryInterface)
            # Create product
            product = TestProduct.create_product()
            await product_repository.create(product)
            # Check it
            product_data = await product_repository.get_by_id(product.id)
            TestProduct.check_product(product_data)

    async def test_delete_product(self, container: AsyncContainer):
        async with container() as di_container:
            product_repository = await di_container.get(ProductRepositoryInterface)
            # Create product
            product = TestProduct.create_product()
            await product_repository.create(product)
            # Delete product
            await product_repository.delete(product.id)
            # Check it
            result = await product_repository.get_by_id(product.id)
            assert result is None

    async def test_get_product_by_category(self, container: AsyncContainer):
        async with container() as di_container:
            product_repository = await di_container.get(ProductRepositoryInterface)
            # Create product
            product = TestProduct.create_product()
            await product_repository.create(product)
            # Check it and get it
            products = await product_repository.get_by_category(
                offset=0, limit=10, category="test_category"
            )
            assert len(products) == 1
            products = await product_repository.get_by_category(
                offset=1, limit=10, category="test_category"
            )
            assert len(products) == 0
            products = await product_repository.get_by_category(
                offset=0, limit=10, category="1q2w3e"
            )
            assert len(products) == 0

    async def test_get_many_products(self, container: AsyncContainer):
        async with container() as di_container:
            product_repository = await di_container.get(ProductRepositoryInterface)
            # Create products
            product = TestProduct.create_product()
            await product_repository.create(product)
            # Check products
            products = await product_repository.get_many(offset=0, limit=10)
            assert len(products) == 1
            products = await product_repository.get_many(
                offset=0, limit=10, search="test_product"
            )
            assert len(products) == 1
            products = await product_repository.get_many(
                offset=1, limit=10, search="test_product"
            )
            assert len(products) == 0
            products = await product_repository.get_many(
                offset=0, limit=10, search="1q2w3e"
            )
            assert len(products) == 0

    async def test_count(self, container: AsyncContainer):
        async with container() as di_container:
            product_repository = await di_container.get(ProductRepositoryInterface)
            # Create products
            product = TestProduct.create_product()
            await product_repository.create(product)
            count = await product_repository.count()
            assert count == 1
            count = await product_repository.count(search="test_product")
            assert count == 1
            count = await product_repository.count(search="1q2w3e")
            assert count == 0
