from .base import BaseDAO
from ...models import Currency


class CurrencyDAO(BaseDAO):
    def __init__(self):
        self.model = Currency
        super().__init__(model=self.model)
