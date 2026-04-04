import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

from app.database.session import DATABASE_URL  # важно

engine = create_async_engine(DATABASE_URL)


async def test():
    async with engine.begin() as conn:
        print("Connected!")


if __name__ == "__main__":
    asyncio.run(test())