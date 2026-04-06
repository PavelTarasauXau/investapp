from pydantic import BaseModel, field_validator, computed_field
from app.schemas.asset import AssetResponse

class StockCreate(BaseModel):
    ticker: str
    name: str
    isin: str | None = None
    sector: str | None = None
    shares_outstanding: int | None = None
    dividend_policy: str | None = None

    @field_validator("shares_outstanding")
    def shares_not_negative(cls, v):
        if v is not None and v < 0:
            raise ValueError("Shares outstanding cannot be negative")
        return v

    @field_validator("sector", "dividend_policy")
    def strip_strings(cls, v):
        return v.strip() if v else None

class StockResponse(AssetResponse):
    sector: str | None
    shares_outstanding: int | None
    dividend_policy: str | None

    @computed_field
    def has_dividends(self) -> bool:
        return bool(
            self.dividend_policy and
            self.dividend_policy.lower() != "none"
        )