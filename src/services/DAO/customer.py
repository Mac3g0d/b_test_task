from datetime import datetime
from typing import Self
from uuid import UUID

from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ...models import AccountOperation, Currency, Customer, CustomerAccount
from .basemodel import BaseDAO


class CustomerDAO(BaseDAO):
    def __init__(self: Self) -> None:
        self.model = Customer
        super().__init__(model=self.model)

    async def get_customer_detail(self: Self,
                                  session: AsyncSession,
                                  *,
                                  id: str | UUID) -> Customer:
        customer_stmt = select(self.model).where(self.model.id == id).options(selectinload("*"))
        return (await session.scalars(customer_stmt)).first()

    async def get_profits(self: Self,
                          session: AsyncSession,
                          *,
                          currency_name: Currency.name,
                          date: datetime.date) -> dict:
        stmt = select(
            func.distinct(self.model.name).label("customer_name"),
            Currency.name.label("currency_name"),
            func.sum(
                case(
                    ((AccountOperation.type == "d")
                     & (func.DATE(AccountOperation.created_at) == date), AccountOperation.amount),
                    ((AccountOperation.type == "c")
                     & (func.DATE(AccountOperation.created_at) == date), -AccountOperation.amount),
                    else_=0,
                )).label("profit_for_given_date"),
            func.sum(
                case(((AccountOperation.type == "d")
                      & (func.DATE(AccountOperation.created_at) <= date), AccountOperation.amount),
                     ((AccountOperation.type == "c")
                      & (func.DATE(AccountOperation.created_at) <= date), -AccountOperation.amount),
                     else_=0),
            ).label("balance_on_given_date")) \
            .join(self.model.accounts).join(CustomerAccount.operations) \
            .where(Currency.name == currency_name).group_by(self.model, Currency.name)

        return (await session.execute(stmt)).all()
