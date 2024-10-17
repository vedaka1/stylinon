from dataclasses import dataclass

from src.application.common.interfaces.transaction import TransactionManagerInterface
from src.domain.products.repository import CategoryRepositoryInterface


@dataclass
class DeleteCategoryUseCase:

    category_repository: CategoryRepositoryInterface
    transaction_manager: TransactionManagerInterface

    async def execute(self, category_name: str) -> None:
        await self.category_repository.delete(category_name=category_name)

        await self.transaction_manager.commit()

        return None
