from decimal import Decimal
from uuid import UUID

from fastapi import Body
from pydantic import BaseModel, Field

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


class Profits(BaseModel):
    results: list[Profit]


class ReadCustomers(BaseModel):
    results: list[ReadCustomer] | list


class UpdateCustomer(CustomerBase):
    name: str = Body()

