from typing import cast

from passlib.context import CryptContext
from src.application.common.password_hasher import PasswordHasherInterface

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordHasher(PasswordHasherInterface):

    def hash(self, password: str) -> str:
        return cast(str, pwd_context.hash(password))

    def verify(self, password: str, hash: str) -> bool:
        return cast(bool, pwd_context.verify(password, hash))
