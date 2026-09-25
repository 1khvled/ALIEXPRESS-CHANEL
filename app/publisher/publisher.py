from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional, Tuple
import httpx
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.settings import settings
from app.db.models import TelegramPost, Deal
from app.utils.logger import logger, record_system_log

class TelegramPublisher:
    def __init__(
        self,
        bot_token: Optional[str] = None,
        target_channel: Optional[str] = None
    ):
        self.bot_token = bot_token or settings.TELEGRAM_BOT_TOKEN
        self.target_channel = target_channel or settings.TARGET_CHANNEL_ID

    async def can_publish(self, session: AsyncSession) -> Tuple[bool, Optional[str]]:
        """
        Enforces cooldown and rate limits:
        - Max posts per hour
        - Max posts per day
        - Minimum cooldown between consecutive posts
        """
        now = datetime.now(timezone.utc)

        # 1. Cooldown since last published post
        cooldown_cutoff = now - timedelta(minutes=settings.COOLDOWN_MINUTES)
        last_post_query = select(TelegramPost).where(
            and_(
                TelegramPost.status == "PUBLISHED",
                TelegramPost.published_at >= cooldown_cutoff
            )
        ).order_by(TelegramPost.published_at.desc()).limit(1)
        res = await session.execute(last_post_query)
        last_post = res.scalar_one_or_none()
        if last_post:
            return False, f"Cooldown active: last post published at {last_post.published_at.isoformat()}"

        # 2. Hourly limit
        hour_cutoff = now - timedelta(hours=1)
        hourly_query = select(func.count(TelegramPost.id)).where(
            and_(
                TelegramPost.status == "PUBLISHED",
                TelegramPost.published_at >= hour_cutoff
            )
        )
        hourly_count = (await session.execute(hourly_query)).scalar() or 0
        if hourly_count >= settings.MAX_POSTS_PER_HOUR:
            return False, f"Hourly limit reached: {hourly_count}/{settings.MAX_POSTS_PER_HOUR}"

        # 3. Daily limit
        day_cutoff = now - timedelta(days=1)
        daily_query = select(func.count(TelegramPost.id)).where(
            and_(
                TelegramPost.status == "PUBLISHED",
                TelegramPost.published_at >= day_cutoff
            )
        )
        daily_count = (await session.execute(daily_query)).scalar() or 0
        if daily_count >= settings.MAX_POSTS_PER_DAY:
            return False, f"Daily limit reached: {daily_count}/{settings.MAX_POSTS_PER_DAY}"

        return True, None

    async def publish_deal(
        self,
        session: AsyncSession,
        deal: Deal,
        caption: str,
        image_path: Optional[Path] = None,
        force: bool = False
    ) -> Tuple[bool, Optional[str]]:
        """
        Publishes deal post to the target Telegram channel.
        Handles DRY_RUN, APPROVAL, and AUTO modes.
        """
        mode = settings.PUBLISH_MODE.lower()

        # DRY RUN MODE
        if mode == "dry_run":
            post_record = TelegramPost(
                deal_id=deal.id,
                channel_id=self.target_channel or "DRY_RUN",
                status="DRY_RUN",
                published_at=datetime.now(timezone.utc),
                permalink="https://t.me/dry_run_preview"
            )
            session.add(post_record)
            deal.status = "PUBLISHED"
            await session.commit()
            await record_system_log("INFO", "publisher", f"[DRY RUN] Would publish deal #{deal.id}: {deal.title}")
            return True, None

        # Check rate limits unless force is set
        if not force:
            can_send, reason = await self.can_publish(session)
            if not can_send:
                logger.warning(f"Publish delayed for deal #{deal.id}: {reason}")
                return False, reason

        if not self.bot_token or not self.target_channel:
            err = "TELEGRAM_BOT_TOKEN or TARGET_CHANNEL_ID not configured in settings"
            logger.error(err)
            return False, err

        # Send via Telegram Bot API
        api_url = f"https://api.telegram.org/bot{self.bot_token}"
        try:
            # Inline keyboard for direct purchase + coin discount bot
            import json
            inline_keyboard = []
            if deal.affiliate_url and deal.affiliate_url.startswith("http"):
                btn_title = "🎟️ صفحة الكوبونات والتخفيضات" if getattr(deal, "quality_score", 0) == 95 and "كود" in caption else "🛒 رابط الشراء من AliExpress"
                inline_keyboard.append([{"text": btn_title, "url": deal.affiliate_url}])
            inline_keyboard.append([{"text": "🪙 بوت تخفيض العملات DealScoutDz", "url": "https://t.me/Alilo07BOT"}])
            reply_markup_json = json.dumps({"inline_keyboard": inline_keyboard})

            async with httpx.AsyncClient(timeout=30.0) as client:
                if image_path and image_path.exists():
                    # Send photo with caption
                    with open(image_path, "rb") as photo_file:
                        files = {"photo": photo_file}
                        data = {
                            "chat_id": self.target_channel,
                            "caption": caption,
                            "parse_mode": "HTML",
                            "reply_markup": reply_markup_json
                        }
                        resp = await client.post(f"{api_url}/sendPhoto", data=data, files=files)
                else:
                    # Send text message
                    data = {
                        "chat_id": self.target_channel,
                        "text": caption,
                        "parse_mode": "HTML",
                        "reply_markup": reply_markup_json
                    }
                    resp = await client.post(f"{api_url}/sendMessage", data=data)

                result = resp.json()

                if resp.status_code == 200 and result.get("ok"):
                    msg_data = result.get("result", {})
                    msg_id = msg_data.get("message_id")
                    channel_username = str(self.target_channel).lstrip("@")
                    permalink = f"https://t.me/{channel_username}/{msg_id}" if not channel_username.startswith("-") else None

                    post_record = TelegramPost(
                        deal_id=deal.id,
                        telegram_message_id=msg_id,
                        channel_id=str(self.target_channel),
                        status="PUBLISHED",
                        published_at=datetime.now(timezone.utc),
                        permalink=permalink
                    )
                    session.add(post_record)
                    deal.status = "PUBLISHED"
                    await session.commit()

                    await record_system_log(
                        "INFO",
                        "publisher",
                        f"Published deal #{deal.id} to Telegram channel {self.target_channel} (msg #{msg_id})"
                    )
                    return True, None
                else:
                    err_msg = result.get("description", f"HTTP {resp.status_code}")
                    deal.status = "FAILED"
                    deal.rejection_reason = err_msg
                    post_record = TelegramPost(
                        deal_id=deal.id,
                        channel_id=str(self.target_channel),
                        status="FAILED",
                        error_message=err_msg
                    )
                    session.add(post_record)
                    await session.commit()
                    await record_system_log("ERROR", "publisher", f"Failed to publish deal #{deal.id}: {err_msg}")
                    return False, err_msg

        except Exception as e:
            err_msg = str(e)
            logger.exception(f"Exception publishing deal #{deal.id}: {err_msg}")
            deal.status = "FAILED"
            deal.rejection_reason = err_msg
            await session.commit()
            return False, err_msg

telegram_publisher = TelegramPublisher()
