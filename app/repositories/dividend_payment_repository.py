from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import override
from app.models.dividend_payment import DividendPayment
from app.repositories.abstract_repository import AbstractRepository

class DividendPaymentRepository(AbstractRepository[DividendPayment]):
    def __init__(self, session: AsyncSession):
        self.session = session

    @override
    async def create(self, entity: DividendPayment) -> DividendPayment:
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    @override
    async def get_by_id(self, entity_id: int) -> DividendPayment | None:
        return await self.session.get(DividendPayment, entity_id)

    @override
    async def list_all(self) -> list[DividendPayment]:
        result = await self.session.execute(select(DividendPayment))
        return list(result.scalars().all())

    @override
    async def update(self, entity_id: int, data: dict) -> DividendPayment | None:
        payment = await self.session.get(DividendPayment, entity_id)
        if payment is None:
            return None
        for key, value in data.items():
            setattr(payment, key, value)
        await self.session.commit()
        await self.session.refresh(payment)
        return payment

    @override
    async def delete(self, entity_id: int) -> bool:
        payment = await self.session.get(DividendPayment, entity_id)
        if payment is None:
            return False
        await self.session.delete(payment)
        await self.session.commit()
        return True
    
    async def get_by_stock_id(self, stock_id: int) -> list[DividendPayment]:
        result = await self.session.execute(
            select(DividendPayment)
            .where(DividendPayment.stock_id == stock_id)
            .order_by(DividendPayment.payment_date.asc())
        )
        return list(result.scalars().all())