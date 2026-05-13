from decimal import Decimal
from datetime import date

from app.models.enums import TransactionType, AssetType
from app.repositories.portfolio_repository import PortfolioRepository
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.asset_repository import AssetRepository
from app.repositories.dividend_payment_repository import DividendPaymentRepository
from app.repositories.coupon_payment_repository import CouponPaymentRepository


class AnalyticsService:
    def __init__(
        self,
        portfolio_repo: PortfolioRepository,
        transaction_repo: TransactionRepository,
        asset_repo: AssetRepository,
        dividend_repo: DividendPaymentRepository,
        coupon_repo: CouponPaymentRepository,
    ):
        self.portfolio_repo = portfolio_repo
        self.transaction_repo = transaction_repo
        self.asset_repo = asset_repo
        self.dividend_repo = dividend_repo
        self.coupon_repo = coupon_repo

    async def get_portfolio_positions(self, portfolio_id: int) -> list[dict]:
        portfolio = await self.portfolio_repo.get_by_id(portfolio_id)
        if portfolio is None:
            raise ValueError("Portfolio not found")

        transactions = await self.transaction_repo.get_by_portfolio_id(portfolio_id)

        positions: dict[int, Decimal] = {}
        last_prices: dict[int, Decimal] = {}

        for tx in transactions:
            positions.setdefault(tx.asset_id, Decimal("0"))

            if tx.transaction_type == TransactionType.BUY:
                positions[tx.asset_id] += tx.quantity
            elif tx.transaction_type == TransactionType.SELL:
                positions[tx.asset_id] -= tx.quantity

            last_prices[tx.asset_id] = tx.price

        result = []

        for asset_id, quantity in positions.items():
            if quantity <= 0:
                continue

            asset = await self.asset_repo.get_by_id(asset_id)
            if asset is None:
                continue

            last_price = last_prices.get(asset_id, Decimal("0"))
            market_value = quantity * last_price

            result.append(
                {
                    "asset_id": asset.id,
                    "ticker": asset.ticker,
                    "name": asset.name,
                    "asset_type": asset.asset_type.value,
                    "quantity": quantity,
                    "last_price": last_price,
                    "market_value": market_value,
                }
            )
        return result

    async def get_portfolio_assets(self, portfolio_id: int) -> list[dict]:
        positions = await self.get_portfolio_positions(portfolio_id)

        return [
            {
                "asset_id": item["asset_id"],
                "ticker": item["ticker"],
                "name": item["name"],
                "asset_type": item["asset_type"],
            }
            for item in positions
        ]

    async def get_allocation_by_asset_type(self, portfolio_id: int) -> dict:
        positions = await self.get_portfolio_positions(portfolio_id)

        allocation: dict[str, Decimal] = {
            AssetType.STOCK.value: Decimal("0"),
            AssetType.BOND.value: Decimal("0"),
            AssetType.ETF.value: Decimal("0"),
            AssetType.CURRENCY.value: Decimal("0"),
        }

        for item in positions:
            allocation[item["asset_type"]] += item["market_value"]

        return allocation

    async def get_allocation_by_sector(self, portfolio_id: int) -> dict:
        positions = await self.get_portfolio_positions(portfolio_id)

        allocation: dict[str, Decimal] = {}

        for item in positions:
            if item["asset_type"] != AssetType.STOCK.value:
                continue

            stock_details = await self.asset_repo.get_stock_details(item["asset_id"])

            sector = "Unknown"
            if stock_details and stock_details.sector:
                sector = stock_details.sector

            allocation.setdefault(sector, Decimal("0"))
            allocation[sector] += item["market_value"]

        return allocation

    async def get_transaction_history(self, portfolio_id: int):
        portfolio = await self.portfolio_repo.get_by_id(portfolio_id)
        if portfolio is None:
            raise ValueError("Portfolio not found")

        return await self.transaction_repo.get_by_portfolio_id(portfolio_id)

    async def get_received_dividends_total(self, portfolio_id: int) -> Decimal:
        positions = await self.get_portfolio_positions(portfolio_id)

        total = Decimal("0")

        for item in positions:
            if item["asset_type"] != AssetType.STOCK.value:
                continue

            dividends = await self.dividend_repo.get_by_stock_id(item["asset_id"])

            for dividend in dividends:
                if dividend.payment_date <= date.today():
                    total += item["quantity"] * dividend.dividend_per_share

        return total

    async def get_upcoming_payments(self, portfolio_id: int):
        portfolio = await self.portfolio_repo.get_by_id(portfolio_id)

        if portfolio is None:
            raise ValueError("Portfolio not found")

        positions = await self.get_portfolio_positions(portfolio_id)

        upcoming_payments = []

        for position in positions:
            asset_id = position["asset_id"]
            ticker = position["ticker"]
            quantity = position["quantity"]
            asset_type = position["asset_type"]

            if asset_type == "stock":
                dividends = await self.dividend_repo.get_by_stock_id(asset_id)

                for dividend in dividends:
                    if dividend.payment_date >= date.today():
                        estimated_amount = quantity * dividend.dividend_per_share

                        upcoming_payments.append({
                            "type": "Дивиденд",
                            "ticker": ticker,
                            "payment_date": dividend.payment_date,
                            "amount": estimated_amount,
                        })

            if asset_type == "bond":
                coupons = await self.coupon_repo.get_by_bond_id(asset_id)

                for coupon in coupons:
                    if coupon.payment_date >= date.today():
                        estimated_amount = quantity * coupon.coupon_amount

                        upcoming_payments.append({
                            "type": "Купон",
                            "ticker": ticker,
                            "payment_date": coupon.payment_date,
                            "amount": estimated_amount,
                        })

        upcoming_payments.sort(key=lambda item: item["payment_date"])

        return upcoming_payments

    async def get_simple_realized_profit(self, portfolio_id: int) -> Decimal:
        transactions = await self.transaction_repo.get_by_portfolio_id(portfolio_id)

        buy_total = Decimal("0")
        sell_total = Decimal("0")
        commissions = Decimal("0")

        for tx in transactions:
            amount = tx.quantity * tx.price
            commissions += tx.commission

            if tx.transaction_type == TransactionType.BUY:
                buy_total += amount
            elif tx.transaction_type == TransactionType.SELL:
                sell_total += amount

        return sell_total - buy_total - commissions

    async def get_portfolio_summary(self, portfolio_id: int) -> dict:
        positions = await self.get_portfolio_positions(portfolio_id)
        transactions = await self.get_transaction_history(portfolio_id)
        allocation_by_type = await self.get_allocation_by_asset_type(portfolio_id)
        allocation_by_sector = await self.get_allocation_by_sector(portfolio_id)
        received_dividends = await self.get_received_dividends_total(portfolio_id)
        upcoming_payments = await self.get_upcoming_payments(portfolio_id)
        realized_profit = await self.get_simple_realized_profit(portfolio_id)

        cash_flow = await self.get_cash_flow(portfolio_id)
        realized_pnl = await self.get_realized_pnl(portfolio_id)

        return {
            "portfolio_id": portfolio_id,
            "positions_count": len(positions),
            "transactions_count": len(transactions),
            "positions": positions,
            "allocation_by_asset_type": allocation_by_type,
            "allocation_by_sector": allocation_by_sector,
            "received_dividends_total": received_dividends,
            "upcoming_payments": upcoming_payments,
            #"simple_realized_profit": realized_profit,
            "cash_flow": cash_flow,
            "realized_pnl": realized_pnl,
        }
    
    async def get_cash_flow(self, portfolio_id: int) -> Decimal:
        transactions = await self.transaction_repo.get_by_portfolio_id(portfolio_id)

        cash_flow = Decimal("0")

        for tx in transactions:
            amount = tx.quantity * tx.price

            if tx.transaction_type == TransactionType.BUY:
                cash_flow -= amount + tx.commission
            elif tx.transaction_type == TransactionType.SELL:
                cash_flow += amount - tx.commission

        return cash_flow

    async def get_realized_pnl(self, portfolio_id: int) -> Decimal:
        transactions = await self.transaction_repo.get_by_portfolio_id(portfolio_id)

        positions: dict[int, Decimal] = {}
        total_cost: dict[int, Decimal] = {}
        realized_pnl = Decimal("0")

        sorted_transactions = sorted(
            transactions,
            key=lambda tx: tx.transaction_date,
        )

        for tx in sorted_transactions:
            asset_id = tx.asset_id
            amount = tx.quantity * tx.price

            positions.setdefault(asset_id, Decimal("0"))
            total_cost.setdefault(asset_id, Decimal("0"))

            if tx.transaction_type == TransactionType.BUY:
                positions[asset_id] += tx.quantity
                total_cost[asset_id] += amount + tx.commission

            elif tx.transaction_type == TransactionType.SELL:
                if positions[asset_id] <= 0:
                    continue

                average_price = total_cost[asset_id] / positions[asset_id]
                cost_basis = average_price * tx.quantity

                sell_value = amount - tx.commission
                realized_pnl += sell_value - cost_basis

                positions[asset_id] -= tx.quantity
                total_cost[asset_id] -= cost_basis

        return realized_pnl