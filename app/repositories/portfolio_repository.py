from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import override
from app.models.portfolio import Portfolio
from app.repositories.abstract_repository import AbstractRepository

class PortfolioRepository(AbstractRepository[Portfolio]):
    def __init__(self, session: AsyncSession):
        self.session = session

    @override
    async def create(self, entity: Portfolio) -> Portfolio:
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    @override
    async def get_by_id(self, entity_id: int) -> Portfolio | None:
        return await self.session.get(Portfolio, entity_id)

    @override
    async def list_all(self) -> list[Portfolio]:
        result = await self.session.execute(select(Portfolio))
        return list(result.scalars().all())

    @override
    async def update(self, entity_id: int, data: dict) -> Portfolio | None:
        portfolio = await self.session.get(Portfolio, entity_id)
        if portfolio is None:
            return None
        for key, value in data.items():
            setattr(portfolio, key, value)
        await self.session.commit()
        await self.session.refresh(portfolio)
        return portfolio

    @override
    async def delete(self, entity_id: int) -> bool:
        portfolio = await self.session.get(Portfolio, entity_id)
        if portfolio is None:
            return False
        await self.session.delete(portfolio)
        await self.session.commit()
        return True

    async def get_by_user_id(self, user_id: int) -> list[Portfolio]:
        result = await self.session.execute(
            select(Portfolio).where(Portfolio.user_id == user_id)
        )
        return list(result.scalars().all())