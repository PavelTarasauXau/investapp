from datetime import date
from decimal import Decimal
from pydantic import BaseModel, field_validator, computed_field

class DividendPaymentCreate(BaseModel):
    stock_id: int
    record_date: date
    payment_date: date
    dividend_per_share: Decimal

    @field_validator("stock_id")
    def id_positive(cls, v):
        if v <= 0:
            raise ValueError("Stock id must be positive")
        return v

    @field_validator("dividend_per_share")
    def not_negative(cls, v):
        if v < 0:
            raise ValueError("Dividend per share cannot be negative")
        return v

class DividendPaymentResponse(BaseModel):
    id: int
    stock_id: int
    record_date: date
    payment_date: date
    dividend_per_share: Decimal

    @computed_field
    def is_future_payment(self) -> bool:
        return self.payment_date > date.today()

    model_config = {"from_attributes": True}