import asyncio
import random

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


@pytest_asyncio.fixture(name='session', scope='function')
async def db_session() -> AsyncSession:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

        async with async_session() as session:
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
    usdt = await CurrencyFactory.create(name='USDT')
    rub = await CurrencyFactory.create(name='RUB')
    eur = await CurrencyFactory.create(name='EUR')
    _customer = await CustomerFactory.create()
    ac_usdt = await CustomerAccountFactory.create(currency_id=usdt.id, customer_id=_customer.id)
    ac_rub = await CustomerAccountFactory.create(currency_id=rub.id, customer_id=_customer.id)
    ac_eur = await CustomerAccountFactory.create(currency_id=eur.id, customer_id=_customer.id)

    await AccountOperationFactory.create_batch(50, customer_account_id=ac_usdt.id, account=ac_usdt)
    await AccountOperationFactory.create_batch(50, customer_account_id=ac_rub.id, account=ac_rub)
    await AccountOperationFactory.create_batch(50, customer_account_id=ac_eur.id, account=ac_eur)


    return _customer


@pytest_asyncio.fixture
async def many_customers():
    return await CustomerFactory.create_batch(random.randrange(5, 25))


@pytest.fixture
def customer_data():
    return CustomerFactory.build()


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
