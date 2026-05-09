from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session

from app.repositories.portfolio_repository import PortfolioRepository
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.asset_repository import AssetRepository
from app.repositories.dividend_payment_repository import DividendPaymentRepository
from app.repositories.coupon_payment_repository import CouponPaymentRepository

from app.services.analytics_service import AnalyticsService
from app.schemas.transaction import TransactionResponse


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


def get_analytics_service(
    session: AsyncSession = Depends(get_session),
) -> AnalyticsService:
    portfolio_repo = PortfolioRepository(session)
    transaction_repo = TransactionRepository(session)
    asset_repo = AssetRepository(session)
    dividend_repo = DividendPaymentRepository(session)
    coupon_repo = CouponPaymentRepository(session)

    return AnalyticsService(
        portfolio_repo=portfolio_repo,
        transaction_repo=transaction_repo,
        asset_repo=asset_repo,
        dividend_repo=dividend_repo,
        coupon_repo=coupon_repo,
    )


@router.get("/portfolio/{portfolio_id}/positions")
async def get_positions(
    portfolio_id: int,
    service: AnalyticsService = Depends(get_analytics_service),
):
    try:
        return await service.get_portfolio_positions(portfolio_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/portfolio/{portfolio_id}/assets")
async def get_portfolio_assets(
    portfolio_id: int,
    service: AnalyticsService = Depends(get_analytics_service),
):
    try:
        return await service.get_portfolio_assets(portfolio_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/portfolio/{portfolio_id}/allocation/type")
async def get_allocation_by_type(
    portfolio_id: int,
    service: AnalyticsService = Depends(get_analytics_service),
):
    try:
        return await service.get_allocation_by_asset_type(portfolio_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/portfolio/{portfolio_id}/allocation/sector")
async def get_allocation_by_sector(
    portfolio_id: int,
    service: AnalyticsService = Depends(get_analytics_service),
):
    try:
        return await service.get_allocation_by_sector(portfolio_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "/portfolio/{portfolio_id}/transactions",
    response_model=list[TransactionResponse],
)
async def get_transaction_history(
    portfolio_id: int,
    service: AnalyticsService = Depends(get_analytics_service),
):
    try:
        return await service.get_transaction_history(portfolio_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/portfolio/{portfolio_id}/dividends/received-total")
async def get_received_dividends_total(
    portfolio_id: int,
    service: AnalyticsService = Depends(get_analytics_service),
):
    try:
        total = await service.get_received_dividends_total(portfolio_id)
        return {
            "portfolio_id": portfolio_id,
            "received_dividends_total": total,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/portfolio/{portfolio_id}/upcoming-payments")
async def get_upcoming_payments(
    portfolio_id: int,
    service: AnalyticsService = Depends(get_analytics_service),
):
    try:
        return await service.get_upcoming_payments(portfolio_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/portfolio/{portfolio_id}/profit/simple")
async def get_simple_realized_profit(
    portfolio_id: int,
    service: AnalyticsService = Depends(get_analytics_service),
):
    try:
        profit = await service.get_simple_realized_profit(portfolio_id)
        return {
            "portfolio_id": portfolio_id,
            "simple_realized_profit": profit,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/portfolio/{portfolio_id}/summary")
async def get_portfolio_summary(
    portfolio_id: int,
    service: AnalyticsService = Depends(get_analytics_service),
):
    try:
        return await service.get_portfolio_summary(portfolio_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))