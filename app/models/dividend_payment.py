from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.stock import Stock


class DividendPayment(Base):
    __tablename__ = "dividend_payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    stock_id: Mapped[int] = mapped_column(
        ForeignKey("stocks.asset_id", ondelete="CASCADE"),
        nullable=False
    )
    record_date: Mapped[date] = mapped_column(Date, nullable=False)
    payment_date: Mapped[date] = mapped_column(Date, nullable=False)
    dividend_per_share: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)

    stock: Mapped["Stock"] = relationship(back_populates="dividend_payments")