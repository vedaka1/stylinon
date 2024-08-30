from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column
from src.domain.users.entities import User, UserRole
from src.infrastructure.persistence.postgresql.models.base import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    mobile_phone: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    role: Mapped[UserRole] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"UserModel({self.__dict__})"


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
