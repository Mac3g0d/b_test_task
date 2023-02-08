import datetime
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4
from sqlalchemy import case

from sqlalchemy.ext.hybrid import hybrid_property
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .customer_account import CustomerAccount


class OperationType(str, Enum):
    DEBIT = 'd'
    CREDIT = 'c'


class AccountOperationBase(SQLModel):
    type: OperationType
    amount: Decimal = Field(gt=Decimal(0))

    class Config:
        arbitrary_types_allowed = True


class AccountOperation(AccountOperationBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    customer_account_id: UUID = Field(nullable=False, foreign_key='customeraccount.id')

    account: 'CustomerAccount' = Relationship(back_populates="operations")

    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now, nullable=False)

    # @hybrid_property
    # def fact_amount(self) -> Decimal:
    #     return self.amount if self.type == OperationType.DEBIT.value else -self.amount
    #
    # @fact_amount.expression
    # def fact_amount(cls):
    #     return case(
    #         (cls.type == OperationType.DEBIT.value, cls.amount),
    #         else_=-cls.amount
    #     )
