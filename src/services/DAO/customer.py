from datetime import datetime

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
        customer_stmt = select(self.model).where(self.model.id == id).options(selectinload('*'))
        customer = (await session.scalars(customer_stmt)).first()
        return customer

    async def get_profits(self,
                          session: AsyncSession,
                          *,
                          currency_name: Currency.name,
                          date: datetime.date):


        stmt = select(
            func.distinct(self.model.name).label('customer_name'),
            Currency.name.label('currency_name'),
            func.sum(
                case(
                    ((AccountOperation.type == 'd')
                     & (func.DATE(AccountOperation.created_at) == date), AccountOperation.amount),
                    ((AccountOperation.type == 'c')
                     & (func.DATE(AccountOperation.created_at) == date), -AccountOperation.amount),
                    else_=0
                )).label('profit_for_given_date'),
            func.sum(
                case(((AccountOperation.type == 'd')
                      & (func.DATE(AccountOperation.created_at) <= date), AccountOperation.amount),
                     ((AccountOperation.type == 'c')
                      & (func.DATE(AccountOperation.created_at) <= date), -AccountOperation.amount),
                     else_=0)
            ).label('balance_on_given_date'))\
            .join(self.model.accounts).join(CustomerAccount.operations) \
            .where(Currency.name == currency_name).group_by(self.model, Currency.name)
        profits = (await session.execute(stmt)).all()
        return profits
