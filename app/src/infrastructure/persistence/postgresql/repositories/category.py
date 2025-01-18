from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.products.entities import Category
from src.domain.products.repository import CategoryRepositoryInterface
from src.infrastructure.persistence.postgresql.models.product import (
    CategoryModel,
    map_to_category,
)


class SqlalchemyCategoryRepository(CategoryRepositoryInterface):
    __slots__ = ['session']

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, category: Category) -> None:
        query = insert(CategoryModel).values(name=category.name, is_available=category.is_available)
        await self.session.execute(query)
        return None

    async def update(self, category: Category) -> None:
        query = (
            update(CategoryModel)
            .where(CategoryModel.name == category.name)
            .values(name=category.name, is_available=category.is_available)
        )
        await self.session.execute(query)
        return None

    async def delete(self, category_name: str) -> None:
        query = delete(CategoryModel).where(CategoryModel.name == category_name)
        await self.session.execute(query)
        return None

    async def get_by_name(self, category_name: str) -> Category | None:
        query = select(CategoryModel).where(CategoryModel.name == category_name)
        cursor = await self.session.execute(query)
        entity = cursor.scalar_one_or_none()
        return map_to_category(entity) if entity else None

    async def get_many(self) -> list[Category]:
        query = select(CategoryModel)
        cursor = await self.session.execute(query)
        entity = cursor.scalars().all()
        return [map_to_category(entity) for entity in entity]

    async def count(self) -> int:
        query = select(func.count()).select_from(CategoryModel)
        cursor = await self.session.execute(query)
        count = cursor.scalar_one_or_none()
        return count if count else 0
