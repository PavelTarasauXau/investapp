from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import override
from app.models.asset import Asset
from app.models.enums import AssetType
from app.repositories.abstract_repository import AbstractRepository

class AssetRepository(AbstractRepository[Asset]):
    def __init__(self, session: AsyncSession):
        self.session = session

    @override
    async def create(self, entity: Asset) -> Asset:
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
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