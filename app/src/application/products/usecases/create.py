from dataclasses import dataclass

from src.application.common.interfaces.transaction import ICommiter
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
    commiter: ICommiter

    async def execute(self, command: CreateProductCommand) -> None:
        category_name = command.category.lower().replace(r'/', '-')

        product = Product.create(
            name=command.name.replace('/', '-'),
            category=category_name,
            description=command.description,
            units_of_measurement=command.units_of_measurement,
            sku=command.sku,
            weight=command.weight,
            collection=command.collection,
            size=command.size,
            retail_price=ProductPrice(command.retail_price),
            wholesale_price=parse_price(command.wholesale_price),
            d1_delivery_price=parse_price(command.d1_delivery_price),
            d1_self_pickup_price=parse_price(command.d1_self_pickup_price),
            image=command.image,
        )

        await self.product_repository.create(product=product)
        await self.commiter.commit()

        return None


@dataclass
class CreateCategoryUseCase:
    category_repository: CategoryRepositoryInterface
    commiter: ICommiter

    async def execute(self, command: CreateCategoryCommand) -> None:
        category_name = command.name.lower().replace(r'/', '-')
        category = Category.create(name=category_name)

        await self.category_repository.create(category=category)
        await self.commiter.commit()

        return None
