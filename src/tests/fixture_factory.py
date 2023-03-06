import random
import datetime
from decimal import Decimal

from async_factory_boy.factory.sqlalchemy import AsyncSQLAlchemyFactory
from factory import Faker, SubFactory, LazyFunction
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from ..models import Customer, CustomerAccount, Currency, AccountOperation

engine = create_async_engine("sqlite+aiosqlite://", future=True,
                             connect_args={"check_same_thread": False})
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


class SAFactory(AsyncSQLAlchemyFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = async_session()
        sqlalchemy_session_persistence = "commit"


class CurrencyFactory(SAFactory):
    id = Faker('uuid4')
    name = Faker('name')
    default = False

    class Meta:
        model = Currency


class CustomerAccountFactory(SAFactory):
    id = Faker('uuid4')
    customer_id = Faker('uuid4')
    currency_id = Faker('uuid4')
    currency = SubFactory(CurrencyFactory)

    class Meta:
        model = CustomerAccount


class CustomerFactory(SAFactory):
    id = Faker('uuid4')
    name = Faker('name')

    class Meta:
        model = Customer


class AccountOperationFactory(SAFactory):
    id = Faker('uuid4')
    customer_account_id = Faker('uuid4')
    account = SubFactory(CustomerAccountFactory)
    type = LazyFunction(lambda: random.choice(['d', 'c']))
    amount = LazyFunction(lambda: Decimal(f'{random.randrange(500)}.{random.randrange(500)}'))
    created_at = LazyFunction(lambda: datetime.datetime.now())

    class Meta:
        model = AccountOperation
