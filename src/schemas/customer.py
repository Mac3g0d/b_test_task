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


class ReadCustomers(BaseModel):
    results: list[ReadCustomer] | list


class UpdateCustomer(CustomerBase):
    name: str = Body()

