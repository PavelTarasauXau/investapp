from pydantic import BaseModel, field_validator
from app.schemas.asset import AssetResponse

class CurrencyAssetCreate(BaseModel):
    ticker: str
    name: str
    iso4217: str
    country: str | None = None
    symbol: str | None = None

    @field_validator("iso4217")
    def iso_valid(cls, v):
        v = v.strip().upper()
        if len(v) != 3:
            raise ValueError("ISO 4217 must be exactly 3 characters")
        return v

    @field_validator("country", "symbol")
    def strip_strings(cls, v):
        return v.strip() if v else None

class CurrencyAssetResponse(AssetResponse):
    iso4217: str
    country: str | None
    symbol: str | None