from abc import ABC, abstractmethod


class PasswordHasherInterface(ABC):

    @abstractmethod
    def hash(self, password: str) -> str: ...

    @abstractmethod
    def verify(self, password: str, hash: str) -> bool: ...
