from decimal import Decimal
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.transaction import TransactionCreate
from app.models.transaction import TransactionType

class TransactionService:
    def __init__(self, repo: TransactionRepository):
        self.repo = repo

    async def buy(self, portfolio_id: int, asset_id: int, quantity: Decimal, price: Decimal, **kwargs):
        data = TransactionCreate(
            portfolio_id=portfolio_id,
            asset_id=asset_id,
            transaction_type=TransactionType.BUY,
            quantity=quantity,
            price=price,
            **kwargs
        )
        return await self.repo.create(data)

    async def sell(self, portfolio_id: int, asset_id: int, quantity: Decimal, price: Decimal, **kwargs):
        # здесь позже добавить проверку — есть ли столько актива в портфеле
        data = TransactionCreate(
            portfolio_id=portfolio_id,
            asset_id=asset_id,
            transaction_type=TransactionType.SELL,
            quantity=quantity,
            price=price,
            **kwargs
        )
        return await self.repo.create(data)

    async def get_portfolio_transactions(self, portfolio_id: int):
        return await self.repo.get_by_portfolio(portfolio_id)