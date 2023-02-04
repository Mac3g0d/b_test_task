from uuid import UUID, uuid4
from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .customer_account import CustomerAccount


class CustomerBase(SQLModel):
    name: str


class Customer(CustomerBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

    accounts: list["CustomerAccount"] = Relationship(back_populates="customers")


