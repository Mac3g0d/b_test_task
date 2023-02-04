from uuid import UUID

from fastapi import Request, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.database import get_session
from ..services.DAO import CurrencyDAO
from ..schemas import CreateCurrency, ReadCurrency, ReadCurrencies, UpdateCurrency

router = APIRouter()
DAO = CurrencyDAO()


@router.post("/", response_model=ReadCurrency, status_code=201)
async def create_currency(request: Request, currency: CreateCurrency, session: AsyncSession = Depends(get_session)):
    created_currency = await DAO.create(session=session, obj_in=currency)
    return created_currency


@router.get("/", response_model=ReadCurrencies)
async def get_currencies(request: Request, limit: int = 100, offset: int = 0, session: AsyncSession = Depends(get_session)):
    currencies = await DAO.list(session=session, limit=limit, offset=offset)
    return {'results': currencies or []}


@router.get("/{currency_id}", response_model=ReadCurrency)
async def get_currency(request: Request, currency_id: UUID, session: AsyncSession = Depends(get_session)):
    currency = await DAO.get(session=session, id=currency_id)
    return currency


@router.patch("/{currency_id}", response_model=ReadCurrency)
async def update_currency(request: Request, currency_id: UUID, currency: UpdateCurrency, session: AsyncSession = Depends(get_session)):
    current_currency = await DAO.get(session=session, id=currency_id)
    updated_currency = await DAO.update(session=session, obj_current=current_currency, obj_new=currency)
    return updated_currency


@router.delete("/{currency_id}", status_code=204)
async def delete_currency(request: Request, currency_id: UUID, session: AsyncSession = Depends(get_session)) -> None:
    await DAO.delete(session=session, id=currency_id)

