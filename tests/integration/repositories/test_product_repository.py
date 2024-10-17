import pytest
from dishka import AsyncContainer
from src.application.products.filters import ProductFilters
from src.domain.products.entities import (
    Category,
    Product,
    ProductStatus,
    ProductVariant,
    UnitsOfMesaurement,
)
from src.domain.products.repository import (
    CategoryRepositoryInterface,
    ProductRepositoryInterface,
    ProductVariantRepositoryInterface,
)

pytestmark = pytest.mark.asyncio(loop_scope="session")


class TestProduct:
    @staticmethod
    def create_product() -> Product:
        return Product.create(
            name="test_product",
            description="test_description",
            category="test_category",
            units_of_measurement=UnitsOfMesaurement.PIECE,
        )

    @staticmethod
    def check_product(product_data: Product | None) -> None:
        assert product_data
        assert product_data.name == "test_product"
        assert product_data.description == "test_description"
        assert product_data.category == "test_category"
        assert product_data.units_of_measurement == UnitsOfMesaurement.PIECE


class TestProductRepository:
    async def test_create_product(self, container: AsyncContainer) -> None:
        async with container() as di_container:

            product_repository = await di_container.get(ProductRepositoryInterface)
            category_repository = await di_container.get(CategoryRepositoryInterface)
            # Create product
            product = TestProduct.create_product()
            category = Category.create(name="test_category")

            await category_repository.create(category)
            await product_repository.create(product)

            # Check it
            product_data = await product_repository.get_by_id(product.id)

            TestProduct.check_product(product_data)

    # async def test_create_many_products(self, container: AsyncContainer) -> None:
    #     async with container() as di_container:
    #         product_repository = await di_container.get(ProductRepositoryInterface)
    #         # Create product
    #         products = [
    #             Product.create(
    #                 name=f"test_product{i}",
    #                 description=f"test_description{i}",
    #                 price=100,
    #                 category=f"test_category{i}",
    #                 units_of_measurement=UnitsOfMesaurement.PIECE,
    #             )
    #             for i in range(10)
    #         ]
    #         await product_repository.create_many(products)
    #         # Check it
    #         products_data = await product_repository.get_many()
    #         assert len(products_data) == len(products)

    async def test_delete_product(self, container: AsyncContainer) -> None:
        async with container() as di_container:

            product_repository = await di_container.get(ProductRepositoryInterface)
            category_repository = await di_container.get(CategoryRepositoryInterface)
            # Create product
            product = TestProduct.create_product()
            category = Category.create(name="test_category")

            await category_repository.create(category)
            await product_repository.create(product)

            # Delete product
            await product_repository.delete(product.id)

            # Check it
            result = await product_repository.get_by_id(product.id)

            assert result is None

    async def test_get_many_products(self, container: AsyncContainer) -> None:
        async with container() as di_container:

            category_repository = await di_container.get(CategoryRepositoryInterface)
            product_repository = await di_container.get(ProductRepositoryInterface)
            product_variant_repository = await di_container.get(
                ProductVariantRepositoryInterface,
            )

            category = Category.create(name="test_category")
            product = TestProduct.create_product()
            product_variant = ProductVariant.create(
                product_id=product.id,
                name=f"test_product_variant_1",
                sku=f"test_sku_1",
                bag_weight=10,
                pallet_weight=100,
                bags_per_pallet=10,
                retail_price=100,
                wholesale_delivery_price=100,
                d2_delivery_price=100,
                d2_self_pickup_price=100,
                d1_delivery_price=100,
                d1_self_pickup_price=100,
                status=ProductStatus.INSTOCK,
            )

            # Create product
            await category_repository.create(category)
            await product_repository.create(product=product)
            await product_variant_repository.create(product_variant)

            # Check products
            products = await product_repository.get_many()

            assert len(products) == 1

            filters = ProductFilters(name="test_product")

            products = await product_repository.get_many(filters=filters)

            assert len(products) == 1

    async def test_count(self, container: AsyncContainer) -> None:
        async with container() as di_container:

            product_repository = await di_container.get(ProductRepositoryInterface)
            category_repository = await di_container.get(CategoryRepositoryInterface)
            product_variant_repository = await di_container.get(
                ProductVariantRepositoryInterface,
            )
            # Create product
            product = TestProduct.create_product()
            category = Category.create(name="test_category")
            product_variant = ProductVariant.create(
                product_id=product.id,
                name=f"test_product_variant_1",
                sku=f"test_sku_1",
                bag_weight=10,
                pallet_weight=100,
                bags_per_pallet=10,
                retail_price=100,
                wholesale_delivery_price=100,
                d2_delivery_price=100,
                d2_self_pickup_price=100,
                d1_delivery_price=100,
                d1_self_pickup_price=100,
                status=ProductStatus.INSTOCK,
            )

            await category_repository.create(category)
            await product_repository.create(product)
            await product_variant_repository.create(product_variant)

            count = await product_repository.count()

            assert count == 1

            filters = ProductFilters(name="test_product")

            count = await product_repository.count(filters=filters)

            assert count == 1
