from dataclasses import dataclass

from src.application.common.interfaces.transaction import TransactionManagerInterface
from src.application.products.commands import (
    CreateCategoryCommand,
    CreateProductCommand,
)
from src.domain.products.entities import Category, Product, ProductVariant
from src.domain.products.repository import (
    CategoryRepositoryInterface,
    ProductRepositoryInterface,
    ProductVariantRepositoryInterface,
)


@dataclass
class CreateProductUseCase:

    product_repository: ProductRepositoryInterface
    product_variant_repository: ProductVariantRepositoryInterface
    # sku_repository: SkuRepositoryInterface
    transaction_manager: TransactionManagerInterface

    async def execute(self, command: CreateProductCommand) -> None:
        product = Product.create(
            name=command.name,
            category=command.category,
            description=command.description,
            units_of_measurement=command.units_of_measurement,
        )

        await self.product_repository.create(product=product)

        for variant in command.variants:
            product_variant = ProductVariant.create(
                name=variant.name,
                sku=variant.sku,
                bag_weight=variant.bag_weight,
                product_id=product.id,
                pallet_weight=variant.pallet_weight,
                bags_per_pallet=variant.bags_per_pallet,
                retail_price=variant.retail_price,
                wholesale_delivery_price=variant.wholesale_delivery_price,
                d1_delivery_price=variant.d1_delivery_price,
                d1_self_pickup_price=variant.d1_self_pickup_price,
                d2_delivery_price=variant.d2_delivery_price,
                d2_self_pickup_price=variant.d2_self_pickup_price,
            )

            await self.product_variant_repository.create(
                product_variant=product_variant,
            )

        await self.transaction_manager.commit()

        return None


@dataclass
class CreateCategoryUseCase:

    category_repository: CategoryRepositoryInterface
    transaction_manager: TransactionManagerInterface

    async def execute(self, command: CreateCategoryCommand) -> None:
        category = Category.create(name=command.name)

        await self.category_repository.create(category=category)

        await self.transaction_manager.commit()

        return None
