from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import override
from app.models.asset import Asset
from app.models.enums import AssetType
from app.repositories.abstract_repository import AbstractRepository
from app.models.stock import Stock
from app.models.bond import Bond
from app.models.etf import ETF
from app.models.currency_asset import CurrencyAsset

class AssetRepository(AbstractRepository[Asset]):
    def __init__(self, session: AsyncSession):
        self.session = session

    @override
    async def create(self, entity: Asset) -> Asset:
        self.session.add(entity)
        await self.session.commit()        #Отправляем в бд, получаем обратно сгенерированный id. Асинхронный метод, нужно ждать пока бд подтвердит запись
        await self.session.refresh(entity) #Обновляет объект в памяти новыми данными
        return entity

    @override
    async def get_by_id(self, entity_id: int) -> Asset | None:
        return await self.session.get(Asset, entity_id)

    @override
    async def list_all(self) -> list[Asset]:
        result = await self.session.execute(select(Asset))
        return list(result.scalars().all())

    @override
    async def update(self, entity_id: int, data: dict) -> Asset | None:
        asset = await self.session.get(Asset, entity_id)
        if asset is None:
            return None
        for key, value in data.items():
            setattr(asset, key, value)
        await self.session.commit()
        await self.session.refresh(asset)
        return asset

    @override
    async def delete(self, entity_id: int) -> bool:
        asset = await self.session.get(Asset, entity_id)
        if asset is None:
            return False
        await self.session.delete(asset)
        await self.session.commit()
        return True

    async def get_by_ticker(self, ticker: str) -> Asset | None:
        result = await self.session.execute(
            select(Asset).where(Asset.ticker == ticker.upper().strip())
        )
        return result.scalar_one_or_none()

    async def list_by_type(self, asset_type: AssetType) -> list[Asset]:
        result = await self.session.execute(
            select(Asset).where(Asset.asset_type == asset_type)
        )
        return list(result.scalars().all())
    
    async def create_stock(self, asset: Asset, stock: Stock) -> Asset:
        self.session.add(asset)
        await self.session.flush()

        stock.asset_id = asset.id
        self.session.add(stock)

        await self.session.commit()
        await self.session.refresh(asset)
        return asset


    async def create_bond(self, asset: Asset, bond: Bond) -> Asset:
        self.session.add(asset)
        await self.session.flush()

        bond.asset_id = asset.id
        self.session.add(bond)

        await self.session.commit()
        await self.session.refresh(asset)
        return asset


    async def create_etf(self, asset: Asset, etf: ETF) -> Asset:
        self.session.add(asset)
        await self.session.flush()

        etf.asset_id = asset.id
        self.session.add(etf)

        await self.session.commit()
        await self.session.refresh(asset)
        return asset


    async def create_currency(self, asset: Asset, currency: CurrencyAsset) -> Asset:
        self.session.add(asset)
        await self.session.flush()

        currency.asset_id = asset.id
        self.session.add(currency)

        await self.session.commit()
        await self.session.refresh(asset)
        return asset
    
    async def get_stock_details(self, asset_id: int) -> Stock | None:
        return await self.session.get(Stock, asset_id)


    async def get_bond_details(self, asset_id: int) -> Bond | None:
        return await self.session.get(Bond, asset_id)


    async def get_etf_details(self, asset_id: int) -> ETF | None:
        return await self.session.get(ETF, asset_id)


    async def get_currency_details(self, asset_id: int) -> CurrencyAsset | None:
        return await self.session.get(CurrencyAsset, asset_id)