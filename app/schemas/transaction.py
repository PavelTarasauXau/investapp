from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, field_validator, computed_field
from app.models.transaction import TransactionType

class TransactionCreate(BaseModel):
    portfolio_id: int
    asset_id: int
    transaction_type: TransactionType
    quantity: Decimal
    price: Decimal
    commission: Decimal = Decimal("0")
    transaction_date: datetime | None = None

    @field_validator("quantity", "price")
    def must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Must be positive")
        return v

    @field_validator("commission")
    def commission_not_negative(cls, v):
        if v < 0:
            raise ValueError("Commission cannot be negative")
        return v

class TransactionResponse(BaseModel):
    id: int
    portfolio_id: int
    asset_id: int
    transaction_type: TransactionType
    quantity: Decimal
    price: Decimal
    commission: Decimal
    transaction_date: datetime

    @computed_field
    def total_amount(self) -> Decimal:
        return self.quantity * self.price

    @computed_field
    def total_with_commission(self) -> Decimal:
        return self.total_amount + self.commission

    model_config = {"from_attributes": True}