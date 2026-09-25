import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.config.settings import settings
from app.telegram.collector import telegram_collector
from app.utils.logger import logger, record_system_log

scheduler = AsyncIOScheduler()

async def monitor_cycle():
    """Scheduled task executing the 3-minute channel monitoring cycle."""
    try:
        logger.info("Starting 3-minute Telegram collection cycle...")
        collected = await telegram_collector.collect_all_channels()
        logger.info(f"Collection cycle finished. New messages processed: {collected}")
    except Exception as e:
        logger.exception(f"Unhandled error in monitor cycle: {e}")
        await record_system_log("ERROR", "scheduler", f"Monitor cycle failed: {e}")

def start_scheduler():
    """Initializes and starts the APScheduler background monitor."""
    interval = settings.POLL_INTERVAL_SECONDS or 180
    scheduler.add_job(
        monitor_cycle,
        "interval",
        seconds=interval,
        max_instances=1,
        coalesce=True,
        id="telegram_channel_monitor"
    )
    scheduler.start()
    logger.info(f"Scheduler active: checking 10 channels every {interval}s.")

def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Scheduler stopped.")
