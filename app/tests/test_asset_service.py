import asyncio
from datetime import date
from decimal import Decimal
from uuid import uuid4

from app.database.session import AsyncSessionLocal
from app.repositories.asset_repository import AssetRepository
from app.services.asset_service import AssetService

from app.models.enums import AssetType
from app.schemas.asset import AssetCreate
from app.schemas.stock import StockCreate, StockDetailsCreate
from app.schemas.bond import BondCreate, BondDetailsCreate
from app.schemas.etf import ETFCreate, ETFDetailsCreate
from app.schemas.currency_asset import CurrencyAssetCreate, CurrencyDetailsCreate


async def main():
    suffix = uuid4().hex[:6].upper()

    async with AsyncSessionLocal() as session:
        repo = AssetRepository(session)
        service = AssetService(repo)

        stock = await service.create_stock(
            StockCreate(
                asset=AssetCreate(
                    ticker=f"AAPL_{suffix}",
                    name="Apple Inc.",
                    asset_type=AssetType.STOCK,
                    isin=None,
                    description="Apple stock test"
                ),
                stock=StockDetailsCreate(
                    sector="Technology",
                    shares_outstanding=15500000000,
                    dividend_policy="Quarterly dividends"
                )
            )
        )
        print("Stock created:", stock.id, stock.ticker)

        bond = await service.create_bond(
            BondCreate(
                asset=AssetCreate(
                    ticker=f"BOND_{suffix}",
                    name="Test Bond",
                    asset_type=AssetType.BOND,
                    isin=None,
                    description="Bond test"
                ),
                bond=BondDetailsCreate(
                    nominal_value=Decimal("1000.00"),
                    coupon_rate=Decimal("4.25"),
                    coupon_frequency=2,
                    maturity_date=date(2034, 5, 15)
                )
            )
        )
        print("Bond created:", bond.id, bond.ticker)

        etf = await service.create_etf(
            ETFCreate(
                asset=AssetCreate(
                    ticker=f"ETF_{suffix}",
                    name="Test ETF",
                    asset_type=AssetType.ETF,
                    isin=None,
                    description="ETF test"
                ),
                etf=ETFDetailsCreate(
                    provider="Vanguard",
                    expense_ratio=Decimal("0.03"),
                    benchmark_index="S&P 500",
                    trading_currency="USD"
                )
            )
        )
        print("ETF created:", etf.id, etf.ticker)

        currency = await service.create_currency(
            CurrencyAssetCreate(
                asset=AssetCreate(
                    ticker=f"CUR_{suffix}",
                    name="Test Currency",
                    asset_type=AssetType.CURRENCY,
                    isin=None,
                    description="Currency test"
                ),
                currency=CurrencyDetailsCreate(
                    iso4217=suffix[:3],
                    country="Test Country",
                    symbol="$"
                )
            )
        )
        print("Currency created:", currency.id, currency.ticker)

        found = await service.get_by_ticker(stock.ticker)
        print("Found by ticker:", found.id, found.ticker)

        assets = await service.list_all()
        print("Assets count:", len(assets))


if __name__ == "__main__":
    asyncio.run(main())