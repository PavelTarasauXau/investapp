from datetime import date
from decimal import Decimal
from sqlalchemy import Date, Numeric, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database.session import Base

class CouponPayment(Base):
    __tablename__ = "coupon_payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    bond_id: Mapped[int] = mapped_column(ForeignKey("assets.id"), nullable=False)
    coupon_number: Mapped[int] = mapped_column(Integer, nullable=False)
    payment_date: Mapped[date] = mapped_column(Date, nullable=False)
    coupon_amount: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)