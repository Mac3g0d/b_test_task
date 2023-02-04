from .base import BaseDAO
from ...models import AccountOperation


class AccountOperationDAO(BaseDAO):
    def __init__(self):
        self.model = AccountOperation
        super().__init__(model=self.model)
