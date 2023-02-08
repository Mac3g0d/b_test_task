from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import case, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .base import BaseDAO
from ...models import Customer, Currency, AccountOperation, CustomerAccount


class CustomerDAO(BaseDAO):
    def __init__(self):
        self.model = Customer
        super().__init__(model=self.model)

    async def get_customer_detail(self,
                                  session: AsyncSession,
                                  *,
                                  id):
        customer_stmt = sa.select(self.model).where(self.model.id == id).options(selectinload('*'))
        customer = (await session.scalars(customer_stmt)).first()
        return customer

    async def get_profits(self,
                          session: AsyncSession,
                          *,
                          currency_name: Currency.name,
                          date: datetime.date):
        stmt = select(
            func.distinct(self.model.name),
            Currency.name,
            func.sum(
                case(
                    ((AccountOperation.type == 'd')
                     & (AccountOperation.created_at == func.DATE(date)), AccountOperation.amount),
                    ((AccountOperation.type == 'c') &
                     (AccountOperation.created_at == func.DATE(date)), -AccountOperation.amount),
                    else_=0
                ).label('profit_for_given_date')),
            sa.func.sum(
                case((AccountOperation.type == 'd', AccountOperation.amount),
                     (AccountOperation.type == 'c', -AccountOperation.amount),
                     else_=0)
            ).label('balance_on_given_date')
        ).where(
            Currency.name == currency_name
        ).options(selectinload('*')).group_by(self.model.name, Currency.name,)
        qq = (await session.execute(stmt)).all()
        from pprint import pprint
        pprint(qq)
        return qq
