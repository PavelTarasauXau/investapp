from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database.session import Base

class CurrencyAsset(Base):
    __tablename__ = "currency_assets"

    id: Mapped[int] = mapped_column(ForeignKey("assets.id"), primary_key=True)
    iso4217: Mapped[str] = mapped_column(String(3), unique=True, nullable=False)
    country: Mapped[str | None] = mapped_column(String(100), nullable=True)
    symbol: Mapped[str | None] = mapped_column(String(10), nullable=True)