from app.database.session import engine, Base
from app.orm.user_orm import UserORM

# импортируем ORM-модели, чтобы SQLAlchemy их увидел
from app.orm.user_orm import UserORM


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    import asyncio
    asyncio.run(init_db())