from datetime import date
from decimal import Decimal
from pydantic import BaseModel, field_validator, computed_field

class CouponPaymentCreate(BaseModel):
    bond_id: int
    coupon_number: int
    payment_date: date
    coupon_amount: Decimal

    @field_validator("bond_id", "coupon_number")
    def must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Must be positive")
        return v

    @field_validator("coupon_amount")
    def not_negative(cls, v):
        if v < 0:
            raise ValueError("Coupon amount cannot be negative")
        return v

class CouponPaymentResponse(BaseModel):
    id: int
    bond_id: int
    coupon_number: int
    payment_date: date
    coupon_amount: Decimal

    @computed_field
    def is_future_payment(self) -> bool:
        return self.payment_date > date.today()

    model_config = {"from_attributes": True}