from typing import Self
from uuid import UUID

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import SQLModel, select


class BaseModel(SQLModel):
    id: UUID


class BaseDAO:

    def __init__(self: Self, model: BaseModel) -> None:
        self.model = model

    async def get(
            self: Self,
            session: AsyncSession,
            *,
            id: UUID,
    ) -> BaseModel:
        return await session.scalar(
            select(self.model).where(self.model.id == id).options(selectinload("*")),
        )

    async def list(
            self: Self,
            session: AsyncSession,
            *,
            limit: int = 100,
            offset: int = 0,
    ) -> list[BaseModel]:
        response = await session.scalars(
            select(self.model).offset(offset).limit(limit).options(selectinload("*")),
        )

        return response.all()

    async def create(
            self: Self,
            session: AsyncSession,
            obj_in: BaseModel,
            **kwargs: dict,
    ) -> BaseModel:
        db_obj = self.model(**obj_in.dict(), **kwargs)
        session.add(db_obj)
        await session.commit()

        return db_obj

    async def update(
            self: Self,
            session: AsyncSession,
            *,
            id: str | UUID,
            obj_new: dict | BaseModel,
    ) -> BaseModel:

        update_data = obj_new if isinstance(obj_new, dict) else obj_new.dict(exclude_unset=True)

        await session.execute(update(self.model).where(self.model.id == id).values(**update_data))

        return await self.get(session, id=id)

    async def delete(self: Self, session: AsyncSession, *, id: UUID) -> None:
        instance = await self.get(session, id=id)
        await session.delete(instance)
        await session.commit()

    async def filter(self: Self,
                     session: AsyncSession,
                     *,
                     stmt: tuple,  # TODO: ADD TYPEHINT FOR STATEMENT!!!
                     ) -> BaseModel:
        response = await session.execute(
            select(self.model).where(*stmt).options(selectinload("*")),
        )

        return response.first()
