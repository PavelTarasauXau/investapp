from typing import override
from app.models.dividend_payment import DividendPayment
from app.repositories.abstract_repository import AbstractRepository


class DividendPaymentRepository(AbstractRepository[DividendPayment]):

    @override
    def create(self, entity: DividendPayment) -> DividendPayment:
        raise NotImplementedError

    @override
    def get_by_id(self, entity_id: int) -> DividendPayment | None:
        raise NotImplementedError

    @override
    def list_all(self) -> list[DividendPayment]:
        raise NotImplementedError

    @override
    def delete(self, entity_id: int) -> bool:
        raise NotImplementedError

    def get_by_stock_id(self, stock_id: int) -> list[DividendPayment]:
        raise NotImplementedError