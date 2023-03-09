from uuid import UUID

from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from ..db.database import get_session
from ..schemas import CreateCustomer, GetProfitsQuery, ReadCustomer, ReadCustomers, ReadDetailCustomer, UpdateCustomer
from ..services.DAO import CustomerDAO

router = APIRouter()
DAO = CustomerDAO()


@router.post("/", response_model=ReadCustomer, status_code=201)
async def create_customer(customer: CreateCustomer, session: AsyncSession = Depends(get_session)) -> ReadCustomer:
    return await DAO.create(session=session, obj_in=customer, accounts=[])


@router.get("/get_profits")
async def get_profits(query: GetProfitsQuery = Depends(GetProfitsQuery), session: AsyncSession = Depends(get_session)) -> dict:
    profits = await DAO.get_profits(session, currency_name=query.currency_name, date=query.date)
    return {"results": profits}


@router.get("/", response_model=ReadCustomers)
async def get_customers(limit: int = 100, offset: int = 0, session: AsyncSession = Depends(get_session)) -> ReadCustomers:
    customers = await DAO.list(session=session, limit=limit, offset=offset)
    return {"results": customers or []}


@router.get("/{customer_id}", response_model=ReadDetailCustomer | None)
async def get_customer(customer_id: UUID = Path(), session: AsyncSession = Depends(get_session)) -> ReadDetailCustomer | None:
    customer = await DAO.get_customer_detail(session=session, id=customer_id)
    if customer:
        return customer
    return Response("customer not found", status_code=400)


@router.patch("/{customer_id}", response_model=ReadCustomer)
async def update_customer(customer: UpdateCustomer,
                          customer_id: UUID = Path(),
                          session: AsyncSession = Depends(get_session)) -> ReadCustomer:
    return await DAO.update(session=session, obj_new=customer, id=customer_id)


@router.delete("/{customer_id}", status_code=204)
async def delete_customer(customer_id: UUID = Path(), session: AsyncSession = Depends(get_session)) -> None:
    await DAO.delete(session=session, id=customer_id)
