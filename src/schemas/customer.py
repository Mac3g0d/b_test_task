from uuid import UUID

from fastapi import Body
from pydantic import BaseModel, Field

from ..models.customer import CustomerBase
from .customer_account import ReadCustomerAccount


class CreateCustomer(CustomerBase):
    name: str = Body()


class ReadCustomer(CustomerBase):
    id: UUID
    accounts: list[ReadCustomerAccount] | list


class ReadCustomers(BaseModel):
    results: list[ReadCustomer] | list


class UpdateCustomer(CustomerBase):
    name: str = Body()

