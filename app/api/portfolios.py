from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.repositories.user_repository import UserRepository
from app.repositories.portfolio_repository import PortfolioRepository
from app.services.portfolio_service import PortfolioService
from app.schemas.portfolio import PortfolioCreate, PortfolioResponse


router = APIRouter(
    prefix="/portfolios",
    tags=["Portfolios"],
)


def get_portfolio_service(
    session: AsyncSession = Depends(get_session),
) -> PortfolioService:
    user_repo = UserRepository(session)
    portfolio_repo = PortfolioRepository(session)
    return PortfolioService(portfolio_repo, user_repo)


@router.post("/", response_model=PortfolioResponse, status_code=status.HTTP_201_CREATED)
async def create_portfolio(
    user_id: int,
    data: PortfolioCreate,
    service: PortfolioService = Depends(get_portfolio_service),
):
    try:
        return await service.create_portfolio(user_id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{portfolio_id}", response_model=PortfolioResponse)
async def get_portfolio(
    portfolio_id: int,
    service: PortfolioService = Depends(get_portfolio_service),
):
    try:
        return await service.get_by_id(portfolio_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/user/{user_id}", response_model=list[PortfolioResponse])
async def get_user_portfolios(
    user_id: int,
    service: PortfolioService = Depends(get_portfolio_service),
):
    try:
        return await service.get_user_portfolios(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/user/{user_id}/active", response_model=list[PortfolioResponse])
async def get_active_user_portfolios(
    user_id: int,
    service: PortfolioService = Depends(get_portfolio_service),
):
    try:
        return await service.get_active_user_portfolios(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{portfolio_id}/rename", response_model=PortfolioResponse)
async def rename_portfolio(
    portfolio_id: int,
    new_name: str,
    service: PortfolioService = Depends(get_portfolio_service),
):
    try:
        return await service.rename_portfolio(portfolio_id, new_name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{portfolio_id}/description", response_model=PortfolioResponse)
async def update_description(
    portfolio_id: int,
    description: str | None = None,
    service: PortfolioService = Depends(get_portfolio_service),
):
    try:
        return await service.update_description(portfolio_id, description)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{portfolio_id}/deactivate", response_model=PortfolioResponse)
async def deactivate_portfolio(
    portfolio_id: int,
    service: PortfolioService = Depends(get_portfolio_service),
):
    try:
        return await service.deactivate_portfolio(portfolio_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{portfolio_id}/activate", response_model=PortfolioResponse)
async def activate_portfolio(
    portfolio_id: int,
    service: PortfolioService = Depends(get_portfolio_service),
):
    try:
        return await service.activate_portfolio(portfolio_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{portfolio_id}")
async def delete_portfolio(
    portfolio_id: int,
    service: PortfolioService = Depends(get_portfolio_service),
):
    try:
        await service.delete_portfolio(portfolio_id)
        return {"message": "Portfolio deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))