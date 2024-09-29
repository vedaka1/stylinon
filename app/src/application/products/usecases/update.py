from dataclasses import dataclass

from src.application.common.interfaces.transaction import TransactionManagerInterface
from src.application.products.commands import UpdateProductCommand
from src.domain.products.exceptions import ProductNotFoundException
from src.domain.products.repository import ProductRepositoryInterface
from src.domain.products.value_objects import ProductPrice


@dataclass
class UpdateProductUseCase:

    product_repository: ProductRepositoryInterface
    transaction_manager: TransactionManagerInterface

    async def execute(self, command: UpdateProductCommand) -> None:
        product = await self.product_repository.get_by_id(product_id=command.product_id)

        if not product:
            raise ProductNotFoundException

        if command.name:
            product.name = command.name
        if command.category:
            product.category = command.category
        if command.description:
            product.description = command.description
        if command.price:
            product.price = ProductPrice(command.price)
        if command.units_of_measurement:
            product.units_of_measurement = command.units_of_measurement
        if command.photo_url:
            product.photo_url = command.photo_url

        await self.product_repository.update(product=product)

        await self.transaction_manager.commit()

        return None
