from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.database import get_session
from ..schemas import CreateAccountOperation, ReadAccountOperation, ReadAccountOperations, UpdateAccountOperation
from ..services.DAO import AccountOperationDAO

router = APIRouter()
DAO = AccountOperationDAO()


@router.post("/", response_model=ReadAccountOperation, status_code=201)
async def create_account_operation(account_operation: CreateAccountOperation,
                                   session: AsyncSession = Depends(get_session)) -> ReadAccountOperation:
    return await DAO.create(session=session, obj_in=account_operation)


@router.get("/", response_model=ReadAccountOperations)
async def get_account_operations(limit: int = 100, offset: int = 0, session: AsyncSession = Depends(get_session)) -> ReadAccountOperations:
    account_operations = await DAO.list(session=session, limit=limit, offset=offset)
    return {"results": account_operations or []}


@router.get("/{account_operation_id}", response_model=ReadAccountOperation)
async def get_account_operation(account_operation_id: UUID, session: AsyncSession = Depends(get_session)) -> ReadAccountOperation:
    return await DAO.get(session=session, id=account_operation_id)


@router.patch("/{customer_account_id}", response_model=ReadAccountOperation)
async def update_account_operation(account_operation_id: UUID,
                                   account_operation: UpdateAccountOperation,
                                   session: AsyncSession = Depends(get_session)) -> ReadAccountOperation:
    return await DAO.update(session=session, obj_new=account_operation, id=account_operation_id)


@router.delete("/{account_operation_id}", status_code=204)
async def delete_account_operation(account_operation_id: UUID, session: AsyncSession = Depends(get_session)) -> None:
    await DAO.delete(session=session, id=account_operation_id)
