from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from .customer_account import CustomerAccount


class CurrencyBase(SQLModel):
    name: str
    default: bool = Field(default=False)


class Currency(CurrencyBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

    customer_accounts: list[CustomerAccount] = Relationship(back_populates="currency")

