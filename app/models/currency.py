from .asset import Asset, AssetType


class CurrencyAsset(Asset):
    def __init__(
        self,
        ticker: str,
        name: str,
        iso4217: str,
        country: str | None = None,
        symbol: str | None = None,
        id: int | None = None,
    ):
        super().__init__(
            ticker=ticker,
            name=name,
            asset_type=AssetType.CURRENCY,
            id=id,
            isin=None,
        )

        if not iso4217 or not iso4217.strip():
            raise ValueError("ISO 4217 code cannot be empty")

        iso4217 = iso4217.strip().upper()
        if len(iso4217) != 3:
            raise ValueError("ISO 4217 code must contain exactly 3 characters")

        self.iso4217 = iso4217
        self.country = country.strip() if country else None
        self.symbol = symbol.strip() if symbol else None

    def __repr__(self) -> str:
        return f"<CurrencyAsset {self.iso4217} ({self.name})>"