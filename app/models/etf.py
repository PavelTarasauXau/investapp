from decimal import Decimal
from sqlalchemy import String, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database.session import Base

class ETF(Base):
    __tablename__ = "etfs"

    id: Mapped[int] = mapped_column(ForeignKey("assets.id"), primary_key=True)
    provider: Mapped[str] = mapped_column(String(100), nullable=False)
    expense_ratio: Mapped[Decimal | None] = mapped_column(Numeric(6, 4), nullable=True)
    benchmark_index: Mapped[str | None] = mapped_column(String(100), nullable=True)
    trading_currency: Mapped[str | None] = mapped_column(String(10), nullable=True)