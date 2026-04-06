from datetime import datetime
from pydantic import BaseModel, field_validator, computed_field
from app.models.portfolio import Currency

class PortfolioCreate(BaseModel):
    name: str
    currency: Currency
    description: str | None = None

    @field_validator("name")
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Portfolio name cannot be empty")
        return v.strip()

    @field_validator("description")
    def strip_description(cls, v):
        return v.strip() if v else None

class PortfolioResponse(BaseModel):
    id: int
    user_id: int
    name: str
    currency: Currency
    description: str | None
    is_active: bool
    created_at: datetime

    @computed_field
    def display_name(self) -> str:
        return f"{self.name} ({self.currency.value})"

    model_config = {"from_attributes": True}