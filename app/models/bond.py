from datetime import date
from decimal import Decimal

from .asset import Asset, AssetType


class Bond(Asset):
    def __init__(
        self,
        ticker: str,
        name: str,
        nominal_value: Decimal,
        coupon_rate: Decimal,
        coupon_frequency: int,
        maturity_date: date,
        id: int | None = None,
        isin: str | None = None,
    ):
        super().__init__(
            ticker=ticker,
            name=name,
            asset_type=AssetType.BOND,
            id=id,
            isin=isin,
        )

        nominal_value = Decimal(nominal_value)
        coupon_rate = Decimal(coupon_rate)

        if nominal_value <= 0:
            raise ValueError("Nominal value must be positive")
        if coupon_rate < 0:
            raise ValueError("Coupon rate cannot be negative")
        if coupon_frequency <= 0:
            raise ValueError("Coupon frequency must be positive")
        if not isinstance(maturity_date, date):
            raise ValueError("Maturity date must be a date object")

        self.nominal_value = nominal_value
        self.coupon_rate = coupon_rate
        self.coupon_frequency = coupon_frequency
        self.maturity_date = maturity_date

    @property
    def annual_coupon_amount(self) -> Decimal:
        return self.nominal_value * self.coupon_rate / Decimal("100")

    @property
    def coupon_payment_amount(self) -> Decimal:
        return self.annual_coupon_amount / Decimal(self.coupon_frequency)

    @property
    def is_matured(self) -> bool:
        return self.maturity_date < date.today()

    def __repr__(self) -> str:
        return f"<Bond {self.ticker} ({self.name})>"