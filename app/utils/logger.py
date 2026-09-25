import logging
import sys
from typing import Optional
from app.config.settings import settings

# Setup standard python logging
log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
logging.basicConfig(
    level=log_level,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("aliexpress_deals")

async def record_system_log(level: str, component: str, message: str, details: Optional[str] = None):
    """
    Saves a log record to the database system_logs table and outputs to standard logger.
    """
    # Print to console
    log_func = getattr(logger, level.lower(), logger.info)
    detail_str = f" | {details}" if details else ""
    log_func(f"{component}: {message}{detail_str}")

    try:
        from app.db.session import db_context
        from app.db.models import SystemLog
        async with db_context() as session:
            log_entry = SystemLog(
                level=level.upper(),
                component=component,
                message=message,
                details=details
            )
            session.add(log_entry)
            await session.commit()
    except Exception as e:
        # Don't fail the caller if DB logging encounters an issue
        logger.warning(f"Failed to persist log to DB: {e}")
