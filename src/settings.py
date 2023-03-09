import uuid
from functools import lru_cache

from pydantic import BaseSettings, Field, SecretStr, validator


class Settings(BaseSettings):
    SESSION_SECRET_KEY: str = Field(default=str(uuid.uuid4()))
    CORS_ORIGINS: str = "*"
    ENVIRONMENT: str
    SHOW_DOCS_ENVIRONMENT: set[str] = ("dev", "stage", "test", "demo")

    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str

    DATABASE_URI: str | None

    DB_POOL_SIZE = 83
    WEB_CONCURRENCY = 9
    POOL_SIZE = max(DB_POOL_SIZE // WEB_CONCURRENCY, 5)

    @validator("DATABASE_URI", pre=True)
    def validate_postgres_uri(cls, v, values) -> str: # noqa
        if isinstance(v, str):
            return v

        password: SecretStr = values.get("POSTGRES_PASSWORD", SecretStr(""))
        return f'postgresql+asyncpg://{values.get("POSTGRES_USER")}:{password.get_secret_value()}' \
               f'@{values.get("POSTGRES_HOST")}:{values.get("POSTGRES_PORT")}/{values.get("POSTGRES_DB")}'

    class Config:
        env_file = "src/.env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
