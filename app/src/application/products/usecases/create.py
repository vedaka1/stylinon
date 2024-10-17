from dataclasses import dataclass

from src.application.common.interfaces.transaction import TransactionManagerInterface
from src.application.common.utils import parse_price
from src.application.products.commands import (
    CreateCategoryCommand,
    CreateProductCommand,
)
from src.domain.products.entities import Category, Product
from src.domain.products.repository import (
    CategoryRepositoryInterface,
    ProductRepositoryInterface,
)
from src.domain.products.value_objects import ProductPrice


@dataclass
class CreateProductUseCase:

    product_repository: ProductRepositoryInterface
    transaction_manager: TransactionManagerInterface

    async def execute(self, command: CreateProductCommand) -> None:

        product = Product.create(
            name=command.name,
            category=command.category.lower(),
            description=command.description,
            units_of_measurement=command.units_of_measurement,
            sku=command.sku,
            bag_weight=command.bag_weight,
            pallet_weight=command.pallet_weight,
            bags_per_pallet=command.bags_per_pallet,
            retail_price=ProductPrice(command.retail_price),
            wholesale_delivery_price=parse_price(command.wholesale_delivery_price),
            d1_delivery_price=parse_price(command.d1_delivery_price),
            d1_self_pickup_price=parse_price(command.d1_self_pickup_price),
            d2_delivery_price=parse_price(command.d2_delivery_price),
            d2_self_pickup_price=parse_price(command.d2_self_pickup_price),
            image=command.image,
        )

        await self.product_repository.create(product=product)

        await self.transaction_manager.commit()

        return None


@dataclass
class CreateCategoryUseCase:

    category_repository: CategoryRepositoryInterface
    transaction_manager: TransactionManagerInterface

    async def execute(self, command: CreateCategoryCommand) -> None:
        category = Category.create(name=command.name.lower())

        await self.category_repository.create(category=category)

        await self.transaction_manager.commit()

        return None
