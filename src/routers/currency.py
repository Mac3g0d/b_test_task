from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.database import get_session
from ..schemas import CreateCurrency, ReadCurrencies, ReadCurrency, UpdateCurrency
from ..services.DAO import CurrencyDAO

router = APIRouter()
DAO = CurrencyDAO()


@router.post("/", response_model=ReadCurrency, status_code=201)
async def create_currency(currency: CreateCurrency, session: AsyncSession = Depends(get_session)) -> ReadCurrency:
    return await DAO.create(session=session, obj_in=currency)


@router.get("/", response_model=ReadCurrencies)
async def get_currencies(limit: int = 100, offset: int = 0, session: AsyncSession = Depends(get_session)) -> ReadCurrency:
    currencies = await DAO.list(session=session, limit=limit, offset=offset)
    return {"results": currencies or []}


@router.get("/{currency_id}", response_model=ReadCurrency)
async def get_currency(currency_id: UUID, session: AsyncSession = Depends(get_session)) -> ReadCurrency:
    return await DAO.get(session=session, id=currency_id)


@router.patch("/{currency_id}", response_model=ReadCurrency)
async def update_currency(currency_id: UUID, currency: UpdateCurrency, session: AsyncSession = Depends(get_session)) -> ReadCurrency:
    return await DAO.update(session=session, id=currency_id, obj_new=currency)


@router.delete("/{currency_id}", status_code=204)
async def delete_currency(currency_id: UUID, session: AsyncSession = Depends(get_session)) -> None:
    await DAO.delete(session=session, id=currency_id)

