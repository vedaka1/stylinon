from uuid import UUID

from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.users.entities import User
from src.domain.users.repository import UserPrimaryKey, UserRepositoryInterface
from src.infrastructure.persistence.postgresql.models.user import UserModel, map_to_user


class SqlalchemyUserRepository(UserRepositoryInterface):
    __slots__ = ("session",)

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user: User) -> None:
        query = insert(UserModel).values(
            id=user.id,
            email=user.email,
            hashed_password=user.hashed_password,
            mobile_phone=user.mobile_phone,
            first_name=user.first_name,
            last_name=user.last_name,
            is_verified=user.is_verified,
            role=user.role,
        )
        await self.session.execute(query)
        return None

    async def update(self, user: User) -> None:
        query = (
            update(UserModel)
            .where(UserModel.id == user.id)
            .values(
                first_name=user.first_name,
                last_name=user.last_name,
                is_verified=user.is_verified,
            )
        )
        await self.session.execute(query)
        return None

    async def delete(self, user_id: UUID) -> None:
        query = delete(UserModel).where(UserModel.id == user_id)
        await self.session.execute(query)
        return None

    async def _get_by(self, key: UserPrimaryKey, value: UUID | str) -> User | None:
        query = select(UserModel)
        if key == UserPrimaryKey.ID:
            query = query.where(UserModel.id == value)
        elif key == UserPrimaryKey.EMAIL:
            query = query.where(UserModel.email == value)
        cursor = await self.session.execute(query)
        entity = cursor.scalar_one_or_none()
        return map_to_user(entity) if entity else None

    async def get_by_id(self, user_id: UUID) -> User | None:
        return await self._get_by(key=UserPrimaryKey.ID, value=user_id)

    async def get_by_email(self, email: str) -> User | None:
        return await self._get_by(key=UserPrimaryKey.EMAIL, value=email)

    async def get_many(
        self,
        search: str | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> list[User]:
        query = select(UserModel)
        if search:
            query = query.where(UserModel.email.ilike(f"%{search}%"))
        query = query.limit(limit).offset(offset)
        cursor = await self.session.execute(query)
        entities = cursor.scalars().all()
        return [map_to_user(entity) for entity in entities]

    async def count(self, search: str | None = None) -> int:
        query = select(func.count()).select_from(UserModel)
        if search:
            query = query.where(UserModel.email.ilike(f"%{search}%"))
        cursor = await self.session.execute(query)
        count = cursor.scalar_one_or_none()
        return count if count else 0
