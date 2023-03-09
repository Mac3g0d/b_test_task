from typing import Self

from ...models import Currency
from .basemodel import BaseDAO


class CurrencyDAO(BaseDAO):
    def __init__(self: Self) -> None:
        self.model = Currency
        super().__init__(model=self.model)
