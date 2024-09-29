from dataclasses import dataclass

from src.application.common.interfaces.transaction import TransactionManagerInterface
from src.application.products.commands import UpdateProductCommand
from src.domain.products.entities import Product
from src.domain.products.service import ProductServiceInterface


@dataclass
class CreateProductUseCase:
    product_service: ProductServiceInterface
    transaction_manager: TransactionManagerInterface

    async def execute(self, command: UpdateProductCommand) -> None:
        await self.product_service.update(
            product_id=command.product_id,
            name=command.name,
            category=command.category,
            description=command.description,
            price=command.price,
            units_of_measurement=command.units_of_measurement,
            photo_url=command.photo_url,
        )
        await self.transaction_manager.commit()
        return None
