import random
from decimal import Decimal

from async_factory_boy.factory.sqlalchemy import AsyncSQLAlchemyFactory
from factory import Faker, SubFactory, LazyFunction
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

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


class CustomerFactory(SAFactory):
    id = Faker('uuid4')
    name = Faker('name')

    class Meta:
        model = Customer


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
    customer = SubFactory(CustomerFactory)
    currency = SubFactory(CurrencyFactory)

    class Meta:
        model = CustomerAccount


class AccountOperationFactory(SAFactory):
    id = Faker('uuid4')
    customer_account_id = Faker('uuid4')
    account = SubFactory(CustomerAccountFactory)
    type = random.choice(['d', 'c'])
    amount = LazyFunction(lambda: Decimal(f'{random.randrange(500)}.{random.randrange(500)}'))

    class Meta:
        model = AccountOperation
