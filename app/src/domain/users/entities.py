from dataclasses import dataclass
from enum import Enum
from uuid import UUID, uuid4


class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
    MANAGER = "manager"


@dataclass
class User:
    id: UUID
    email: str
    hashed_password: str
    mobile_phone: str | None
    first_name: str | None
    last_name: str | None
    is_verified: bool
    role: UserRole

    @staticmethod
    def create(
        email: str,
        hashed_password: str,
        mobile_phone: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        is_verified: bool = False,
    ) -> "User":
        return User(
            id=uuid4(),
            email=email,
            hashed_password=hashed_password,
            mobile_phone=mobile_phone,
            first_name=first_name,
            last_name=last_name,
            is_verified=is_verified,
            role=UserRole.USER,
        )
