from datetime import datetime
from uuid import UUID

from fastapi import Request
from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.domain.users.entities import User, UserRole, UserSession
from src.infrastructure.persistence.postgresql.models.base import Base


class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    mobile_phone: Mapped[str] = mapped_column(nullable=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    role: Mapped[UserRole] = mapped_column(nullable=False)

    sessions: Mapped[list['UserSessionModel']] = relationship(back_populates='user')

    def __admin_repr__(self, request: Request) -> str:
        return f'{self.email}'

    def __repr__(self) -> str:
        return f'UserModel({self.__dict__})'


def map_to_user(entity: UserModel) -> User:
    return User(
        id=entity.id,
        email=entity.email,
        hashed_password=entity.hashed_password,
        mobile_phone=entity.mobile_phone,
        first_name=entity.first_name,
        last_name=entity.last_name,
        is_verified=entity.is_verified,
        role=entity.role,
    )


class UserSessionModel(Base):
    __tablename__ = 'user_sessions'
    id: Mapped[UUID] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), nullable=False)
    expires_in: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), nullable=False)
    user_agent: Mapped[str] = mapped_column(nullable=False)

    user: Mapped['UserModel'] = relationship(back_populates='sessions')


def map_to_user_session(
    entity: UserSessionModel,
    with_relations: bool = False,
) -> UserSession:
    session = UserSession(
        id=entity.id,
        user_id=entity.user_id,
        created_at=entity.created_at,
        expires_in=entity.expires_in,
        user_agent=entity.user_agent,
    )
    if with_relations:
        session.user = map_to_user(entity.user)
    return session
