from dataclasses import dataclass

from src.application.common.interfaces.transaction import TransactionManagerInterface
from src.application.products.commands import CreateProductCommand
from src.domain.products.entities import Product
from src.domain.products.repository import ProductRepositoryInterface
from src.domain.products.value_objects import ProductPrice


@dataclass
class CreateProductUseCase:

    product_repository: ProductRepositoryInterface
    transaction_manager: TransactionManagerInterface

    async def execute(self, command: CreateProductCommand) -> None:
        product = Product.create(
            name=command.name,
            category=command.category,
            description=command.description,
            price=command.price * 100,
            units_of_measurement=command.units_of_measurement,
            photo_url=command.photo_url,
        )

        await self.product_repository.create(product)

        await self.transaction_manager.commit()

        return None
