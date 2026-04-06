from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database.session import Base

class Stock(Base):
    __tablename__ = "stocks"

    id: Mapped[int] = mapped_column(ForeignKey("assets.id"), primary_key=True)
    sector: Mapped[str | None] = mapped_column(String(100), nullable=True)
    shares_outstanding: Mapped[int | None] = mapped_column(Integer, nullable=True)
    dividend_policy: Mapped[str | None] = mapped_column(String(255), nullable=True)