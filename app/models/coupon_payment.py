from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Numeric, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.bond import Bond


class CouponPayment(Base):
    __tablename__ = "coupon_payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    bond_id: Mapped[int] = mapped_column(
        ForeignKey("bonds.asset_id", ondelete="CASCADE"),
        nullable=False
    )
    coupon_number: Mapped[int] = mapped_column(Integer, nullable=False)
    payment_date: Mapped[date] = mapped_column(Date, nullable=False)
    coupon_amount: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)

    bond: Mapped["Bond"] = relationship(back_populates="coupon_payments")