from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session

from app.repositories.asset_repository import AssetRepository
from app.services.asset_service import AssetService

from app.models.enums import AssetType

from app.schemas.asset import AssetResponse
from app.schemas.stock import StockCreate
from app.schemas.bond import BondCreate
from app.schemas.etf import ETFCreate
from app.schemas.currency_asset import CurrencyAssetCreate


router = APIRouter(
    prefix="/assets",
    tags=["Assets"],
)


def get_asset_service(
    session: AsyncSession = Depends(get_session),
) -> AssetService:
    asset_repo = AssetRepository(session)
    return AssetService(asset_repo)


@router.get("/", response_model=list[AssetResponse])
async def list_assets(
    service: AssetService = Depends(get_asset_service),
):
    return await service.list_all()


@router.get("/{asset_id}", response_model=AssetResponse)
async def get_asset(
    asset_id: int,
    service: AssetService = Depends(get_asset_service),
):
    asset = await service.get_by_id(asset_id)
    if asset is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )
    return asset


@router.get("/ticker/{ticker}", response_model=AssetResponse)
async def get_asset_by_ticker(
    ticker: str,
    service: AssetService = Depends(get_asset_service),
):
    asset = await service.get_by_ticker(ticker)
    if asset is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )
    return asset


@router.get("/type/{asset_type}", response_model=list[AssetResponse])
async def list_assets_by_type(
    asset_type: AssetType,
    service: AssetService = Depends(get_asset_service),
):
    return await service.list_by_type(asset_type)


@router.post(
    "/stocks",
    response_model=AssetResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_stock(
    data: StockCreate,
    service: AssetService = Depends(get_asset_service),
):
    try:
        return await service.create_stock(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/bonds",
    response_model=AssetResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_bond(
    data: BondCreate,
    service: AssetService = Depends(get_asset_service),
):
    try:
        return await service.create_bond(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/etfs",
    response_model=AssetResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_etf(
    data: ETFCreate,
    service: AssetService = Depends(get_asset_service),
):
    try:
        return await service.create_etf(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/currencies",
    response_model=AssetResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_currency(
    data: CurrencyAssetCreate,
    service: AssetService = Depends(get_asset_service),
):
    try:
        return await service.create_currency(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{asset_id}")
async def delete_asset(
    asset_id: int,
    service: AssetService = Depends(get_asset_service),
):
    deleted = await service.delete(asset_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )

    return {"message": "Asset deleted successfully"}