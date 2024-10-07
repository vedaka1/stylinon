from uuid import UUID

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from src.domain.users.entities import UserSession
from src.domain.users.repository import UserSessionRepositoryInterface
from src.infrastructure.persistence.postgresql.models.user import (
    UserSessionModel,
    map_to_user_session,
)


class SqlalchemyUserSessionRepository(UserSessionRepositoryInterface):

    __slots__ = ("session",)

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, session: UserSession) -> None:
        query = insert(UserSessionModel).values(
            id=session.id,
            user_id=session.user_id,
            created_at=session.created_at,
            expires_in=session.expires_in,
        )

        await self.session.execute(query)

        return None

    async def update(self, session: UserSession) -> None:
        query = update(UserSessionModel).values(
            expires_in=session.expires_in,
        )

        await self.session.execute(query)

        return None

    async def delete(self, session_id: UUID) -> None:
        query = delete(UserSessionModel).where(UserSessionModel.id == session_id)

        await self.session.execute(query)

        return None

    async def delete_by_user_id(self, user_id: UUID) -> None:
        query = delete(UserSessionModel).where(UserSessionModel.user_id == user_id)

        await self.session.execute(query)

        return None

    async def get_by_id(self, session_id: UUID) -> UserSession | None:
        query = (
            select(UserSessionModel)
            .where(UserSessionModel.id == session_id)
            .options(joinedload(UserSessionModel.user))
        )

        cursor = await self.session.execute(query)

        entity = cursor.scalar_one_or_none()

        return map_to_user_session(entity, with_relations=True) if entity else None

    async def get_by_user_id(self, user_id: UUID) -> list[UserSession]:
        query = select(UserSessionModel).where(UserSessionModel.user_id == user_id)

        cursor = await self.session.execute(query)

        entities = cursor.scalars().all()

        return [map_to_user_session(entity) for entity in entities]
