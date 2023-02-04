from decimal import Decimal
from uuid import UUID

from fastapi import Body
from pydantic import BaseModel, Field

from ..models.customer_account import CustomerAccountBase
from .currencies import ReadCurrency
#from .customer import ReadCustomer
from .account_operation import ReadAccountOperation


class CreateCustomerAccount(BaseModel):
    customer_id: UUID = Body()
    currency_id: UUID = Body()


class ReadCustomerAccount(CustomerAccountBase):
    id: UUID
    #customer: ReadCustomer

    currency: ReadCurrency
    operations: list[ReadAccountOperation]
    balance: Decimal | None


class ReadCustomerAccounts(BaseModel):
    results: list[ReadCustomerAccount] | list


class UpdateCustomerAccount(BaseModel):
    customer_id: UUID = Body()
    currency_id: UUID = Body()

