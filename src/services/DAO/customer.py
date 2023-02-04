from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from sqlmodel.ext.asyncio.session import AsyncSession

from .base import BaseDAO
from ...models import Customer


class CustomerDAO(BaseDAO):
    def __init__(self):
        self.model = Customer
        super().__init__(model=self.model)

    async def get(
            self,
            session: AsyncSession,
            *,
            id: UUID
    ):
        # response = await session.exec(
        #     select(self.model).where(self.model.id == id).options(selectinload('*'))
        # )
        response = await session.scalars(select(self.model).where(self.model.id == id).options(joinedload('*', innerjoin=True)))

        return response.first()

    async def get_customer_detail(self,
                                  session: AsyncSession,
                                  *,
                                  id):
        customer = await self.get(session, id=id)
        print('\n\n')
        print(customer)
        print('\n\n')
        return customer
