from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.database import get_session
from ..schemas import CreateCustomerAccount, ReadCustomerAccount, ReadCustomerAccounts, UpdateCustomerAccount
from ..services.DAO import CustomerAccountDAO

router = APIRouter()
DAO = CustomerAccountDAO()


@router.post("/", response_model=ReadCustomerAccount, status_code=201)
async def create_customer_account(customer_account: CreateCustomerAccount,
                                  session: AsyncSession = Depends(get_session)) -> ReadCustomerAccount:
    return await DAO.create(session=session, obj_in=customer_account)


@router.get("/", response_model=ReadCustomerAccounts)
async def get_customer_accounts(limit: int = 100, offset: int = 0, session: AsyncSession = Depends(get_session)) -> ReadCustomerAccounts:
    customers = await DAO.list(session=session, limit=limit, offset=offset)
    return {"results": customers or []}


@router.get("/{customer_account_id}", response_model=ReadCustomerAccount)
async def get_customer_account(customer_account_id: UUID, session: AsyncSession = Depends(get_session)) -> ReadCustomerAccount:
    return await DAO.get(session=session, id=customer_account_id)


@router.patch("/{customer_account_id}", response_model=ReadCustomerAccount)
async def update_customer(customer_id: UUID,
                          customer_account: UpdateCustomerAccount,
                          session: AsyncSession = Depends(get_session)) -> ReadCustomerAccount:
    return await DAO.update(session=session, id=customer_id, obj_new=customer_account)


@router.delete("/{customer_account_id}", status_code=204)
async def delete_customer(customer_account_id: UUID, session: AsyncSession = Depends(get_session)) -> None:
    await DAO.delete(session=session, id=customer_account_id)
