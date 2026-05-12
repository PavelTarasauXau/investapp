from __future__ import annotations

from sqlalchemy import String, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base
from app.models.enums import AssetType

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.transaction import Transaction
    from app.models.stock import Stock
    from app.models.bond import Bond
    from app.models.etf import ETF
    from app.models.currency_asset import CurrencyAsset


class Asset(Base):#не обычный python класс, а таблица базы данных
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(primary_key=True)
    ticker: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    isin: Mapped[str | None] = mapped_column(String(12), unique=True, nullable=True)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)

    asset_type: Mapped[AssetType] = mapped_column(
        SAEnum(
            AssetType,
            values_callable=lambda enum: [e.value for e in enum],
            native_enum=False
        ),
        nullable=False
    )

    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction",
        back_populates="asset"
    )

    stock: Mapped["Stock | None"] = relationship(
        "Stock",
        back_populates="asset",
        uselist=False,
        cascade="all, delete-orphan"
    )

    bond: Mapped["Bond | None"] = relationship(
        "Bond",
        back_populates="asset",
        uselist=False,
        cascade="all, delete-orphan"
    )

    etf: Mapped["ETF | None"] = relationship(
        "ETF",
        back_populates="asset",
        uselist=False,
        cascade="all, delete-orphan"
    )

    currency_asset: Mapped["CurrencyAsset | None"] = relationship(
        "CurrencyAsset",
        back_populates="asset",
        uselist=False,
        cascade="all, delete-orphan"
    )