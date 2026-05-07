from app.models.asset import Asset
from app.models.stock import Stock
from app.models.bond import Bond
from app.models.etf import ETF
from app.models.currency_asset import CurrencyAsset
from app.models.enums import AssetType

from app.repositories.asset_repository import AssetRepository

from app.schemas.stock import StockCreate
from app.schemas.bond import BondCreate
from app.schemas.etf import ETFCreate
from app.schemas.currency_asset import CurrencyAssetCreate


class AssetService:
    def __init__(self, asset_repo: AssetRepository):
        self.asset_repo = asset_repo

    async def create_stock(self, data: StockCreate) -> Asset:
        existing_asset = await self.asset_repo.get_by_ticker(data.asset.ticker)
        if existing_asset:
            raise ValueError("Asset with this ticker already exists")

        asset = Asset(
            ticker=data.asset.ticker,
            name=data.asset.name,
            isin=data.asset.isin,
            description=data.asset.description,
            asset_type=AssetType.STOCK,
        )

        stock = Stock(
            sector=data.stock.sector,
            shares_outstanding=data.stock.shares_outstanding,
            dividend_policy=data.stock.dividend_policy,
        )

        return await self.asset_repo.create_stock(asset, stock)

    async def create_bond(self, data: BondCreate) -> Asset:
        existing_asset = await self.asset_repo.get_by_ticker(data.asset.ticker)
        if existing_asset:
            raise ValueError("Asset with this ticker already exists")

        asset = Asset(
            ticker=data.asset.ticker,
            name=data.asset.name,
            isin=data.asset.isin,
            description=data.asset.description,
            asset_type=AssetType.BOND,
        )

        bond = Bond(
            nominal_value=data.bond.nominal_value,
            coupon_rate=data.bond.coupon_rate,
            coupon_frequency=data.bond.coupon_frequency,
            maturity_date=data.bond.maturity_date,
        )

        return await self.asset_repo.create_bond(asset, bond)

    async def create_etf(self, data: ETFCreate) -> Asset:
        existing_asset = await self.asset_repo.get_by_ticker(data.asset.ticker)
        if existing_asset:
            raise ValueError("Asset with this ticker already exists")

        asset = Asset(
            ticker=data.asset.ticker,
            name=data.asset.name,
            isin=data.asset.isin,
            description=data.asset.description,
            asset_type=AssetType.ETF,
        )

        etf = ETF(
            provider=data.etf.provider,
            expense_ratio=data.etf.expense_ratio,
            benchmark_index=data.etf.benchmark_index,
            trading_currency=data.etf.trading_currency,
        )

        return await self.asset_repo.create_etf(asset, etf)

    async def create_currency(self, data: CurrencyAssetCreate) -> Asset:
        existing_asset = await self.asset_repo.get_by_ticker(data.asset.ticker)
        if existing_asset:
            raise ValueError("Asset with this ticker already exists")

        asset = Asset(
            ticker=data.asset.ticker,
            name=data.asset.name,
            isin=data.asset.isin,
            description=data.asset.description,
            asset_type=AssetType.CURRENCY,
        )

        currency = CurrencyAsset(
            iso4217=data.currency.iso4217,
            country=data.currency.country,
            symbol=data.currency.symbol,
        )

        return await self.asset_repo.create_currency(asset, currency)

    async def get_by_id(self, asset_id: int) -> Asset | None:
        return await self.asset_repo.get_by_id(asset_id)

    async def get_by_ticker(self, ticker: str) -> Asset | None:
        return await self.asset_repo.get_by_ticker(ticker)

    async def list_all(self) -> list[Asset]:
        return await self.asset_repo.list_all()

    async def list_by_type(self, asset_type: AssetType) -> list[Asset]:
        return await self.asset_repo.list_by_type(asset_type)

    async def delete(self, asset_id: int) -> bool:
        return await self.asset_repo.delete(asset_id)