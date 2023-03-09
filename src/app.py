from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from .middlewares import ErrorMiddleware
from .routers import api_router
from .settings import get_settings
from .utils import setup_logger

settings = get_settings()

app_config = {
    "title": "Accountant",
    "version": "1.0.0",
    "description": "API для мaнипyляции c 6aлaнcoм клиeнтa",

}

if settings.ENVIRONMENT not in settings.SHOW_DOCS_ENVIRONMENT:
    app_config["openapi_url"] = None


app = FastAPI(**app_config)


@app.on_event("startup")
async def on_startup() -> None:
    setup_logger()


app.start_time = datetime.now(tz=timezone.utc)

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



