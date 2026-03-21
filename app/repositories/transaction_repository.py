from app.models.transaction import Transaction
from app.repositories.abstract_repository import AbstractRepository
from typing import override


class TransactionRepository(AbstractRepository[Transaction]):

    @override
    def create(self, entity: Transaction) -> Transaction:
        raise NotImplementedError

    @override
    def get_by_id(self, entity_id: int) -> Transaction | None:
        raise NotImplementedError

    @override
    def list_all(self) -> list[Transaction]:
        raise NotImplementedError

    @override
    def delete(self, entity_id: int) -> bool:
        raise NotImplementedError

    def get_by_portfolio_id(self, portfolio_id: int) -> list[Transaction]:
        raise NotImplementedError

    def get_by_asset_id(self, asset_id: int) -> list[Transaction]:
        raise NotImplementedError