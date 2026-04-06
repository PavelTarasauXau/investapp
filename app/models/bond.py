from datetime import date
from decimal import Decimal
from sqlalchemy import Date, Integer, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database.session import Base

class Bond(Base):
    __tablename__ = "bonds"

    id: Mapped[int] = mapped_column(ForeignKey("assets.id"), primary_key=True)
    nominal_value: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)
    coupon_rate: Mapped[Decimal] = mapped_column(Numeric(8, 4), nullable=False)
    coupon_frequency: Mapped[int] = mapped_column(Integer, nullable=False)
    maturity_date: Mapped[date] = mapped_column(Date, nullable=False)