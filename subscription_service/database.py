from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/subscription_db"

# Create asynchronous engine and session
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# Dependency to get the database session


async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
