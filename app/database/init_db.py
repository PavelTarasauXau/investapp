from app.database.session import engine, Base

from app.models.user import User
from app.models.asset import Asset
from app.models.stock import Stock
from app.models.bond import Bond
from app.models.etf import ETF
from app.models.currency_asset import CurrencyAsset
from app.models.portfolio import Portfolio
from app.models.transaction import Transaction
from app.models.dividend_payment import DividendPayment
from app.models.coupon_payment import CouponPayment

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    import asyncio
    asyncio.run(init_db())