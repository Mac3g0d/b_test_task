from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from ..settings import get_settings

settings = get_settings()

engine = create_async_engine(settings.DATABASE_URI,
                             pool_size=settings.POOL_SIZE,
                             max_overflow=64,
                             future=True,
                             pool_pre_ping=True,
                             echo=True)

async_session = sessionmaker(bind=engine,
                             class_=AsyncSession,
                             expire_on_commit=False,
                             )


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
