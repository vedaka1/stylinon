from abc import ABC, abstractmethod
from uuid import UUID


class JwtTokenProcessorInterface(ABC):

    @abstractmethod
    def generate_token(self, user_id: UUID) -> str: ...

    @abstractmethod
    def validate_token(self, token: str) -> UUID | None: ...
