from passlib.context import CryptContext

from app.models.user import User
from app.models.enums import UserRole
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(self, data: UserCreate) -> User:
        existing_user = await self.user_repo.get_by_email(data.email)
        if existing_user is not None:
            raise ValueError("User with this email already exists")

        password_hash = self.hash_password(data.password)

        user = User(
            email=data.email.lower().strip(),
            full_name=data.full_name.strip(),
            password_hash=password_hash,
            user_role=UserRole.INVESTOR,
        )

        return await self.user_repo.create(user)

    async def authenticate_user(
        self,
        email: str,
        password: str,
    ) -> User | None:
        user = await self.user_repo.get_by_email(email)

        if user is None:
            return None

        if not self.verify_password(password, user.password_hash):
            return None

        return user

    async def get_by_id(self, user_id: int) -> User:
        user = await self.user_repo.get_by_id(user_id)

        if user is None:
            raise ValueError("User not found")

        return user

    async def get_by_email(self, email: str) -> User:
        user = await self.user_repo.get_by_email(email)

        if user is None:
            raise ValueError("User not found")

        return user

    async def list_all(self) -> list[User]:
        return await self.user_repo.list_all()

    async def change_password(
        self,
        user_id: int,
        old_password: str,
        new_password: str,
    ) -> User:
        user = await self.user_repo.get_by_id(user_id)

        if user is None:
            raise ValueError("User not found")

        if not self.verify_password(old_password, user.password_hash):
            raise ValueError("Old password is incorrect")

        if len(new_password) < 6:
            raise ValueError("New password must be at least 6 characters long")

        new_hash = self.hash_password(new_password)

        updated_user = await self.user_repo.update(
            user_id,
            {"password_hash": new_hash},
        )

        if updated_user is None:
            raise ValueError("User not found")

        return updated_user

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        return pwd_context.verify(password, password_hash)