from decimal import Decimal

from sqlalchemy import String, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.asset import Asset


class ETF(Base):
    __tablename__ = "etfs"

    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"),
        primary_key=True
    )
    provider: Mapped[str] = mapped_column(String(255), nullable=False)
    expense_ratio: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    benchmark_index: Mapped[str | None] = mapped_column(String(255), nullable=True)
    trading_currency: Mapped[str | None] = mapped_column(String(10), nullable=True)

    asset: Mapped["Asset"] = relationship(back_populates="etf")