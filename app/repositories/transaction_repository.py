from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import override
from app.models.transaction import Transaction
from app.repositories.abstract_repository import AbstractRepository
from app.models.enums import TransactionType

class TransactionRepository(AbstractRepository[Transaction]):
    def __init__(self, session: AsyncSession):
        self.session = session

    @override
    async def create(self, entity: Transaction) -> Transaction:
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    @override
    async def get_by_id(self, entity_id: int) -> Transaction | None:
        return await self.session.get(Transaction, entity_id)

    @override
    async def list_all(self) -> list[Transaction]:
        result = await self.session.execute(select(Transaction))
        return list(result.scalars().all())

    @override
    async def update(self, entity_id: int, data: dict) -> Transaction | None:
        transaction = await self.session.get(Transaction, entity_id)
        if transaction is None:
            return None
        for key, value in data.items():
            setattr(transaction, key, value)
        await self.session.commit()
        await self.session.refresh(transaction)
        return transaction

    @override
    async def delete(self, entity_id: int) -> bool:
        transaction = await self.session.get(Transaction, entity_id)
        if transaction is None:
            return False
        await self.session.delete(transaction)
        await self.session.commit()
        return True

    async def get_by_asset_id(self, asset_id: int) -> list[Transaction]:
        result = await self.session.execute(
            select(Transaction)
            .where(Transaction.asset_id == asset_id)
            .order_by(Transaction.transaction_date.desc())
        )
        return list(result.scalars().all())
    
    async def get_by_portfolio_id(self, portfolio_id: int) -> list[Transaction]:
        result = await self.session.execute(
            select(Transaction)
            .where(Transaction.portfolio_id == portfolio_id)
            .order_by(Transaction.transaction_date.desc())
        )
        return list(result.scalars().all())
    
    async def get_by_portfolio_and_asset(
        self,
        portfolio_id: int,
        asset_id: int
    ) -> list[Transaction]:
        result = await self.session.execute(
            select(Transaction)
            .where(
                Transaction.portfolio_id == portfolio_id,
                Transaction.asset_id == asset_id
            )
            .order_by(Transaction.transaction_date.desc())
        )
        return list(result.scalars().all())
    
    async def get_by_portfolio_id_and_type(
        self,
        portfolio_id: int,
        transaction_type: TransactionType,
    ) -> list[Transaction]:
        result = await self.session.execute(
            select(Transaction)
            .where(Transaction.portfolio_id == portfolio_id)
            .where(Transaction.transaction_type == transaction_type)
            .order_by(Transaction.transaction_date.desc())
        )

        return list(result.scalars().all())