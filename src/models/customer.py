from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .customer_account import CustomerAccount


class CustomerBase(SQLModel):
    name: str


class Customer(CustomerBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

    accounts: list["CustomerAccount"] | None = Relationship(back_populates="customer",
                                                            sa_relationship_kwargs={"cascade": "all, delete"})



