from uuid import UUID

from fastapi import Body
from pydantic import BaseModel

from ..models.currency import CurrencyBase


class CreateCurrency(CurrencyBase):
    name: str = Body()
    default: bool = Body()


class ReadCurrency(CurrencyBase):
    id: UUID


class ReadCurrencies(BaseModel):
    results: list[ReadCurrency] | list


class UpdateCurrency(CurrencyBase):
    name: str = Body()
    default: bool = Body()

