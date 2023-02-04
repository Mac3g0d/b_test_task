from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, Relationship


if TYPE_CHECKING:
    from .currency import Currency

    from .customer import Customer
    from .account_operation import AccountOperation


class CustomerAccountBase(SQLModel):
    pass


class CustomerAccount(CustomerAccountBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    customer_id: UUID = Field(nullable=False, foreign_key='customer.id')
    currency_id: UUID = Field(nullable=False, foreign_key='currency.id')

    currency: "Currency" = Relationship()
    customer: "Customer" = Relationship()

    customers: list["Customer"] = Relationship(back_populates="accounts")

    operations: list["AccountOperation"] = Relationship(back_populates="account")


