from datetime import datetime
from math import exp
from uuid import UUID

from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.application.auth.dto import RefreshSession
from src.infrastructure.persistence.postgresql.models.base import Base


class RefreshSessionModel(Base):
    __tablename__ = "refresh_session"

    refresh_token: Mapped[str] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    expires_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"RefreshSessionModel({self.__dict__})"


def map_to_refresh_session(entity: RefreshSessionModel) -> RefreshSession:
    return RefreshSession(
        refresh_token=entity.refresh_token,
        user_id=entity.user_id,
        expires_at=entity.expires_at,
    )
