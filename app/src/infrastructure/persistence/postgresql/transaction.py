from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession
from src.application.common.interfaces.transaction import ICommiter


@dataclass
class Commiter(ICommiter):
    session: AsyncSession

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def close(self) -> None:
        await self.session.close()
