from datetime import date
from decimal import Decimal
from pydantic import BaseModel, field_validator, computed_field
from app.schemas.asset import AssetResponse

class BondCreate(BaseModel):
    ticker: str
    name: str
    isin: str | None = None
    nominal_value: Decimal
    coupon_rate: Decimal
    coupon_frequency: int
    maturity_date: date

    @field_validator("nominal_value", "coupon_rate")
    def must_be_positive(cls, v):
        if v < 0:
            raise ValueError("Must be non-negative")
        return v

    @field_validator("coupon_frequency")
    def frequency_positive(cls, v):
        if v <= 0:
            raise ValueError("Coupon frequency must be positive")
        return v

class BondResponse(AssetResponse):
    nominal_value: Decimal
    coupon_rate: Decimal
    coupon_frequency: int
    maturity_date: date

    @computed_field
    def annual_coupon_amount(self) -> Decimal:
        return self.nominal_value * self.coupon_rate / Decimal("100")

    @computed_field
    def coupon_payment_amount(self) -> Decimal:
        return self.annual_coupon_amount / Decimal(self.coupon_frequency)

    @computed_field
    def is_matured(self) -> bool:
        return self.maturity_date < date.today()