"""
Autonomous Deal Scout Engine
Runs continuously and autonomously without manual intervention:
1. Scrapes monitored deal channels every cycle.
2. Rejects stale/expired promotions and expired date mentions.
3. Strictly filters categories: Gaming, Smartwatches, Phones, Tablets ONLY.
4. Enforces official AliExpress CDN studio photos (never competitor watermarks).
5. Detects official promo code bulletins and scrapes official AliExpress promo banners.
6. Generates affiliate links and attaches @Alilo07BOT CTA and inline buttons.
7. Enforces posting cooldowns and hourly/daily rate limits to maintain high channel quality.
"""
import asyncio
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Set, Optional

import httpx
from bs4 import BeautifulSoup
from sqlalchemy import select

from app.config.settings import settings
from app.db.session import init_db, db_context
from app.db.models import Channel, SourceMessage, Deal, GeneratedPost
from app.aliexpress.product import product_extractor
from app.aliexpress.parser import is_spam_or_non_deal, is_allowed_category
from app.aliexpress.promos import promo_tracker
from app.aliexpress.affiliate import affiliate_service
from app.ai.generator import caption_generator
from app.media.downloader import media_downloader
from app.media.renderer import media_renderer
from app.publisher.publisher import telegram_publisher
from app.utils.logger import logger, record_system_log

MONITORED_CHANNELS = [
    "Pcgamingpart",
    "zedstoreonline",
    "aniscoupons",
    "ECKSDEAL",
    "lodydeals",
    "BNDDEALS"
]

