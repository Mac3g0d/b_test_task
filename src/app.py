from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
# from sqladmin import Admin


from .middlewares import ErrorMiddleware
from .routers import api_router
from .settings import get_settings
from .utils import setup_logger
# from admin_views import CustomerAdmin, CurrencyAdmin, CustomerAccountAdmin, AccountOperationAdmin

settings = get_settings()

app_config = {
    "title": "Accountant",
    "version": "1.0.0",
    "description": "API для манипуляции с балансом клиента",

}

if settings.ENVIRONMENT not in settings.SHOW_DOCS_ENVIRONMENT:
    app_config["openapi_url"] = None


app = FastAPI(**app_config)

# if settings.ENVIRONMENT in settings.SHOW_DOCS_ENVIRONMENT:
#     admin = Admin(app, engine, title="Админ панель")
#     admin.add_view(CustomerAdmin)
#     admin.add_view(CurrencyAdmin)
#     admin.add_view(CustomerAccountAdmin)
#     admin.add_view(AccountOperationAdmin)


@app.on_event("startup")
async def on_startup():

    # await init_db()
    setup_logger()


app.start_time = datetime.now()

app.include_router(api_router)

app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)
app.add_middleware(ErrorMiddleware)



