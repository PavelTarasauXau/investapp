from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import override

from app.models.user import User
from app.orm.user_orm import UserORM
from app.repositories.abstract_repository import AbstractRepository


class UserRepository(AbstractRepository[User]):
    def __init__(self, session: AsyncSession):
        self.session = session

    @override
    async def create(self, entity: User) -> User:
        orm_user = UserORM(
            email=entity.email,
            full_name=entity.full_name,
            password_hash=entity.password_hash,
            created_at=entity.created_at,
        )

        self.session.add(orm_user)
        await self.session.commit()
        await self.session.refresh(orm_user)

        return User(
            id=orm_user.id,
            email=orm_user.email,
            full_name=orm_user.full_name,
            password_hash=orm_user.password_hash,
            created_at=orm_user.created_at,
        )

    @override
    async def get_by_id(self, entity_id: int) -> User | None:
        orm_user = await self.session.get(UserORM, entity_id)
        if orm_user is None:
            return None

        return User(
            id=orm_user.id,
            email=orm_user.email,
            full_name=orm_user.full_name,
            password_hash=orm_user.password_hash,
            created_at=orm_user.created_at,
        )

    @override
    async def list_all(self) -> list[User]:
        result = await self.session.execute(select(UserORM))
        orm_users = result.scalars().all()

        return [
            User(
                id=user.id,
                email=user.email,
                full_name=user.full_name,
                password_hash=user.password_hash,
                created_at=user.created_at,
            )
            for user in orm_users
        ]

    @override
    async def delete(self, entity_id: int) -> bool:
        orm_user = await self.session.get(UserORM, entity_id)
        if orm_user is None:
            return False

        await self.session.delete(orm_user)
        await self.session.commit()
        return True

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(UserORM).where(UserORM.email == email.lower().strip())
        )
        orm_user = result.scalar_one_or_none()

        if orm_user is None:
            return None

        return User(
            id=orm_user.id,
            email=orm_user.email,
            full_name=orm_user.full_name,
            password_hash=orm_user.password_hash,
            created_at=orm_user.created_at,
        )