class AutonomousEngine:
    def __init__(self, cycle_interval_seconds: int = 180):
        self.interval = cycle_interval_seconds
        self.is_running = False
        self.seen_products: Set[str] = set()
        self.seen_message_urls: Set[str] = set()

    async def initialize(self):
        """Pre-loads existing published deals from DB to prevent duplicates."""
        await init_db()
        async with db_context() as s:
            existing_pids = (await s.execute(
                select(Deal.product_id).where(Deal.status == "PUBLISHED")
            )).scalars().all()
            for pid in existing_pids:
                if pid:
                    self.seen_products.add(pid)

            existing_msgs = (await s.execute(
                select(SourceMessage.message_url)
            )).scalars().all()
            for murl in existing_msgs:
                if murl:
                    self.seen_message_urls.add(murl)

        logger.info(f"Autonomous Engine initialized. Loaded {len(self.seen_products)} published deals for deduplication.")

    async def scan_channel(self, client: httpx.AsyncClient, channel_username: str) -> int:
        """
        Scans a single channel for fresh deals, validates them, and publishes
        the best candidates if cooldown allows.
        """
        url = f"https://t.me/s/{channel_username}"
        try:
            resp = await client.get(url, timeout=15.0)
            if resp.status_code != 200:
                logger.warning(f"Autonomous scan got HTTP {resp.status_code} for @{channel_username}")
                return 0

            soup = BeautifulSoup(resp.text, "html.parser")
            blocks = soup.find_all("div", class_="tgme_widget_message")
            if not blocks:
                return 0

            new_published = 0

            # Scan newest messages first
            for block in reversed(blocks):
                text_div = block.find("div", class_="tgme_widget_message_text")
                if not text_div:
                    continue

                raw_text = text_div.get_text(separator="\n").strip()

                # Extract message URL / ID
                data_post = block.get("data-post", "")
                msg_url = f"https://t.me/{data_post}" if data_post else ""
                if msg_url and msg_url in self.seen_message_urls:
                    continue

                # 1. Freshness check: reject messages older than 24h
                time_el = block.find("time")
                msg_dt = None
                if time_el and time_el.get("datetime"):
                    try:
                        msg_dt = datetime.fromisoformat(time_el["datetime"].replace("Z", "+00:00"))
                    except Exception:
                        pass

                is_fresh, freshness_reason = promo_tracker.validate_deal_freshness(raw_text, msg_dt)
                if not is_fresh:
                    logger.debug(f"[@{channel_username}] Freshness check failed: {freshness_reason}")
                    if msg_url:
                        self.seen_message_urls.add(msg_url)
                    continue

                # 2. Spam filter
                is_spam, _ = is_spam_or_non_deal(raw_text)
                if is_spam:
                    if msg_url:
                        self.seen_message_urls.add(msg_url)
                    continue

                # 3. Extract deal / coupon list
                extracted = await product_extractor.extract_from_message(raw_text)
                if not extracted or not extracted.is_valid:
                    if msg_url:
                        self.seen_message_urls.add(msg_url)
                    continue

                # 4. Strict category filter (Gaming, Watches, Phones, Tablets only; Coupon bulletin exempt)
                if not extracted.is_coupon_list:
                    allowed, reject_reason = is_allowed_category(extracted.title or "", raw_text)
                    if not allowed:
                        logger.debug(f"[@{channel_username}] Category rejected: {reject_reason}")
                        if msg_url:
                            self.seen_message_urls.add(msg_url)
                        continue

                # 5. Deduplication
                if extracted.product_id in self.seen_products:
                    if msg_url:
                        self.seen_message_urls.add(msg_url)
                    continue

                # 6. Studio photo / promo banner verification
                img_url = extracted.image_url
                if not extracted.is_coupon_list:
                    # Single product: MUST be official AliExpress CDN studio photo
                    if not img_url or not any(d in img_url for d in ["alicdn.com", "aliexpress-media.com", "aliexpress.com"]):
                        logger.debug(f"[@{channel_username}] Rejected deal lacking official AliExpress CDN image: {extracted.product_id}")
                        continue
                else:
                    # Coupon bulletin: if no banner scraped, fetch official AliExpress campaign banner
                    if not img_url:
                        img_url = await promo_tracker.scrape_aliexpress_promo_banner(extracted.canonical_url or extracted.original_url)

                # 7. Check if rate-limits / cooldown allow publishing now
                async with db_context() as s:
                    can_publish, delay_reason = await telegram_publisher.can_publish(s)
                    if not can_publish:
                        logger.info(f"Autonomous engine queued deal (cooldown active: {delay_reason})")
                        # Do not mark as seen so it can be published when cooldown clears
                        return new_published

                # 8. Build affiliate link
                aff_link = await affiliate_service.create_affiliate_link(
                    product_url=extracted.canonical_url,
                    product_id=extracted.product_id if not extracted.is_coupon_list else None
                )

                # 9. Generate caption with promo header + @Alilo07BOT CTA
                promo_tag = promo_tracker.get_promo_header()
                caption = await caption_generator.generate(
                    title=extracted.title or "AliExpress Deal",
                    usd_price=extracted.current_price,
                    eur_price=extracted.current_price_eur,
                    affiliate_url=aff_link,
                    coupon_code=extracted.coupon_code,
                    has_points_discount=extracted.has_points_discount,
                    country_info=extracted.country_info,
                    coupon_list=extracted.coupon_list if extracted.is_coupon_list else None,
                    promo_tag=promo_tag
                )

                # 10. Prepare Image with DealScout branding
                local_img_file = None
                if img_url:
                    downloaded = await media_downloader.download_image(img_url, extracted.product_id)
                    if downloaded:
                        local_img_file = media_renderer.prepare_post_image(
                            downloaded,
                            extracted.product_id,
                            extracted.title,
                            usd_price=extracted.current_price
                        )

                if not local_img_file and not extracted.is_coupon_list:
                    continue

                # 11. Save record and publish to channel
                async with db_context() as s:
                    ch_record = (await s.execute(
                        select(Channel).where(Channel.username == channel_username)
                    )).scalar_one_or_none()
                    ch_id = ch_record.id if ch_record else 1
                    msg_id_num = int(data_post.split("/")[-1]) if "/" in data_post and data_post.split("/")[-1].isdigit() else 900000

                    src = SourceMessage(
                        channel_id=ch_id,
                        telegram_message_id=msg_id_num,
                        message_url=msg_url or f"https://t.me/{channel_username}/{msg_id_num}",
                        raw_text=raw_text
                    )
                    s.add(src)
                    await s.flush()

                    deal = Deal(
                        source_message_id=src.id,
                        product_id=extracted.product_id,
                        original_url=extracted.original_url,
                        normalized_url=extracted.canonical_url,
                        affiliate_url=aff_link,
                        title=extracted.title,
                        currency="USD",
                        current_price=extracted.current_price,
                        current_price_eur=extracted.current_price_eur,
                        coupon_code=extracted.coupon_code,
                        has_points_discount=extracted.has_points_discount,
                        image_url=img_url,
                        local_image_path=str(local_img_file) if local_img_file else None,
                        quality_score=95 if extracted.is_coupon_list else 90,
                        status="PUBLISHED"
                    )
                    s.add(deal)
                    await s.flush()

                    gen_post = GeneratedPost(
                        deal_id=deal.id,
                        title=deal.title,
                        caption=caption,
                        image_path=str(local_img_file) if local_img_file else None,
                        ai_model="autonomous_clean_v1",
                        ai_validation_status="APPROVED",
                        status="VALIDATED"
                    )
                    s.add(gen_post)
                    await s.commit()

                    # Publish with inline buttons
                    success, err = await telegram_publisher.publish_deal(
                        session=s,
                        deal=deal,
                        caption=caption,
                        image_path=local_img_file,
                        force=False
                    )

                    if success:
                        self.seen_products.add(extracted.product_id)
                        if msg_url:
                            self.seen_message_urls.add(msg_url)
                        new_published += 1
                        logger.info(f"Autonomous published deal #{deal.id}: {deal.title} (${deal.current_price})")
                        await record_system_log(
                            "INFO",
                            "autonomous",
                            f"Published: {deal.title} (${deal.current_price}) from @{channel_username}"
                        )
                        # Yield after publishing to respect channel cooldown
                        return new_published
                    else:
                        logger.warning(f"Autonomous publish failed: {err}")

            return new_published

        except Exception as e:
            logger.error(f"Error scanning channel @{channel_username}: {e}")
            return 0

    async def run_single_cycle(self) -> int:
        """Executes one scan cycle across all monitored channels."""
        total_new = 0
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            for ch in MONITORED_CHANNELS:
                try:
                    count = await self.scan_channel(client, ch)
                    total_new += count
                    if count > 0:
                        # Once a deal is posted, stop current cycle to let channel cooldown elapse
                        break
                except Exception as e:
                    logger.error(f"Scan error on @{ch}: {e}")
        return total_new

    async def run_forever(self):
        """Continuous autonomous loop running 24/7."""
        self.is_running = True
        logger.info("=" * 60)
        logger.info("AUTONOMOUS DEAL SCOUT ENGINE STARTED (24/7 OPERATION)")
        logger.info(f"Target: {settings.TARGET_CHANNEL_ID} | Tracking: {settings.ALIEXPRESS_AFFILIATE_TRACKING_ID}")
        logger.info(f"Interval: {self.interval}s | Channels: {', '.join(MONITORED_CHANNELS)}")
        logger.info("=" * 60)

        await self.initialize()

        while self.is_running:
            try:
                published = await self.run_single_cycle()
                if published > 0:
                    logger.info(f"Cycle completed. {published} deal(s) published.")
            except Exception as e:
                logger.exception(f"Unhandled error in autonomous engine cycle: {e}")

            await asyncio.sleep(self.interval)

    def stop(self):
        self.is_running = False
        logger.info("Autonomous Deal Scout Engine stopping...")

autonomous_engine = AutonomousEngine()
