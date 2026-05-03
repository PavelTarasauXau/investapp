import asyncio
from datetime import date
from decimal import Decimal

from app.database.session import AsyncSessionLocal

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

from app.models.enums import AssetType, Currency, TransactionType, UserRole

from app.repositories.user_repository import UserRepository
from app.repositories.portfolio_repository import PortfolioRepository
from app.repositories.asset_repository import AssetRepository
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.dividend_payment_repository import DividendPaymentRepository
from app.repositories.coupon_payment_repository import CouponPaymentRepository


async def main():
    async with AsyncSessionLocal() as session:
        user_repo = UserRepository(session)
        portfolio_repo = PortfolioRepository(session)
        asset_repo = AssetRepository(session)
        transaction_repo = TransactionRepository(session)
        dividend_repo = DividendPaymentRepository(session)
        coupon_repo = CouponPaymentRepository(session)

        user = await user_repo.create(
            User(
                email="repo_test@example.com",
                full_name="Repository Test User",
                password_hash="fake_hash",
                user_role=UserRole.INVESTOR,
            )
        )
        print("User:", user.id, user.email)

        portfolio = await portfolio_repo.create(
            Portfolio(
                user_id=user.id,
                name="Test Portfolio",
                currency=Currency.USD,
                description="Portfolio for repository tests",
            )
        )
        print("Portfolio:", portfolio.id, portfolio.name)

        stock_asset = Asset(
            ticker="AAPL",
            name="Apple Inc.",
            isin="US0378331005",
            asset_type=AssetType.STOCK,
            description="Apple stock test asset",
        )

        stock = Stock(
            sector="Technology",
            shares_outstanding=15500000000,
            dividend_policy="Quarterly dividends",
        )

        stock_asset = await asset_repo.create_stock(stock_asset, stock)
        print("Stock asset:", stock_asset.id, stock_asset.ticker)

        bond_asset = Asset(
            ticker="US10Y",
            name="US Treasury 10Y",
            isin="US91282CJL62",
            asset_type=AssetType.BOND,
            description="Bond test asset",
        )

        bond = Bond(
            nominal_value=Decimal("1000.00"),
            coupon_rate=Decimal("4.25"),
            coupon_frequency=2,
            maturity_date=date(2034, 5, 15),
        )

        bond_asset = await asset_repo.create_bond(bond_asset, bond)
        print("Bond asset:", bond_asset.id, bond_asset.ticker)

        etf_asset = Asset(
            ticker="VOO",
            name="Vanguard S&P 500 ETF",
            isin="US9229083632",
            asset_type=AssetType.ETF,
            description="ETF test asset",
        )

        etf = ETF(
            provider="Vanguard",
            expense_ratio=Decimal("0.03"),
            benchmark_index="S&P 500",
            trading_currency="USD",
        )

        etf_asset = await asset_repo.create_etf(etf_asset, etf)
        print("ETF asset:", etf_asset.id, etf_asset.ticker)

        currency_asset = Asset(
            ticker="USD",
            name="US Dollar",
            isin=None,
            asset_type=AssetType.CURRENCY,
            description="Currency test asset",
        )

        currency = CurrencyAsset(
            iso4217="USD",
            country="United States",
            symbol="$",
        )

        currency_asset = await asset_repo.create_currency(currency_asset, currency)
        print("Currency asset:", currency_asset.id, currency_asset.ticker)

        buy_transaction = await transaction_repo.create(
            Transaction(
                portfolio_id=portfolio.id,
                asset_id=stock_asset.id,
                transaction_type=TransactionType.BUY,
                quantity=Decimal("10"),
                price=Decimal("180.50"),
                commission=Decimal("1.50"),
            )
        )
        print("Transaction:", buy_transaction.id, buy_transaction.transaction_type)

        dividend = await dividend_repo.create(
            DividendPayment(
                stock_id=stock_asset.id,
                record_date=date(2026, 5, 1),
                payment_date=date(2026, 5, 15),
                dividend_per_share=Decimal("0.25"),
            )
        )
        print("Dividend:", dividend.id, dividend.dividend_per_share)

        coupon = await coupon_repo.create(
            CouponPayment(
                bond_id=bond_asset.id,
                coupon_number=1,
                payment_date=date(2026, 6, 1),
                coupon_amount=Decimal("21.25"),
            )
        )
        print("Coupon:", coupon.id, coupon.coupon_amount)

        user_portfolios = await portfolio_repo.get_by_user_id(user.id)
        portfolio_transactions = await transaction_repo.get_by_portfolio_id(portfolio.id)
        stock_dividends = await dividend_repo.get_by_stock_id(stock_asset.id)
        bond_coupons = await coupon_repo.get_by_bond_id(bond_asset.id)

        print("User portfolios count:", len(user_portfolios))
        print("Portfolio transactions count:", len(portfolio_transactions))
        print("Stock dividends count:", len(stock_dividends))
        print("Bond coupons count:", len(bond_coupons))


if __name__ == "__main__":
    asyncio.run(main())