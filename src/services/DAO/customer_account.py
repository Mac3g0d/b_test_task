from sqlalchemy.sql import select, func, case
from sqlalchemy.orm import joinedload
from sqlmodel.ext.asyncio.session import AsyncSession

from .base import BaseDAO
from ...models import CustomerAccount, AccountOperation


class CustomerAccountDAO(BaseDAO):
    def __init__(self):
        self.model = CustomerAccount
        super().__init__(model=self.model)

    async def get_customer_account_detail(self,
                                          session: AsyncSession,
                                          *,
                                          id):
        balance = await session.scalars(
            select(
                func.sum(AccountOperation.amount * case((AccountOperation.type == 'd', 1), else_=-1)))
            .where(self.model.id == id)
            .options(joinedload('*', innerjoin=True)))

        balance = balance.first()
        account = await self.get(session, id=id)
        return {**account.dict(), 'balance': balance, 'currency': account.currency, 'operations': account.operations}
