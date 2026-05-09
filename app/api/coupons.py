from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.repositories.coupon_payment_repository import CouponPaymentRepository
from app.schemas.coupon_payment import CouponPaymentCreate, CouponPaymentResponse


router = APIRouter(
    prefix="/coupons",
    tags=["Coupons"],
)


def get_coupon_repo(
    session: AsyncSession = Depends(get_session),
) -> CouponPaymentRepository:
    return CouponPaymentRepository(session)


@router.post("/", response_model=CouponPaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_coupon(
    data: CouponPaymentCreate,
    repo: CouponPaymentRepository = Depends(get_coupon_repo),
):
    try:
        from app.models.coupon_payment import CouponPayment

        coupon = CouponPayment(
            bond_id=data.bond_id,
            coupon_number=data.coupon_number,
            payment_date=data.payment_date,
            coupon_amount=data.coupon_amount,
        )

        return await repo.create(coupon)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{coupon_id}", response_model=CouponPaymentResponse)
async def get_coupon(
    coupon_id: int,
    repo: CouponPaymentRepository = Depends(get_coupon_repo),
):
    coupon = await repo.get_by_id(coupon_id)

    if coupon is None:
        raise HTTPException(status_code=404, detail="Coupon payment not found")

    return coupon


@router.get("/bond/{bond_id}", response_model=list[CouponPaymentResponse])
async def get_bond_coupons(
    bond_id: int,
    repo: CouponPaymentRepository = Depends(get_coupon_repo),
):
    return await repo.get_by_bond_id(bond_id)


@router.delete("/{coupon_id}")
async def delete_coupon(
    coupon_id: int,
    repo: CouponPaymentRepository = Depends(get_coupon_repo),
):
    deleted = await repo.delete(coupon_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Coupon payment not found")

    return {"message": "Coupon payment deleted successfully"}