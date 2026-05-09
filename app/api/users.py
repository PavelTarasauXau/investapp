from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserResponse


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


def get_user_service(
    session: AsyncSession = Depends(get_session),
) -> UserService:
    user_repo = UserRepository(session)
    return UserService(user_repo)

"""
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    data: UserCreate,
    service: UserService = Depends(get_user_service),
):
    try:
        return await service.register_user(data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
"""

@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
async def get_user_by_id(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    try:
        return await service.get_by_id(user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=list[UserResponse],
)
async def list_users(
    service: UserService = Depends(get_user_service),
):
    return await service.list_all()