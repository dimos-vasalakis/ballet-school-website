import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    secret_key: str
    app_title: str = "T.PARADISE Ballet School"
    environment: str = "development"
    database_url: str = "postgresql+asyncpg://ballet:ballet@localhost:5432/ballet"


class ConfigError(RuntimeError):
    """Raised when required configuration is missing or invalid."""


@lru_cache
def get_settings() -> Settings:
    load_dotenv()
    secret_key = os.environ.get("SECRET_KEY")
    if not secret_key:
        raise ConfigError(
            "Missing SECRET_KEY.\n"
            "Set it in your .env file (see .env.example) before starting the app.\n"
            "Example: SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')"
        )
    environment = os.environ.get("ENVIRONMENT", "development")
    database_url = os.environ.get("DATABASE_URL") or Settings.database_url
    return Settings(secret_key=secret_key, environment=environment, database_url=database_url)
