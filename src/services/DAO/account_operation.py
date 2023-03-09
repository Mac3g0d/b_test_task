from typing import Self

from ...models import AccountOperation
from .basemodel import BaseDAO


class AccountOperationDAO(BaseDAO):
    def __init__(self: Self) -> None:
        self.model = AccountOperation
        super().__init__(model=self.model)
