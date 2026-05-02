from sqlalchemy import String, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.asset import Asset
    from app.models.dividend_payment import DividendPayment


class Stock(Base):
    __tablename__ = "stocks"

    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"),
        primary_key=True
    )
    sector: Mapped[str | None] = mapped_column(String(100), nullable=True)
    shares_outstanding: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    dividend_policy: Mapped[str | None] = mapped_column(String(255), nullable=True)

    asset: Mapped["Asset"] = relationship(back_populates="stock")

    dividend_payments: Mapped[list["DividendPayment"]] = relationship(
        back_populates="stock",
        cascade="all, delete-orphan"
    )