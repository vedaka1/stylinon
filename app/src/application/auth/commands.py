from dataclasses import dataclass

from pydantic import EmailStr


@dataclass
class RegisterCommand:
    email: EmailStr
    password: str
    mobile_phone: str | None = None
    first_name: str | None = None
    last_name: str | None = None


@dataclass
class LoginCommand:
    password: str
    username: str