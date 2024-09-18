from dataclasses import dataclass

from src.application.common.interfaces.transaction import TransactionManagerInterface
from src.application.products.commands import CreateProductCommand
from src.domain.products.entities import Product
from src.domain.products.service import ProductServiceInterface


@dataclass
class CreateProductUseCase:
    product_service: ProductServiceInterface
    transaction_manager: TransactionManagerInterface

    async def execute(self, command: CreateProductCommand) -> None:
        product = Product.create(
            name=command.name,
            category=command.category,
            description=command.description,
            price=command.price,
            units_of_measurement=command.units_of_measurement,
        )
        await self.product_service.create(product)
        await self.transaction_manager.commit()
        return None
