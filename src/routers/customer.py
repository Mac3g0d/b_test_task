from uuid import UUID

from fastapi import Request, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.database import get_session
from ..services.DAO import CustomerDAO
from ..schemas import CreateCustomer, ReadCustomer, ReadCustomers, UpdateCustomer

router = APIRouter()
DAO = CustomerDAO()


@router.post("/", response_model=ReadCustomer, status_code=201)
async def create_customer(request: Request, customer: CreateCustomer, session: AsyncSession = Depends(get_session)):
    created_customer = await DAO.create(session=session, obj_in=customer)
    return created_customer


@router.get("/", response_model=ReadCustomers)
async def get_customers(request: Request, limit: int = 100, offset: int = 0, session: AsyncSession = Depends(get_session)):
    customers = await DAO.list(session=session, limit=limit, offset=offset)
    return {'results': customers or []}


@router.get("/{customer_id}", response_model=ReadCustomer)
async def get_customer(request: Request, customer_id: UUID, session: AsyncSession = Depends(get_session)):
    customer = await DAO.get_customer_detail(session=session, id=customer_id)
    return customer


@router.patch("/{customer_id}", response_model=ReadCustomer)
async def update_customer(request: Request, customer_id: UUID, customer: UpdateCustomer, session: AsyncSession = Depends(get_session)):
    current_customer = await DAO.get(session=session, id=customer_id)
    updated_customer = await DAO.update(session=session, obj_current=current_customer, obj_new=customer)
    return updated_customer


@router.delete("/{customer_id}", status_code=204)
async def delete_customer(request: Request, customer_id: UUID, session: AsyncSession = Depends(get_session)) -> None:
    await DAO.delete(session=session, id=customer_id)

