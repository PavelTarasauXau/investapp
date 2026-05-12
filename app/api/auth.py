from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session

from app.repositories.user_repository import UserRepository

from app.services.user_service import UserService

from app.schemas.auth import LoginRequest
from app.schemas.user import UserCreate, UserResponse

from app.core.security import security
from authx import TokenPayload


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


def get_user_service(
    session: AsyncSession = Depends(get_session),
) -> UserService:
    user_repo = UserRepository(session)
    return UserService(user_repo)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
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


@router.post("/login")
async def login(
    data: LoginRequest,
    service: UserService = Depends(get_user_service),
):
    user = await service.authenticate_user(
        email=data.email,
        password=data.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = security.create_access_token(
        uid=str(user.id)
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.get("/me")
async def get_me(
    payload: TokenPayload = Depends(security.access_token_required),
    service: UserService = Depends(get_user_service),
):
    user = await service.get_by_id(int(payload.sub))

    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
    }