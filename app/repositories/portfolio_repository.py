from app.models.portfolio import Portfolio
from app.repositories.abstract_repository import AbstractRepository
from typing import override

class PortfolioRepository(AbstractRepository[Portfolio]):

    @override
    def create(self, entity: Portfolio) -> Portfolio:
        raise NotImplementedError

    @override
    def get_by_id(self, entity_id: int) -> Portfolio | None:
        raise NotImplementedError

    @override
    def list_all(self) -> list[Portfolio]:
        raise NotImplementedError

    @override
    def delete(self, entity_id: int) -> bool:
        raise NotImplementedError

    def get_by_user_id(self, user_id: int) -> list[Portfolio]:
        raise NotImplementedError

    def update(self, entity: Portfolio) -> Portfolio:
        raise NotImplementedError