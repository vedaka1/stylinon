from uuid import UUID

from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.application.auth.dto import RefreshSession
from src.application.common.interfaces.refresh import RefreshTokenRepositoryInterface
from src.infrastructure.persistence.postgresql.models.auth import (
    RefreshSessionModel,
    map_to_refresh_session,
)


class SqlalchemyRefreshTokenRepository(RefreshTokenRepositoryInterface):

    slots = ("session",)

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, refresh_session: RefreshSession) -> None:
        query = insert(RefreshSessionModel).values(
            user_id=refresh_session.user_id,
            refresh_token=refresh_session.refresh_token,
            expires_at=refresh_session.expires_at,
            user_agent=refresh_session.user_agent,
        )
        await self.session.execute(query)
        return None

    async def delete_by_token(self, refresh_token: str) -> None:
        query = delete(RefreshSessionModel).where(
            RefreshSessionModel.refresh_token == refresh_token,
        )
        await self.session.execute(query)
        return None

    async def delete_by_user_id(self, user_id: UUID) -> None:
        query = delete(RefreshSessionModel).where(
            RefreshSessionModel.user_id == user_id,
        )
        await self.session.execute(query)
        return None

    async def get(self, refresh_token: str) -> RefreshSession | None:
        query = select(RefreshSessionModel).where(
            RefreshSessionModel.refresh_token == refresh_token,
        )
        cursor = await self.session.execute(query)
        entity = cursor.scalar_one_or_none()
        return map_to_refresh_session(entity) if entity else None

    async def get_by_user_id_and_user_agent(
        self,
        user_id: UUID,
        user_agent: str,
    ) -> RefreshSession | None:
        query = (
            select(RefreshSessionModel)
            .where(RefreshSessionModel.user_id == user_id)
            .where(RefreshSessionModel.user_agent == user_agent)
        )
        cursor = await self.session.execute(query)
        entity = cursor.scalar_one_or_none()
        return map_to_refresh_session(entity) if entity else None
