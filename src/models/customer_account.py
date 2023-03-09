from typing import TYPE_CHECKING, Self
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy import case
from sqlalchemy_utils import aggregated
from sqlmodel import Field, Relationship, SQLModel

from .account_operation import AccountOperation

if TYPE_CHECKING:
    from .currency import Currency
    from .customer import Customer


class CustomerAccountBase(SQLModel):

    class Config:
        arbitrary_types_allowed = True


class CustomerAccount(CustomerAccountBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    customer_id: UUID = Field(nullable=False, foreign_key="customer.id")
    currency_id: UUID = Field(nullable=False, foreign_key="currency.id")

    currency: "Currency" = Relationship(back_populates="customer_accounts")

    customer: "Customer" = Relationship(back_populates="accounts")

    operations: list["AccountOperation"] | None = Relationship(back_populates="account",
                                                               sa_relationship_kwargs={"cascade": "all, delete"})

    @aggregated("operations", sa.Column(sa.Numeric, nullable=False, default=0))
    def balance(self: Self):  # noqa: ANN201
        return sa.func.sum(
            case((AccountOperation.type == "d", AccountOperation.amount),
                 (AccountOperation.type == "c", -AccountOperation.amount),
                 else_=0),
        )
