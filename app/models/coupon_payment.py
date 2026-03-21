from datetime import date
from decimal import Decimal


class CouponPayment:
    def __init__(
        self,
        bond_id: int,
        coupon_number: int,
        payment_date: date,
        coupon_amount: Decimal,
        id: int | None = None,
    ):
        if bond_id <= 0:
            raise ValueError("Bond id must be a positive integer")
        if coupon_number <= 0:
            raise ValueError("Coupon number must be a positive integer")
        if not isinstance(payment_date, date):
            raise ValueError("Payment date must be a date object")

        coupon_amount = Decimal(coupon_amount)
        if coupon_amount < 0:
            raise ValueError("Coupon amount cannot be negative")

        self.id = id
        self.bond_id = bond_id
        self.coupon_number = coupon_number
        self.payment_date = payment_date
        self.coupon_amount = coupon_amount

    @property
    def is_future_payment(self) -> bool:
        return self.payment_date > date.today()

    def total_for_bonds(self, bonds_count: Decimal | int) -> Decimal:
        bonds_count = Decimal(bonds_count)
        if bonds_count < 0:
            raise ValueError("Bonds count cannot be negative")
        return self.coupon_amount * bonds_count

    def __repr__(self) -> str:
        return (
            f"<CouponPayment bond_id={self.bond_id}, "
            f"coupon_number={self.coupon_number}, "
            f"payment_date={self.payment_date}, "
            f"coupon_amount={self.coupon_amount}>"
        )