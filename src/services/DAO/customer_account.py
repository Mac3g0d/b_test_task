from typing import Self

from sqlalchemy.orm import joinedload
from sqlalchemy.sql import case, func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from ...models import AccountOperation, CustomerAccount
from .basemodel import BaseDAO


class CustomerAccountDAO(BaseDAO):
    def __init__(self: Self) -> None:
        self.model = CustomerAccount
        super().__init__(model=self.model)

    async def get_customer_account_detail(self: Self,
                                          session: AsyncSession,
                                          *,
                                          id: str) -> dict:
        balance = await session.scalars(
            select(
                func.sum(AccountOperation.amount * case((AccountOperation.type == "d", 1), else_=-1)))
            .where(self.model.id == id)
            .options(joinedload("*", innerjoin=True)))

        balance = balance.first()
        account = await self.get(session, id=id)
        return {**account.dict(), "balance": balance, "currency": account.currency, "operations": account.operations}
