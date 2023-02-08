from decimal import Decimal
from uuid import UUID

from fastapi import Body
from pydantic import BaseModel

from ..models.account_operation import AccountOperationBase


class CreateAccountOperation(AccountOperationBase):
    customer_account_id: UUID = Body()


class ReadAccountOperation(AccountOperationBase):
    id: UUID
    customer_account_id: UUID


class ReadAccountOperations(BaseModel):
    results: list[ReadAccountOperation] | list


class UpdateAccountOperation(AccountOperationBase):
    customer_account_id: UUID = Body()


