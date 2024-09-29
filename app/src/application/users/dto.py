from dataclasses import dataclass

from src.domain.users.entities import UserRole


@dataclass
class UserOut:
    id: str
    email: str
    mobile_phone: str | None
    first_name: str | None
    last_name: str | None
    is_verified: bool
    role: UserRole
