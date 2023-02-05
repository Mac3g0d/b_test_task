import asyncio

import pytest
import pytest_asyncio
from sqlmodel import SQLModel
from fastapi.testclient import TestClient
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.database import get_session
from src.app import app
from .fixture_factory import CustomerFactory, CurrencyFactory, CustomerAccountFactory, AccountOperationFactory, engine, \
    async_session

_ = pytest.fixture(autouse=True)(lambda db: None)


@pytest.fixture(scope='session')
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name='session', scope='session', autouse=True)
async def db_session() -> AsyncSession:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

        async with async_session(bind=conn) as session:
            yield session
            await session.flush()
            await session.rollback()


@pytest.fixture(name="client")
def client_fixture(session: AsyncSession):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    yield TestClient(app, base_url='http://test_server/api/v1')
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def customer():
    return await CustomerFactory.create()


@pytest_asyncio.fixture
async def customer_data():
    return await CustomerFactory.build()


@pytest_asyncio.fixture
async def currency():
    return await CurrencyFactory()


@pytest_asyncio.fixture
async def currency_data():
    return await CurrencyFactory.build()


@pytest_asyncio.fixture
async def customer_account():
    return await CustomerAccountFactory()


@pytest_asyncio.fixture
async def customer_account_data():
    return await CustomerAccountFactory.build()


@pytest_asyncio.fixture
async def account_operation():
    return await AccountOperationFactory()


@pytest_asyncio.fixture
async def account_operation_data():
    return AccountOperationFactory.build()
