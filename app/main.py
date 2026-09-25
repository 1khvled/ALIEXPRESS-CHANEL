import os
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import yaml
from sqlalchemy import select

from app.config.settings import settings
from app.db.session import init_db, db_context
from app.db.models import Channel
from app.api.routes import api_router
from app.api.dashboard import dashboard_router
from app.jobs.monitor import start_scheduler, stop_scheduler
from app.telegram.client import telegram_client_manager
from app.utils.logger import logger, record_system_log

async def bootstrap_channels():
    """Seeds the 10 source channels from channels.yaml if not already present."""
    yaml_path = settings.BASE_DIR / "app" / "config" / "channels.yaml"
    if not yaml_path.exists():
        return

    try:
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            channels_data = data.get("channels", [])

        async with db_context() as session:
            active_usernames = []
            for item in channels_data:
                username = item.get("username", "").strip().lstrip("@")
                if not username:
                    continue
                active_usernames.append(username)

                existing = (await session.execute(
                    select(Channel).where(Channel.username == username)
                )).scalar_one_or_none()

                if not existing:
                    ch = Channel(
                        username=username,
                        display_name=item.get("name", username),
                        enabled=item.get("enabled", True),
                        priority=item.get("priority", 50),
                        last_message_id=0
                    )
                    session.add(ch)
                else:
                    existing.enabled = item.get("enabled", True)
                    existing.display_name = item.get("name", existing.display_name)
                    existing.priority = item.get("priority", existing.priority)

            # Disable any channel not in channels.yaml
            all_channels = (await session.execute(select(Channel))).scalars().all()
            for ch in all_channels:
                if ch.username not in active_usernames:
                    ch.enabled = False

            await session.commit()
            logger.info("Channels synchronized from configuration.")
    except Exception as e:
        logger.error(f"Error bootstrapping channels: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Initializing database...")
    await init_db()
    await bootstrap_channels()

    logger.info(f"AliExpress Telegram Deals system starting in [{settings.PUBLISH_MODE.upper()}] mode.")
    await record_system_log("INFO", "system", f"Application started in {settings.PUBLISH_MODE} mode")

    # Start background 180s scheduler
    start_scheduler()

    yield

    # Shutdown
    logger.info("Shutting down background scheduler...")
    stop_scheduler()
    await telegram_client_manager.disconnect()
    logger.info("Application stopped.")

app = FastAPI(
    title="AliExpress Deals to Telegram Channel Automation",
    description="Automates scraping 10 Telegram deal channels, converting to affiliate links, and publishing to our Telegram channel.",
    version="1.0.0",
    lifespan=lifespan
)

# Mount Routers
app.include_router(dashboard_router)
app.include_router(api_router)

# Mount static storage if present
if settings.STORAGE_DIR.exists():
    app.mount("/storage", StaticFiles(directory=str(settings.STORAGE_DIR)), name="storage")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
