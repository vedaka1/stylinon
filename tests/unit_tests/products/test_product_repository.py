import pytest
from dishka import AsyncContainer
from src.domain.products.entities import Product, UnitsOfMesaurement
from src.domain.products.repository import ProductRepositoryInterface

pytestmark = pytest.mark.asyncio(scope="session")


class TestProduct:
    @staticmethod
    def create_product() -> Product:
        return Product.create(
            name="test_product",
            description="test_description",
            price=100,
            category="test_category",
            units_of_measurement=UnitsOfMesaurement.PIECES,
        )

    @staticmethod
    def check_product(product_data: Product | None) -> None:
        assert product_data
        assert product_data.name == "test_product"
        assert product_data.description == "test_description"
        assert product_data.price == 100
        assert product_data.category == "test_category"
        assert product_data.units_of_measurement == UnitsOfMesaurement.PIECES


class TestProductRepository:
    async def test_create_product(self, container: AsyncContainer) -> None:
        async with container() as di_container:
            product_repository = await di_container.get(ProductRepositoryInterface)
            # Create product
            product = TestProduct.create_product()
            await product_repository.create(product)
            # Check it
            product_data = await product_repository.get_by_id(product.id)
            TestProduct.check_product(product_data)

    async def test_delete_product(self, container: AsyncContainer) -> None:
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

    async def test_get_many_products(self, container: AsyncContainer) -> None:
        async with container() as di_container:
            product_repository = await di_container.get(ProductRepositoryInterface)
            # Create products
            product = TestProduct.create_product()
            await product_repository.create(product)
            # Check products
            products = await product_repository.get_many()
            assert len(products) == 1
            products = await product_repository.get_many(
                name="test_product",
            )
            assert len(products) == 1

    async def test_count(self, container: AsyncContainer) -> None:
        async with container() as di_container:
            product_repository = await di_container.get(ProductRepositoryInterface)
            # Create products
            product = TestProduct.create_product()
            await product_repository.create(product)
            count = await product_repository.count()
            assert count == 1
            count = await product_repository.count(name="test_product")
            assert count == 1
