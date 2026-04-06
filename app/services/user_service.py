from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def register(self, data: UserCreate):
        if await self.repo.get_by_email(data.email):
            raise ValueError("Email already taken")
        return await self.repo.create(
            email=data.email.lower().strip(),
            full_name=data.full_name,
            password_hash=hash_password(data.password)
        )

    async def verify_password(self, email: str, password: str):
        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            return None
        return user