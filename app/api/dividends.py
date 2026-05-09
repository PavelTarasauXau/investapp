from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.repositories.dividend_payment_repository import DividendPaymentRepository
from app.schemas.dividend_payment import DividendPaymentCreate, DividendPaymentResponse


router = APIRouter(
    prefix="/dividends",
    tags=["Dividends"],
)


def get_dividend_repo(
    session: AsyncSession = Depends(get_session),
) -> DividendPaymentRepository:
    return DividendPaymentRepository(session)


@router.post("/", response_model=DividendPaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_dividend(
    data: DividendPaymentCreate,
    repo: DividendPaymentRepository = Depends(get_dividend_repo),
):
    try:
        from app.models.dividend_payment import DividendPayment

        dividend = DividendPayment(
            stock_id=data.stock_id,
            record_date=data.record_date,
            payment_date=data.payment_date,
            dividend_per_share=data.dividend_per_share,
        )

        return await repo.create(dividend)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{dividend_id}", response_model=DividendPaymentResponse)
async def get_dividend(
    dividend_id: int,
    repo: DividendPaymentRepository = Depends(get_dividend_repo),
):
    dividend = await repo.get_by_id(dividend_id)

    if dividend is None:
        raise HTTPException(status_code=404, detail="Dividend payment not found")

    return dividend


@router.get("/stock/{stock_id}", response_model=list[DividendPaymentResponse])
async def get_stock_dividends(
    stock_id: int,
    repo: DividendPaymentRepository = Depends(get_dividend_repo),
):
    return await repo.get_by_stock_id(stock_id)


@router.delete("/{dividend_id}")
async def delete_dividend(
    dividend_id: int,
    repo: DividendPaymentRepository = Depends(get_dividend_repo),
):
    deleted = await repo.delete(dividend_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Dividend payment not found")

    return {"message": "Dividend payment deleted successfully"}