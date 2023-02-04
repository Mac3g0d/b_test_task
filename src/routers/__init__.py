from fastapi import APIRouter
from .misc import router as misc_router
from .customer import router as customer_router
from .currency import router as currency_router
from .customer_account import router as customer_account_router
from .account_operation import router as account_operation_router

api_router = APIRouter(prefix='/api/v1')

api_router.include_router(misc_router, prefix='', tags=['misc'])
api_router.include_router(customer_router, prefix='/customers', tags=['customers'])
api_router.include_router(currency_router, prefix='/currencies', tags=['currencies'])
api_router.include_router(customer_account_router, prefix='/customer_accounts', tags=['customer_accounts'])
api_router.include_router(account_operation_router, prefix='/account_operations', tags=['account_operations'])



