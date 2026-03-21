from decimal import Decimal

from .asset import Asset, AssetType


class ETF(Asset):
    def __init__(
        self,
        ticker: str,
        name: str,
        provider: str,
        expense_ratio: Decimal | None = None,
        benchmark_index: str | None = None,
        trading_currency: str | None = None,
        id: int | None = None,
        isin: str | None = None,
    ):
        super().__init__(
            ticker=ticker,
            name=name,
            asset_type=AssetType.ETF,
            id=id,
            isin=isin,
        )

        if not provider or not provider.strip():
            raise ValueError("Provider cannot be empty")

        if expense_ratio is not None:
            expense_ratio = Decimal(expense_ratio)
            if expense_ratio < 0:
                raise ValueError("Expense ratio cannot be negative")

        self.provider = provider.strip()
        self.expense_ratio = expense_ratio
        self.benchmark_index = benchmark_index.strip() if benchmark_index else None
        self.trading_currency = trading_currency.strip().upper() if trading_currency else None

    @property
    def has_expense_ratio(self) -> bool:
        return self.expense_ratio is not None

    def __repr__(self) -> str:
        return f"<ETF {self.ticker} ({self.name})>"