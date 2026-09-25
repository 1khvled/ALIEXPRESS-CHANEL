import asyncio
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.db.session import init_db
from app.main import bootstrap_channels
from app.utils.logger import logger

async def main():
    logger.info("Initializing database schema...")
    await init_db()
    logger.info("Bootstrapping channels...")
    await bootstrap_channels()
    logger.info("Database initialization complete.")

if __name__ == "__main__":
    asyncio.run(main())
