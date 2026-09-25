from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from app.config.settings import settings
from app.db.models import Channel, SourceMessage
from app.db.session import db_context
from app.telegram.client import telegram_client_manager
from app.deals.processor import deal_processor
from app.utils.logger import logger, record_system_log

class TelegramCollector:
    def __init__(self):
        self.client_manager = telegram_client_manager
        self.downloads_dir = settings.DOWNLOADS_DIR

    async def collect_all_channels(self) -> int:
        """
        Executes a 180-second collection cycle across all enabled channels.
        Returns total new messages processed.
        """
        client = self.client_manager.get_client()
        if not client or not client.is_connected():
            is_connected = await self.client_manager.connect()
            if not is_connected:
                logger.info("Collector skipped: Telethon client is not connected/authorized.")
                return 0

        total_collected = 0

        async with db_context() as session:
            # Query enabled channels ordered by priority
            q = select(Channel).where(Channel.enabled == True).order_by(Channel.priority.desc())
            channels = (await session.execute(q)).scalars().all()

            if not channels:
                logger.debug("No enabled channels configured for collection.")
                return 0

            for channel in channels:
                try:
                    count = await self._collect_channel(session, client, channel)
                    total_collected += count
                except Exception as e:
                    logger.error(f"Error collecting channel @{channel.username}: {e}")
                    await record_system_log("ERROR", "collector", f"Failed checking @{channel.username}: {e}")

        return total_collected

    async def _collect_channel(self, session: AsyncSession, client, channel: Channel) -> int:
        """Collects new messages from a single channel since channel.last_message_id."""
        username = channel.username.strip().lstrip("@")
        min_id = channel.last_message_id or 0
        new_count = 0
        max_seen_id = min_id

        try:
            entity = await client.get_entity(username)
            if hasattr(entity, "id") and not channel.telegram_channel_id:
                channel.telegram_channel_id = entity.id

            # Fetch messages newer than last_message_id (limit 25 per cycle)
            messages = await client.get_messages(
                entity,
                limit=25,
                min_id=min_id,
                reverse=True  # oldest first to process chronologically
            )

            for msg in messages:
                if not msg.id or msg.id <= min_id:
                    continue

                if msg.id > max_seen_id:
                    max_seen_id = msg.id

                # Deduplicate by (channel_id, telegram_message_id)
                check_q = select(SourceMessage).where(
                    and_(
                        SourceMessage.channel_id == channel.id,
                        SourceMessage.telegram_message_id == msg.id
                    )
                )
                existing = (await session.execute(check_q)).scalar_one_or_none()
                if existing:
                    continue

                # Media handling
                media_type = "none"
                media_path = None
                if isinstance(msg.media, MessageMediaPhoto):
                    media_type = "photo"
                    try:
                        saved_path = await msg.download_media(file=str(self.downloads_dir / f"src_{channel.id}_{msg.id}.jpg"))
                        media_path = str(saved_path) if saved_path else None
                    except Exception as e:
                        logger.debug(f"Media download failed for msg {msg.id}: {e}")
                elif isinstance(msg.media, MessageMediaDocument):
                    media_type = "document"

                pub_date = msg.date.astimezone(timezone.utc) if msg.date else datetime.now(timezone.utc)
                msg_url = f"https://t.me/{username}/{msg.id}"

                source_msg = SourceMessage(
                    channel_id=channel.id,
                    telegram_message_id=msg.id,
                    message_url=msg_url,
                    raw_text=msg.text or msg.message or "",
                    media_type=media_type,
                    media_path=media_path,
                    published_at=pub_date
                )
                session.add(source_msg)
                await session.flush()

                new_count += 1

                # Send directly to deal processor
                await deal_processor.process_source_message(session, source_msg)

            # Update channel cursor
            channel.last_message_id = max_seen_id
            channel.last_checked_at = datetime.now(timezone.utc)
            await session.commit()

            if new_count > 0:
                await record_system_log(
                    "INFO",
                    "collector",
                    f"Channel @{username}: processed {new_count} new messages (cursor: {max_seen_id})"
                )

        except Exception as e:
            logger.error(f"Failed to collect messages for @{username}: {e}")
            raise e

        return new_count

telegram_collector = TelegramCollector()
