from __future__ import annotations
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.asset import Asset


class CurrencyAsset(Base):
    __tablename__ = "currencies"

    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id", ondelete="CASCADE"),
        primary_key=True
    )
    iso4217: Mapped[str] = mapped_column(String(3), unique=True, nullable=False)
    country: Mapped[str | None] = mapped_column(String(100), nullable=True)
    symbol: Mapped[str | None] = mapped_column(String(10), nullable=True)

    asset: Mapped["Asset"] = relationship(back_populates="currency_asset")

    #вот с валютами надо разобраться, потому что сейчас две таблицы в бд, одна из которых просто висит без связей