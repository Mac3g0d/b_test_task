from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Currency(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str
    default: bool = Field(default=False)
