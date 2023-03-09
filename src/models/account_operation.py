import datetime
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .customer_account import CustomerAccount


class OperationType(str, Enum):
    DEBIT = "d"
    CREDIT = "c"


class AccountOperationBase(SQLModel):
    type: OperationType
    amount: Decimal = Field(gt=Decimal(0))

    class Config:
        arbitrary_types_allowed = True


class AccountOperation(AccountOperationBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    customer_account_id: UUID = Field(nullable=False, foreign_key="customeraccount.id")

    account: "CustomerAccount" = Relationship(back_populates="operations")

    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now, nullable=False)

