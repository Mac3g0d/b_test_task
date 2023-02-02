from fastapi import APIRouter
from .misc import router as misc_router

api_router = APIRouter()

api_router.include_router(misc_router, prefix='', tags=['misc'])

