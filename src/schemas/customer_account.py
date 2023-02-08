from decimal import Decimal
from uuid import UUID

from fastapi import Body
from pydantic import BaseModel

from ..models.customer_account import CustomerAccountBase
from .currencies import ReadCurrency


class CreateCustomerAccount(BaseModel):
    customer_id: UUID = Body()
    currency_id: UUID = Body()


class ReadCustomerAccount(CustomerAccountBase):
    id: UUID
    currency: ReadCurrency
    balance: Decimal | None


class ReadCustomerAccounts(BaseModel):
    results: list[ReadCustomerAccount] | list


class UpdateCustomerAccount(BaseModel):
    customer_id: UUID = Body()
    currency_id: UUID = Body()

