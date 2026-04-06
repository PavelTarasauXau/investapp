from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import override
from app.models.user import User
from app.repositories.abstract_repository import AbstractRepository

class UserRepository(AbstractRepository[User]):
    def __init__(self, session: AsyncSession):
        self.session = session

    @override
    async def create(self, entity: User) -> User:
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    @override
    async def get_by_id(self, entity_id: int) -> User | None:
        return await self.session.get(User, entity_id)

    @override
    async def list_all(self) -> list[User]:
        result = await self.session.execute(select(User))
        return list(result.scalars().all())

    @override
    async def delete(self, entity_id: int) -> bool:
        user = await self.session.get(User, entity_id)
        if user is None:
            return False
        await self.session.delete(user)
        await self.session.commit()
        return True

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.email == email.lower().strip())
        )
        return result.scalar_one_or_none()
    
    @override
    async def update(self, entity_id: int, data: dict) -> User | None:
        user = await self.session.get(User, entity_id)
        if user is None:
            return None
        for key, value in data.items():
            setattr(user, key, value)
        await self.session.commit()
        await self.session.refresh(user)
        return user