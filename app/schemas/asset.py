import re
from pydantic import BaseModel, computed_field, field_validator
from app.models.enums import AssetType

class AssetCreate(BaseModel):
    ticker: str
    name: str
    asset_type: AssetType
    isin: str | None = None
    description: str | None = None

    @field_validator("ticker")
    def ticker_valid(cls, v):
        v = v.strip().upper()
        if not v or len(v) > 20:
            raise ValueError("Ticker must be 1-20 characters")
        return v

    @field_validator("isin")
    def isin_valid(cls, v):
        if v is None:
            return v
        v = v.strip().upper()
        if not re.match(r'^[A-Z]{2}[A-Z0-9]{9}[0-9]$', v):
            raise ValueError(f"Invalid ISIN format: {v}")
        return v

class AssetResponse(BaseModel):
    id: int
    ticker: str
    name: str
    asset_type: AssetType
    isin: str | None
    description: str | None = None

    @computed_field
    def is_stock(self) -> bool:
        return self.asset_type == AssetType.STOCK

    @computed_field
    def is_bond(self) -> bool:
        return self.asset_type == AssetType.BOND

    @computed_field
    def is_etf(self) -> bool:
        return self.asset_type == AssetType.ETF

    @computed_field
    def is_currency(self) -> bool:
        return self.asset_type == AssetType.CURRENCY

    model_config = {"from_attributes": True}