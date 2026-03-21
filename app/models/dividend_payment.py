from datetime import date
from decimal import Decimal


class DividendPayment:
    def __init__(
        self,
        stock_id: int,
        record_date: date,
        payment_date: date,
        dividend_per_share: Decimal,
        id: int | None = None,
    ):
        if stock_id <= 0:
            raise ValueError("Stock id must be a positive integer")
        if not isinstance(record_date, date):
            raise ValueError("Record date must be a date object")
        if not isinstance(payment_date, date):
            raise ValueError("Payment date must be a date object")

        dividend_per_share = Decimal(dividend_per_share)
        if dividend_per_share < 0:
            raise ValueError("Dividend per share cannot be negative")

        self.id = id
        self.stock_id = stock_id
        self.record_date = record_date
        self.payment_date = payment_date
        self.dividend_per_share = dividend_per_share

    @property
    def is_future_payment(self) -> bool:
        return self.payment_date > date.today()

    def total_for_shares(self, shares_count: Decimal | int) -> Decimal:
        shares_count = Decimal(shares_count)
        if shares_count < 0:
            raise ValueError("Shares count cannot be negative")
        return self.dividend_per_share * shares_count

    def __repr__(self) -> str:
        return (
            f"<DividendPayment stock_id={self.stock_id}, "
            f"payment_date={self.payment_date}, "
            f"dividend_per_share={self.dividend_per_share}>"
        )