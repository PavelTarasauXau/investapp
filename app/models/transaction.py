from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import DateTime, Numeric, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base
from app.models.enums import TransactionType

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.portfolio import Portfolio
    from app.models.asset import Asset


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    portfolio_id: Mapped[int] = mapped_column(
        ForeignKey("portfolios.id", ondelete="CASCADE"),
        nullable=False
    )
    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id", ondelete="RESTRICT"),
        nullable=False
    )

    transaction_type: Mapped[TransactionType] = mapped_column(
        SAEnum(
            TransactionType,
            values_callable=lambda enum: [e.value for e in enum],
            native_enum=False
        ),
        nullable=False
    )

    transaction_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    quantity: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    commission: Mapped[Decimal] = mapped_column(
        Numeric(18, 4),
        default=Decimal("0"),
        nullable=False
    )

    portfolio: Mapped["Portfolio"] = relationship(back_populates="transactions")

    asset: Mapped["Asset"] = relationship(back_populates="transactions")