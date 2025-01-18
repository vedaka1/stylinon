import logging
from dataclasses import dataclass

from src.application.common.interfaces.transaction import ICommiter
from src.application.products.commands import UpdateProductCommand
from src.domain.products.exceptions import ProductNotFoundException
from src.domain.products.repository import ProductRepositoryInterface
from src.domain.products.value_objects import ProductPrice

logger = logging.getLogger()


@dataclass
class UpdateProductUseCase:
    product_repository: ProductRepositoryInterface
    commiter: ICommiter

    async def execute(self, command: UpdateProductCommand) -> None:
        product = await self.product_repository.get_by_id(product_id=command.product_id)
        if not product:
            raise ProductNotFoundException

        for key, value in command.__dict__.items():
            if value:
                if key == 'price':
                    setattr(product, key, ProductPrice.from_rubles(value))
                else:
                    setattr(product, key, value)

        await self.product_repository.update(product=product)
        await self.commiter.commit()

        return None
