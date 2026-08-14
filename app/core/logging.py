import logging
import sys

from app.core.config import get_settings


def configure_logging() -> None:
    settings = get_settings()
    level = logging.INFO if settings.environment == "production" else logging.DEBUG
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        stream=sys.stdout,
    )
