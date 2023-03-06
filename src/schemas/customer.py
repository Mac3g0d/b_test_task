import datetime
from decimal import Decimal
from uuid import UUID

from fastapi import Body, Query
from pydantic import BaseModel, Field, validator

from .customer_account import ReadCustomerAccount
from ..models.customer import CustomerBase


class CreateCustomer(CustomerBase):
    name: str = Body()


class ReadCustomer(CustomerBase):
    id: UUID
    accounts: list[ReadCustomerAccount] | list = Field(alias='accounts')


class ReadDetailCustomer(CustomerBase):
    id: UUID
    accounts: list[ReadCustomerAccount] | list = Field(alias='accounts')


class Profit(BaseModel):
    customer_name: str
    currency_name: str
    profit_for_given_date: Decimal
    balance_on_given_date: Decimal


class GetProfitsQuery(BaseModel):
    currency_name: str = Query(example='USDT')
    date: datetime.date | str = Query(example='01.01.1990')

    @validator('date', pre=True)
    def date_validation(cls, date):
        return datetime.datetime.strptime(
            date,
            "%d.%m.%Y"
        ).date()



class Profits(BaseModel):
    results: list[Profit]


class ReadCustomers(BaseModel):
    results: list[ReadCustomer] | list


class UpdateCustomer(CustomerBase):
    name: str = Body()
