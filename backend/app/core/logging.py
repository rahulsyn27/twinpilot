import logging
import sys

import structlog
from rich.logging import RichHandler

from app.core.config import settings


def configure_logging() -> None:
    """
    Configure application logging.

    Uses:
    - Rich for beautiful console logs.
    - Structlog for structured logging.
    """

    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format="%(message)s",
        handlers=[
            RichHandler(
                rich_tracebacks=True,
                show_path=False,
                markup=True,
            )
        ],
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.getLevelName(settings.LOG_LEVEL)
        ),
        logger_factory=structlog.PrintLoggerFactory(
            file=sys.stdout
        ),
        cache_logger_on_first_use=True,
    )


logger = structlog.get_logger("twinpilot")