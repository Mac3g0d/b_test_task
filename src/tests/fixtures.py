import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from starlette.testclient import TestClient

from src.db.database import get_session
from src.app import app


_ = pytest.fixture(autouse=True)(lambda db: None)


@pytest.fixture(name="session")
async def session_fixture():
    engine = create_async_engine('')

    async_session = sessionmaker(bind=engine,
                                 class_=AsyncSession,
                                 expire_on_commit=False,
                                 )
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    with async_session() as session:
        yield session


@pytest.fixture(name="client")
async def client_fixture(session: AsyncSession):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

