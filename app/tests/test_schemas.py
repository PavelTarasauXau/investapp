from datetime import date
from decimal import Decimal
from pydantic import ValidationError

from app.models.enums import AssetType, Currency, TransactionType
from app.schemas.asset import AssetCreate
from app.schemas.stock import StockCreate, StockDetailsCreate
from app.schemas.bond import BondCreate, BondDetailsCreate
from app.schemas.etf import ETFCreate, ETFDetailsCreate
from app.schemas.currency_asset import CurrencyAssetCreate, CurrencyDetailsCreate
from app.schemas.portfolio import PortfolioCreate
from app.schemas.transaction import TransactionCreate
from app.schemas.dividend_payment import DividendPaymentCreate
from app.schemas.coupon_payment import CouponPaymentCreate
from app.schemas.user import UserCreate


def test_valid_schemas():
    asset = AssetCreate(
        ticker=" aapl ",
        name="Apple Inc.",
        asset_type=AssetType.STOCK,
        isin="US0378331005",
        description="Apple stock"
    )
    print("Asset:", asset)

    stock = StockCreate(
        asset=asset,
        stock=StockDetailsCreate(
            sector="Technology",
            shares_outstanding=15500000000,
            dividend_policy="Quarterly dividends"
        )
    )
    print("Stock:", stock)

    bond = BondCreate(
        asset=AssetCreate(
            ticker="US10Y",
            name="US Treasury 10Y",
            asset_type=AssetType.BOND,
            isin=None,
            description="Test bond"
        ),
        bond=BondDetailsCreate(
            nominal_value=Decimal("1000.00"),
            coupon_rate=Decimal("4.25"),
            coupon_frequency=2,
            maturity_date=date(2034, 5, 15)
        )
    )
    print("Bond:", bond)

    etf = ETFCreate(
        asset=AssetCreate(
            ticker="VOO",
            name="Vanguard S&P 500 ETF",
            asset_type=AssetType.ETF,
            isin="US9229083632",
            description="ETF test"
        ),
        etf=ETFDetailsCreate(
            provider="Vanguard",
            expense_ratio=Decimal("0.03"),
            benchmark_index="S&P 500",
            trading_currency="usd"
        )
    )
    print("ETF:", etf)

    currency_asset = CurrencyAssetCreate(
        asset=AssetCreate(
            ticker="USD",
            name="US Dollar",
            asset_type=AssetType.CURRENCY,
            isin=None,
            description="Currency asset"
        ),
        currency=CurrencyDetailsCreate(
            iso4217="usd",
            country="United States",
            symbol="$"
        )
    )
    print("Currency asset:", currency_asset)

    portfolio = PortfolioCreate(
        name=" Main portfolio ",
        currency=Currency.USD,
        description=" Test portfolio "
    )
    print("Portfolio:", portfolio)

    transaction = TransactionCreate(
        portfolio_id=1,
        asset_id=1,
        transaction_type=TransactionType.BUY,
        quantity=Decimal("10"),
        price=Decimal("180.50"),
        commission=Decimal("1.50")
    )
    print("Transaction:", transaction)

    dividend = DividendPaymentCreate(
        stock_id=1,
        record_date=date(2026, 5, 1),
        payment_date=date(2026, 5, 15),
        dividend_per_share=Decimal("0.25")
    )
    print("Dividend:", dividend)

    coupon = CouponPaymentCreate(
        bond_id=2,
        coupon_number=1,
        payment_date=date(2026, 6, 1),
        coupon_amount=Decimal("21.25")
    )
    print("Coupon:", coupon)

    user = UserCreate(
        email="test@example.com",
        full_name=" Test User ",
        password="123456"
    )
    print("User:", user)


def test_invalid_schema():
    try:
        AssetCreate(
            ticker="",
            name="Broken Asset",
            asset_type=AssetType.STOCK,
            isin="BAD_ISIN"
        )
    except ValidationError as e:
        print("Invalid asset caught correctly:")
        print(e)


if __name__ == "__main__":
    test_valid_schemas()
    test_invalid_schema()