from decimal import Decimal
from enum import Enum
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class OperationType(str, Enum):
    DEBIT = 'd'
    CREDIT = 'c'


class AccountOperation(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    customer_account_id: UUID = Field(nullable=False, foreign_key='customeraccount.id')
    type: OperationType
    amount: Decimal = Field(gt=Decimal(0))
