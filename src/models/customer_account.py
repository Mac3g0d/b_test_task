from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class CustomerAccount(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    customer_id: UUID = Field(nullable=False, foreign_key='customer.id')
    currency_id: UUID = Field(nullable=False, foreign_key='currency.id')
