from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session

from app.repositories.transaction_repository import TransactionRepository
from app.repositories.portfolio_repository import PortfolioRepository
from app.repositories.asset_repository import AssetRepository

from app.services.transaction_service import TransactionService

from app.schemas.transaction import TransactionCreate, TransactionResponse


router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)


def get_transaction_service(
    session: AsyncSession = Depends(get_session),
) -> TransactionService:
    transaction_repo = TransactionRepository(session)
    portfolio_repo = PortfolioRepository(session)
    asset_repo = AssetRepository(session)

    return TransactionService(
        transaction_repo=transaction_repo,
        portfolio_repo=portfolio_repo,
        asset_repo=asset_repo,
    )


@router.post(
    "/",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_transaction(
    data: TransactionCreate,
    service: TransactionService = Depends(get_transaction_service),
):
    try:
        return await service.create_transaction(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/portfolio/{portfolio_id}",
    response_model=list[TransactionResponse],
)
async def get_portfolio_transactions(
    portfolio_id: int,
    service: TransactionService = Depends(get_transaction_service),
):
    try:
        return await service.get_portfolio_transactions(portfolio_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "/asset/{asset_id}",
    response_model=list[TransactionResponse],
)
async def get_asset_transactions(
    asset_id: int,
    service: TransactionService = Depends(get_transaction_service),
):
    try:
        return await service.get_asset_transactions(asset_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "/position",
)
async def calculate_position(
    portfolio_id: int,
    asset_id: int,
    service: TransactionService = Depends(get_transaction_service),
):
    try:
        position = await service.calculate_asset_position(
            portfolio_id=portfolio_id,
            asset_id=asset_id,
        )
        return {
            "portfolio_id": portfolio_id,
            "asset_id": asset_id,
            "position": position,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))