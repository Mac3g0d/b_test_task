import random
from decimal import Decimal

import factory

from ..models import Customer, CustomerAccount, Currency, AccountOperation
from ..db.database import async_session


class CustomerFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Faker('uuid4')
    name = factory.Faker('name')

    class Meta:
        model = Customer
        sqlalchemy_session = async_session()


class CurrencyFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Faker('uuid4')
    name = factory.Faker('name')
    default = False

    class Meta:
        model = Currency
        sqlalchemy_session = async_session()


class CustomerAccountFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Faker('uuid4')
    customer_id = factory.Faker('uuid4')
    currency_id = factory.Faker('uuid4')
    customer = factory.SubFactory(CustomerFactory)
    currency = factory.SubFactory(CurrencyFactory)

    class Meta:
        model = CustomerAccount
        sqlalchemy_session = async_session()


class AccountOperationFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Faker('uuid4')
    customer_account_id = factory.Faker('uuid4')
    account = factory.SubFactory(CustomerAccountFactory)
    type = random.choice(['d', 'c'])
    amount = factory.LazyFunction(lambda: Decimal(f'{random.randrange(500)}.{random.randrange(500)}'))

    class Meta:
        model = AccountOperation
        sqlalchemy_session = async_session
