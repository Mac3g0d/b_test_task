from uuid import UUID
from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy import delete
from sqlmodel import select
from sqlalchemy.orm import selectinload, joinedload
from sqlmodel.ext.asyncio.session import AsyncSession


class BaseDAO:

    def __init__(self, model):
        self.model = model

    async def get(
            self,
            session: AsyncSession,
            *,
            id: UUID
    ):
        response = await session.exec(
            select(self.model).where(self.model.id == id).options(joinedload('*', innerjoin=True))
        )

        return response.first()

    async def list(
            self,
            session: AsyncSession,
            *,
            limit: int = 100,
            offset: int = 0
    ):
        response = await session.exec(
            select(self.model).offset(offset).limit(limit).options(selectinload('*'))
        )

        return response.all()

    async def create(
            self,
            session: AsyncSession,
            *,
            obj_in
    ):
        db_obj = self.model.from_orm(obj_in)

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)

        return db_obj

    async def update(
            self,
            session: AsyncSession,
            *,
            obj_current,
            obj_new
    ):
        obj_data = jsonable_encoder(obj_current)

        if isinstance(obj_new, dict):
            update_data = obj_new

        else:
            update_data = obj_new.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(obj_current, field, update_data[field])

            if field == "updated_at":
                setattr(obj_current, field, datetime.utcnow())

        session.add(obj_current)
        await session.commit()
        await session.refresh(obj_current)

        return obj_current

    async def delete(self, session, *, id: UUID):
        instance = await self.get(session, id=id)
        await session.delete(instance)
        await session.commit()

    async def filter(self,
                     session: AsyncSession,
                     *,
                     stmt):
        response = await session.exec(
            select(self.model).where(*stmt).options(selectinload('*'))
        )

        return response.first()
