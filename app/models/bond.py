from __future__ import annotations
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Integer, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.asset import Asset
    from app.models.coupon_payment import CouponPayment


class Bond(Base):
    __tablename__ = "bonds"

    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"),
        primary_key=True
    )
    nominal_value: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    coupon_rate: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    coupon_frequency: Mapped[int] = mapped_column(Integer, nullable=False)
    maturity_date: Mapped[date] = mapped_column(Date, nullable=False)

    asset: Mapped["Asset"] = relationship(
        "Asset",
        back_populates="bond"
    )

    coupon_payments: Mapped[list["CouponPayment"]] = relationship(
        "CouponPayment",
        back_populates="bond",
        cascade="all, delete-orphan"
    )