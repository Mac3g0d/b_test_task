from uuid import UUID

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select


class BaseDAO:

    def __init__(self, model):
        self.model = model

    async def get(
            self,
            session: AsyncSession,
            *,
            id: UUID
    ):
        response = await session.scalar(
            select(self.model).where(self.model.id == id).options(selectinload('*'))
        )

        return response

    async def list(
            self,
            session: AsyncSession,
            *,
            limit: int = 100,
            offset: int = 0
    ):
        response = await session.scalars(
            select(self.model).offset(offset).limit(limit).options(selectinload('*'))
        )

        return response.all()

    async def create(
            self,
            session: AsyncSession,
            obj_in,
            **kwargs
    ):
        db_obj = self.model(**obj_in.dict(), **kwargs)
        session.add(db_obj)
        await session.commit()

        return db_obj

    async def update(
            self,
            session: AsyncSession,
            *,
            id,
            obj_new,
    ):

        if isinstance(obj_new, dict):
            update_data = obj_new

        else:
            update_data = obj_new.dict(exclude_unset=True)

        await session.execute(update(self.model).where(self.model.id == id).values(**update_data))

        return await self.get(session, id=id)

    async def delete(self, session, *, id: UUID):
        instance = await self.get(session, id=id)
        await session.delete(instance)
        await session.commit()

    async def filter(self,
                     session: AsyncSession,
                     *,
                     stmt):
        response = await session.execute(
            select(self.model).where(*stmt).options(selectinload('*'))
        )

        return response.first()
