from app.database.session import engine, Base
from app.models.user import User

# импортируем ORM-модели, чтобы SQLAlchemy их увидел
from app.models.user import User


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    import asyncio
    asyncio.run(init_db())