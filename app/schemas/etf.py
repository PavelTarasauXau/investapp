from decimal import Decimal
from pydantic import BaseModel, field_validator, computed_field
from app.schemas.asset import AssetResponse
from app.schemas.asset import AssetCreate, AssetResponse

class ETFDetailsCreate(BaseModel):
    provider: str
    expense_ratio: Decimal | None = None
    benchmark_index: str | None = None
    trading_currency: str | None = None

    @field_validator("provider")
    def provider_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Provider cannot be empty")
        return v.strip()

    @field_validator("expense_ratio")
    def ratio_not_negative(cls, v):
        if v is not None and v < 0:
            raise ValueError("Expense ratio cannot be negative")
        return v

    @field_validator("trading_currency")
    def currency_upper(cls, v):
        return v.strip().upper() if v else None


class ETFCreate(BaseModel):
    asset: AssetCreate
    etf: ETFDetailsCreate

class ETFResponse(AssetResponse):
    provider: str
    expense_ratio: Decimal | None
    benchmark_index: str | None
    trading_currency: str | None

    @computed_field
    def has_expense_ratio(self) -> bool:
        return self.expense_ratio is not None