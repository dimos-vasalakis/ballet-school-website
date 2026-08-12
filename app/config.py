import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    secret_key: str
    app_title: str = "T.PARADISE Ballet School"


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
    return Settings(secret_key=secret_key)
