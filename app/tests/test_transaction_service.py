import asyncio
from decimal import Decimal
from uuid import uuid4

from app.database.session import AsyncSessionLocal

from app.models.enums import * 
from app.models.user import User
from app.models.portfolio import Portfolio
from app.models.asset import Asset
from app.models.stock import Stock
from app.models.bond import Bond
from app.models.etf import ETF
from app.models.currency_asset import CurrencyAsset
from app.models.transaction import Transaction
from app.models.dividend_payment import DividendPayment
from app.models.coupon_payment import CouponPayment

from app.repositories.user_repository import UserRepository
from app.repositories.portfolio_repository import PortfolioRepository
from app.repositories.asset_repository import AssetRepository
from app.repositories.transaction_repository import TransactionRepository

from app.services.transaction_service import TransactionService

from app.schemas.transaction import TransactionCreate


async def main():
    suffix = uuid4().hex[:6].upper()

    async with AsyncSessionLocal() as session:
        user_repo = UserRepository(session)
        portfolio_repo = PortfolioRepository(session)
        asset_repo = AssetRepository(session)
        transaction_repo = TransactionRepository(session)

        transaction_service = TransactionService(
            transaction_repo=transaction_repo,
            portfolio_repo=portfolio_repo,
            asset_repo=asset_repo,
        )

        user = await user_repo.create(
            User(
                email=f"transaction_test_{suffix}@example.com",
                full_name="Transaction Test User",
                password_hash="fake_hash",
                user_role=UserRole.INVESTOR,
            )
        )

        portfolio = await portfolio_repo.create(
            Portfolio(
                user_id=user.id,
                name="Transaction Test Portfolio",
                currency=Currency.USD,
                description="Portfolio for transaction service test",
            )
        )

        asset = Asset(
            ticker=f"AAPL_{suffix}",
            name="Apple Inc.",
            isin=None,
            asset_type=AssetType.STOCK,
            description="Apple stock for transaction test",
        )

        stock = Stock(
            sector="Technology",
            shares_outstanding=15500000000,
            dividend_policy="Quarterly dividends",
        )

        asset = await asset_repo.create_stock(asset, stock)

        buy_transaction = await transaction_service.create_transaction(
            TransactionCreate(
                portfolio_id=portfolio.id,
                asset_id=asset.id,
                transaction_type=TransactionType.BUY,
                quantity=Decimal("10"),
                price=Decimal("180.50"),
                commission=Decimal("1.50"),
            )
        )

        print(
            "Buy transaction:",
            buy_transaction.id,
            buy_transaction.transaction_type,
            buy_transaction.quantity,
        )

        position_after_buy = await transaction_service.calculate_asset_position(
            portfolio_id=portfolio.id,
            asset_id=asset.id,
        )

        print("Position after buy:", position_after_buy)

        sell_transaction = await transaction_service.create_transaction(
            TransactionCreate(
                portfolio_id=portfolio.id,
                asset_id=asset.id,
                transaction_type=TransactionType.SELL,
                quantity=Decimal("3"),
                price=Decimal("190.00"),
                commission=Decimal("1.00"),
            )
        )

        print(
            "Sell transaction:",
            sell_transaction.id,
            sell_transaction.transaction_type,
            sell_transaction.quantity,
        )

        position_after_sell = await transaction_service.calculate_asset_position(
            portfolio_id=portfolio.id,
            asset_id=asset.id,
        )

        print("Position after sell:", position_after_sell)

        try:
            await transaction_service.create_transaction(
                TransactionCreate(
                    portfolio_id=portfolio.id,
                    asset_id=asset.id,
                    transaction_type=TransactionType.SELL,
                    quantity=Decimal("100"),
                    price=Decimal("200.00"),
                    commission=Decimal("1.00"),
                )
            )
        except ValueError as e:
            print("Oversell caught correctly:", e)

        transactions = await transaction_service.get_portfolio_transactions(
            portfolio_id=portfolio.id
        )

        print("Portfolio transactions count:", len(transactions))


if __name__ == "__main__":
    asyncio.run(main())