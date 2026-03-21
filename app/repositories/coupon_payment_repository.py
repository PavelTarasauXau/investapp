from typing import override
from app.models.coupon_payment import CouponPayment
from app.repositories.abstract_repository import AbstractRepository


class CouponPaymentRepository(AbstractRepository[CouponPayment]):

    @override
    def create(self, entity: CouponPayment) -> CouponPayment:
        raise NotImplementedError

    @override
    def get_by_id(self, entity_id: int) -> CouponPayment | None:
        raise NotImplementedError

    @override
    def list_all(self) -> list[CouponPayment]:
        raise NotImplementedError

    @override
    def delete(self, entity_id: int) -> bool:
        raise NotImplementedError

    def get_by_bond_id(self, bond_id: int) -> list[CouponPayment]:
        raise NotImplementedError