from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import override
from app.models.coupon_payment import CouponPayment
from app.repositories.abstract_repository import AbstractRepository

class CouponPaymentRepository(AbstractRepository[CouponPayment]):
    def __init__(self, session: AsyncSession):
        self.session = session

    @override
    async def create(self, entity: CouponPayment) -> CouponPayment:
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    @override
    async def get_by_id(self, entity_id: int) -> CouponPayment | None:
        return await self.session.get(CouponPayment, entity_id)

    @override
    async def list_all(self) -> list[CouponPayment]:
        result = await self.session.execute(select(CouponPayment))
        return list(result.scalars().all())

    @override
    async def update(self, entity_id: int, data: dict) -> CouponPayment | None:
        payment = await self.session.get(CouponPayment, entity_id)
        if payment is None:
            return None
        for key, value in data.items():
            setattr(payment, key, value)
        await self.session.commit()
        await self.session.refresh(payment)
        return payment

    @override
    async def delete(self, entity_id: int) -> bool:
        payment = await self.session.get(CouponPayment, entity_id)
        if payment is None:
            return False
        await self.session.delete(payment)
        await self.session.commit()
        return True

    async def get_by_bond_id(self, bond_id: int) -> list[CouponPayment]:
        result = await self.session.execute(
            select(CouponPayment).where(CouponPayment.bond_id == bond_id)
        )
        return list(result.scalars().all())