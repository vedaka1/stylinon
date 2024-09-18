from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class TransactionManagerInterface(ABC):
    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...

    @abstractmethod
    async def close(self) -> None: ...
