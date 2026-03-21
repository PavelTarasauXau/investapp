from .asset import Asset, AssetType

class Stock(Asset): 

    def __init__(
            self,
            ticker: str,
            name: str,
            sector: str | None = None,
            shares_outstanding: int | None = None,
            dividend_policy: str | None = None,
            id: int | None = None,
            isin: str | None = None,
    ):
        super().__init__(
            ticker = ticker,
            name = name,
            asset_type=AssetType.STOCK,
            id = id,
            isin = isin,
        ) 

        if shares_outstanding is not None and shares_outstanding < 0:
            raise ValueError("Shares outstanding cannot be negative")
        
        self.sector = sector.strip() if sector else None
        self.shares_outstanding = shares_outstanding
        self.dividend_policy = dividend_policy.strip() if dividend_policy else None

    @property
    def has_dividends(self) -> bool:
        return bool(self.dividend_policy and self.dividend_policy.lower() != "none")

    def __repr__(self) -> str:
        return f"<Stock {self.ticker} ({self.name})>"