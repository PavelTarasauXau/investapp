from decimal import Decimal

from app.models.transaction import Transaction
from app.models.enums import TransactionType

from app.repositories.transaction_repository import TransactionRepository
from app.repositories.portfolio_repository import PortfolioRepository
from app.repositories.asset_repository import AssetRepository

from app.schemas.transaction import TransactionCreate
from app.models.enums import TransactionType

class TransactionService:
    def __init__(
        self,
        transaction_repo: TransactionRepository,
        portfolio_repo: PortfolioRepository,
        asset_repo: AssetRepository,
    ):
        self.transaction_repo = transaction_repo
        self.portfolio_repo = portfolio_repo
        self.asset_repo = asset_repo

    async def create_transaction(self, data: TransactionCreate) -> Transaction:
        portfolio = await self.portfolio_repo.get_by_id(data.portfolio_id)
        if portfolio is None:
            raise ValueError("Portfolio not found")

        asset = await self.asset_repo.get_by_id(data.asset_id)
        if asset is None:
            raise ValueError("Asset not found")

        if data.transaction_type == TransactionType.SELL:
            current_position = await self.calculate_asset_position(
                portfolio_id=data.portfolio_id,
                asset_id=data.asset_id,
            )

            if data.quantity > current_position:
                raise ValueError("Cannot sell more assets than portfolio contains")

        transaction = Transaction(
            portfolio_id=data.portfolio_id,
            asset_id=data.asset_id,
            transaction_type=data.transaction_type,
            quantity=data.quantity,
            price=data.price,
            commission=data.commission,
            transaction_date=data.transaction_date,
        )

        return await self.transaction_repo.create(transaction)

    async def buy_asset(self, data: TransactionCreate) -> Transaction:
        data.transaction_type = TransactionType.BUY
        return await self.create_transaction(data)

    async def sell_asset(self, data: TransactionCreate) -> Transaction:
        data.transaction_type = TransactionType.SELL
        return await self.create_transaction(data)

    async def get_portfolio_transactions(self, portfolio_id: int) -> list[Transaction]:
        portfolio = await self.portfolio_repo.get_by_id(portfolio_id)
        if portfolio is None:
            raise ValueError("Portfolio not found")

        return await self.transaction_repo.get_by_portfolio_id(portfolio_id)

    async def get_asset_transactions(self, asset_id: int) -> list[Transaction]:
        asset = await self.asset_repo.get_by_id(asset_id)
        if asset is None:
            raise ValueError("Asset not found")

        return await self.transaction_repo.get_by_asset_id(asset_id)

    async def calculate_asset_position(
        self,
        portfolio_id: int,
        asset_id: int,
    ) -> Decimal:
        transactions = await self.transaction_repo.get_by_portfolio_and_asset(
            portfolio_id=portfolio_id,
            asset_id=asset_id,
        )

        position = Decimal("0")

        for transaction in transactions:
            if transaction.transaction_type == TransactionType.BUY:
                position += transaction.quantity
            elif transaction.transaction_type == TransactionType.SELL:
                position -= transaction.quantity

        return position
    
    async def get_portfolio_transactions_by_type(
        self,
        portfolio_id: int,
        transaction_type: TransactionType,
    ):
        portfolio = await self.portfolio_repo.get_by_id(portfolio_id)

        if portfolio is None:
            raise ValueError("Portfolio not found")

        return await self.transaction_repo.get_by_portfolio_id_and_type(
            portfolio_id,
            transaction_type,
        )