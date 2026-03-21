from app.models.asset import Asset, AssetType
from app.repositories.abstract_repository import AbstractRepository
from typing import override


class AssetRepository(AbstractRepository[Asset]):

    @override
    def create(self, entity: Asset) -> Asset:
        raise NotImplementedError

    @override
    def get_by_id(self, entity_id: int) -> Asset | None:
        raise NotImplementedError

    @override
    def list_all(self) -> list[Asset]:
        raise NotImplementedError

    @override
    def delete(self, entity_id: int) -> bool:
        raise NotImplementedError

    def get_by_ticker(self, ticker: str) -> Asset | None:
        raise NotImplementedError

    def list_by_type(self, asset_type: AssetType) -> list[Asset]:
        raise NotImplementedError