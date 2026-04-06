from datetime import date
from decimal import Decimal
from sqlalchemy import Date, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database.session import Base

class DividendPayment(Base):
    __tablename__ = "dividend_payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    stock_id: Mapped[int] = mapped_column(ForeignKey("assets.id"), nullable=False)
    record_date: Mapped[date] = mapped_column(Date, nullable=False)
    payment_date: Mapped[date] = mapped_column(Date, nullable=False)
    dividend_per_share: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)