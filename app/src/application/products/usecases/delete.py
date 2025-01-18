from dataclasses import dataclass

from src.application.common.interfaces.transaction import ICommiter
from src.domain.products.repository import CategoryRepositoryInterface


@dataclass
class DeleteCategoryUseCase:
    category_repository: CategoryRepositoryInterface
    commiter: ICommiter

    async def execute(self, category_name: str) -> None:
        await self.category_repository.delete(category_name=category_name)
        await self.commiter.commit()

        return None
