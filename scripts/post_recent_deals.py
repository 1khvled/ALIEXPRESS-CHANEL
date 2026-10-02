import asyncio
import os
import re
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Ensure utf-8 output on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from app.utils.network import enforce_ipv4
enforce_ipv4()

from datetime import datetime, timezone
import httpx
from bs4 import BeautifulSoup
from sqlalchemy import select, desc

from app.config.settings import settings
from app.db.session import init_db, db_context
from app.db.models import Channel, SourceMessage, Deal, GeneratedPost, TelegramPost
from app.aliexpress.product import product_extractor
from app.aliexpress.parser import is_spam_or_non_deal, is_allowed_category, detect_deal_type, is_france_deal
from app.aliexpress.promos import promo_tracker
from app.aliexpress.affiliate import affiliate_service
from app.ai.generator import caption_generator
from app.media.downloader import media_downloader
from app.media.renderer import media_renderer
from app.publisher.publisher import telegram_publisher
from app.utils.logger import logger
# Primary Algerian deal channels to mimic (Lody, Zedstore, Esk Deals, BND Deals)
CHANNELS = [
    "lodydeals",
    "zedstoreonline",
    "ECKSDEAL",
    "BNDDEALS",
    "megaphonna",
    "aniscoupons",
    "Coupon4Dz"
]

async def collect_and_post_last_10_deals(force: bool = False, force_tajmi3at: bool = False) -> int:
    await init_db()

    print("=" * 70)
    print("ALIEXPRESS DEALS PUBLISHER (CLEAN BRANDS & VERIFIED AFFILIATE)")
    print(f"Target Channel: {settings.TARGET_CHANNEL_ID}")
    print(f"Affiliate Tracking ID: {settings.ALIEXPRESS_AFFILIATE_TRACKING_ID}")
    print(f"Active Channels: {', '.join(CHANNELS)}")
    print("=" * 70)

    # Automated Check: Promo Calendar & Next Promo Transitions
    try:
        from app.publisher.promo_calendar import check_and_auto_post_promo_transitions
        p_success, p_msg = await check_and_auto_post_promo_transitions()
        if p_success:
            print(f"[PROMO CALENDAR AUTO-POST] {p_msg}")
    except Exception as e:
        print(f"[!] Promo calendar check error: {e}")

    # Automated Check: 14-day Region Disclaimer Pinning
    try:
        from app.publisher.region_disclaimer import check_and_auto_post_disclaimer
        d_success, d_msg = await check_and_auto_post_disclaimer()
        if d_success:
            print(f"[REGION DISCLAIMER AUTO-POST] {d_msg}")
    except Exception as e:
        print(f"[!] Region disclaimer check error: {e}")

    # Automated Check: Promo Era Alerts (1-day before end & 1-day before start)
    try:
        from app.publisher.promo_notifiers import check_and_auto_post_promo_notifiers
        alerts = await check_and_auto_post_promo_notifiers()
        for alert in alerts:
            print(f"[PROMO ALERT AUTO-POST] {alert.get('type')}: {alert.get('promo')} (Msg ID: {alert.get('message_id')})")
    except Exception as e:
        print(f"[!] Promo alert check error: {e}")

    # Automated Check: Rotating Coin & PC Educational Reminders (48-72h randomized interval)
    try:
        from app.publisher.bot_ad import post_bot_advertisement
        c_success, c_msg = await post_bot_advertisement(force=False)
        if c_success:
            print(f"[COIN REMINDER AUTO-POST] {c_msg}")
    except Exception as e:
        print(f"[!] Coin reminder check error: {e}")

    # Automated Check: Religious & Spiritual Reminders (Jumu'ah & Fajr Salah)
    try:
        from app.publisher.religious_reminders import check_and_auto_post_religious_reminders
        rel_results = await check_and_auto_post_religious_reminders(force=False)
        for r in rel_results:
            if r.get("success"):
                print(f"[RELIGIOUS REMINDER AUTO-POST] Posted {r.get('type')} reminder to channel (Msg ID: {r.get('message_id')})")
    except Exception as e:
        print(f"[!] Religious reminder check error: {e}")

    # Automated Check: Expired Deals / Dead Links Auto-Updater (Checks last 24h posts in @DzAliexpress0)
    try:
        from app.publisher.state_tracker import check_and_update_expired_deals
        expired_count = await check_and_update_expired_deals()
        if expired_count > 0:
            print(f"[EXPIRED DEALS UPDATER] Edited {expired_count} dead/out-of-stock post(s) in channel with 'انتهى العرض'.")
    except Exception as e:
        print(f"[!] Expired deals updater check error: {e}")

    # Dynamic Interval & Day/Night Schedule Check (Controlled via Admin Bot & Dashboard)
    from app.publisher.state_tracker import is_deal_posting_due, record_deal_posted_time, is_algerian_peak_hour
    is_due, schedule_msg, active_interval = is_deal_posting_due()
    print(f"\n[SCHEDULE EVALUATION] {schedule_msg}")
    if not is_due and not force:
        print(f"--> Skipping deal collection this run. ({schedule_msg})")
        return 0

    # Anti-Flood Pacer & Traffic Evaluation (Peak hours: 12-14 and 18-23:30 Algeria time)
    is_peak = is_algerian_peak_hour()
    max_deals_per_channel = 6 if is_peak else 4
    MAX_DEALS_PER_RUN = 12 if is_peak else 8
    print(f"[PACER TRAFFIC STATUS] Peak Hour Boost: {'ON (Up to 6 deals/ch)' if is_peak else 'OFF (Paced 4 deals/ch)'} | Max run limit: {MAX_DEALS_PER_RUN}")

    published_deals = []
    seen_products = set()
    seen_titles = []

    from app.publisher.state_tracker import sync_deleted_channel_posts
    needs_repost_keys = await sync_deleted_channel_posts()
    if needs_repost_keys:
        print(f"[DELETED POSTS SYNC] Found {len(needs_repost_keys)} post(s) deleted from channel, ready to repost: {needs_repost_keys}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8"
    }
    from app.publisher.state_tracker import (
        get_monitored_channel_last_id,
        record_monitored_channel_last_id,
        is_post_already_published,
        record_post_published,
        record_post_handled,
        is_recent_cross_channel_duplicate,
        refresh_channel_cache,
        is_same_deal_title
    )
    await refresh_channel_cache(force=True)

    async with httpx.AsyncClient(headers=headers, timeout=20.0, follow_redirects=True) as client:
        for ch in CHANNELS:
            if len(published_deals) >= MAX_DEALS_PER_RUN:
                break

            url = f"https://t.me/s/{ch}"
            print(f"\n---> Scanning channel @{ch}...")
            try:
                resp = None
                for attempt in range(2):
                    try:
                        resp = await client.get(url)
                        if resp.status_code == 200:
                            break
                    except Exception:
                        await asyncio.sleep(1.0)

                if not resp or resp.status_code != 200:
                    print(f"  [!] HTTP {resp.status_code if resp else 'TIMEOUT'} for @{ch}")
                    continue

                soup = BeautifulSoup(resp.text, "html.parser")
                blocks = soup.find_all("div", class_="tgme_widget_message")
                print(f"  Found {len(blocks)} message blocks in @{ch}")
                
                block_items = []
                for b in blocks:
                    dp = b.get("data-post", "")
                    if "/" in dp and dp.split("/")[-1].isdigit():
                        block_items.append((int(dp.split("/")[-1]), b))

                if not block_items:
                    print(f"  No valid post IDs found in @{ch}")
                    continue

                current_max_id = max(b_id for b_id, _ in block_items)
                last_seen_id = get_monitored_channel_last_id(ch)

                if last_seen_id is None:
                    # First time seeing this channel — process ALL posts on current page
                    record_monitored_channel_last_id(ch, current_max_id)
                    new_blocks = [
                        (b_id, b) for b_id, b in block_items
                        if not is_post_already_published(ch, b_id)
                    ]
                    new_blocks.sort(key=lambda x: x[0])
                    print(f"  [FIRST RUN] @{ch} baseline set to #{current_max_id}. Processing {len(new_blocks)} visible post(s).")
                else:
                    # Process posts newer than last_seen_id, or unposted recent candidate messages from current page
                    lookback_cutoff = max(0, last_seen_id - 20)
                    new_blocks = [
                        (b_id, b) for b_id, b in block_items
                        if (b_id > last_seen_id or (b_id >= lookback_cutoff and not is_post_already_published(ch, b_id)) or f"{ch.lower()}:{b_id}" in needs_repost_keys)
                        and not is_post_already_published(ch, b_id)
                    ]
                    new_blocks.sort(key=lambda x: x[0])

                    # Pre-filter for message freshness (< 24h) and auto-mark ancient stale posts as handled
                    fresh_blocks = []
                    for b_id, b in new_blocks:
                        time_el = b.find("time")
                        msg_dt = None
                        if time_el and time_el.get("datetime"):
                            try:
                                msg_dt = datetime.fromisoformat(time_el["datetime"].replace("Z", "+00:00"))
                            except Exception:
                                pass
                        text_div = b.find("div", class_="tgme_widget_message_text")
                        raw_text = text_div.get_text(separator="\n").strip() if text_div else ""
                        is_fresh, _ = promo_tracker.validate_deal_freshness(raw_text, msg_dt)
                        if not is_fresh:
                            record_post_handled(ch, b_id)
                            continue
                        fresh_blocks.append((b_id, b))

                    if fresh_blocks:
                        repost_count = sum(1 for b_id, _ in fresh_blocks if b_id <= last_seen_id)
                        new_count = len(fresh_blocks) - repost_count
                        print(f"  [@{ch}] Found {new_count} fresh post(s) and {repost_count} unposted/repostable post(s) to process.")
                    else:
                        print(f"  [NO NEW POSTS] @{ch} has no new or fresh messages (last seen: #{last_seen_id}, current: #{current_max_id}).")
                        record_monitored_channel_last_id(ch, current_max_id)
                        continue

                # Anti-Flood Pacing: pace active fresh deals
                active_blocks = fresh_blocks if last_seen_id is not None else new_blocks
                if len(active_blocks) > max_deals_per_channel:
                    print(f"  [ANTI-FLOOD PACER] Channel @{ch} has {len(active_blocks)} fresh deals. Pacing: publishing top {max_deals_per_channel}, holding remainder for next cycle.")
                    to_process_blocks = active_blocks[:max_deals_per_channel]
                else:
                    to_process_blocks = active_blocks

                max_processed_id = last_seen_id or 0

                for msg_id, block in to_process_blocks:
                    if len(published_deals) >= MAX_DEALS_PER_RUN:
                        break

                    text_div = block.find("div", class_="tgme_widget_message_text")
                    if not text_div:
                        max_processed_id = max(max_processed_id, msg_id)
                        continue

                    # Extract source post photo if present (competitor's coupon banner)
                    source_photo_url = None
                    photo_wrap = block.find("a", class_="tgme_widget_message_photo_wrap")
                    if photo_wrap and photo_wrap.get("style"):
                        m_url = re.search(r"url\(['\"]?(https?://[^'\"]+)['\"]?\)", photo_wrap["style"])
                        if m_url:
                            source_photo_url = m_url.group(1)

                    raw_text = text_div.get_text(separator="\n").strip()

                    # 1. Parse message timestamp and enforce maximum 2h freshness
                    time_el = block.find("time")
                    msg_dt = None
                    if time_el and time_el.get("datetime"):
                        try:
                            msg_dt = datetime.fromisoformat(time_el["datetime"].replace("Z", "+00:00"))
                        except Exception:
                            pass

                    # 2. Promo calendar freshness & expired campaign check
                    is_fresh, freshness_reason = promo_tracker.validate_deal_freshness(raw_text, msg_dt)
                    if not is_fresh:
                        print(f"  [EXPIRED / STALE SKIPPED] {freshness_reason}")
                        max_processed_id = max(max_processed_id, msg_id)
                        record_post_handled(ch, msg_id)
                        continue

                    # 3. Smart spam filtering
                    is_spam, spam_reason = is_spam_or_non_deal(raw_text)
                    if is_spam:
                        max_processed_id = max(max_processed_id, msg_id)
                        record_post_handled(ch, msg_id)
                        continue

                    # 4. Extract deal or coupon list (pass source_photo_url as fallback image)
                    extracted = await product_extractor.extract_from_message(raw_text, media_path=source_photo_url)
                    if not extracted or not extracted.is_valid:
                        # Automated check: Competitor channel service announcements (China holidays, customs, courier notices)
                        from app.aliexpress.parser import detect_channel_announcement
                        from app.publisher.state_tracker import is_channel_announcement_eligible, record_channel_announcement_published
                        is_ann, ann_text, ann_tag = detect_channel_announcement(raw_text)
                        if is_ann and ann_tag:
                            now_dz = datetime.now(timezone(timedelta(hours=1)))
                            today_str = now_dz.strftime("%Y-%m-%d")
                            if is_channel_announcement_eligible(ann_tag, today_str):
                                token = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("ADMIN_BOT_TOKEN")
                                if token:
                                    try:
                                        async with httpx.AsyncClient(timeout=10.0) as client:
                                            resp = await client.post(
                                                f"https://api.telegram.org/bot{token}/sendMessage",
                                                json={
                                                    "chat_id": settings.TARGET_CHANNEL_ID,
                                                    "text": ann_text,
                                                    "parse_mode": "HTML",
                                                    "disable_web_page_preview": True
                                                }
                                            )
                                            if resp.status_code == 200 and resp.json().get("ok"):
                                                record_channel_announcement_published(ann_tag, today_str)
                                                print(f"  [ANNOUNCEMENT PUBLISHED] Auto-posted '{ann_tag}' announcement to {settings.TARGET_CHANNEL_ID}")
                                    except Exception as e:
                                        print(f"  [!] Failed to publish announcement: {e}")
                        max_processed_id = max(max_processed_id, msg_id)
                        record_post_handled(ch, msg_id)
                        continue

                    # 4.5. Strictly reject France-specific deals in Algerian channel @DzAliexpress0
                    # and auto-route them cleanly to @francedealsdz!
                    if is_france_deal(raw_text, url=f"{extracted.original_url} {extracted.canonical_url}", country_info=extracted.country_info):
                        print(f"  [FRANCE DEAL ROUTER] Deal is intended for France/Europe: {extracted.product_id}. Auto-routing to @francedealsdz...")
                        try:
                            from scripts.post_france_deals import publish_extracted_deal_to_france
                            routed = await publish_extracted_deal_to_france(
                                extracted=extracted,
                                raw_text=raw_text,
                                source_photo_url=source_photo_url,
                                channel_username=ch,
                                msg_id=msg_id
                            )
                            if routed:
                                print(f"  [FRANCE ROUTER SUCCESS] Posted {extracted.product_id} to @francedealsdz!")
                        except Exception as e:
                            print(f"  [!] Failed to auto-route France deal: {e}")
                        max_processed_id = max(max_processed_id, msg_id)
                        record_monitored_channel_last_id(ch, msg_id)
                        record_post_handled(ch, msg_id)
                        continue

                    # 5. Category whitelist: ONLY gaming, watches, phones, tablets (Coupons bulletin exempt)
                    if not extracted.is_coupon_list:
                        allowed, reject_reason = is_allowed_category(
                            extracted.title or '',
                            raw_text,
                            channel_username=ch
                        )
                        if not allowed:
                            print(f"  [CATEGORY FILTERED] {reject_reason}")
                            max_processed_id = max(max_processed_id, msg_id)
                            record_post_handled(ch, msg_id)
                            continue

                    # 6. Validate by Post ID & check Cross-Channel duplicates vs Repeat Posts / Restocks:
                    # Enforce full 24h cooldown to prevent duplicate reposts,
                    # while allowing genuine Restock / Return and Price-Drop exceptions!
                    from app.aliexpress.parser import detect_restock_deal
                    is_restock = detect_restock_deal(raw_text)

                    is_dup, dup_reason, is_price_drop = is_recent_cross_channel_duplicate(
                        extracted.product_id, ch, current_price=extracted.current_price, title=extracted.title or "",
                        cooldown_hours=getattr(settings, "DUPLICATE_COOLDOWN_HOURS", 24.0), raw_text=raw_text
                    )
                    if is_dup:
                        print(f"  [CROSS-CHANNEL DUPLICATE BLOCKED] {dup_reason}")
                        max_processed_id = max(max_processed_id, msg_id)
                        record_monitored_channel_last_id(ch, msg_id)
                        record_post_handled(ch, msg_id)
                        continue

                    if is_restock:
                        print(f"  [🚨 RESTOCK EXCEPTION] Competitor announced return/restock! Reposting with restock urgency hook.")
                    elif is_price_drop:
                        print(f"  [📉 PRICE-DROP EXCEPTION] {dup_reason}! Reposting with updated price & hook.")

                    if extracted.product_id and extracted.product_id in seen_products:
                        print(f"  [DUPLICATE IN CURRENT RUN] Product ID '{extracted.product_id}' was already published in this run!")
                        max_processed_id = max(max_processed_id, msg_id)
                        record_monitored_channel_last_id(ch, msg_id)
                        record_post_handled(ch, msg_id)
                        continue

                    if extracted.title and any(is_same_deal_title(extracted.title, st) for st in seen_titles):
                        print(f"  [SIMILAR TITLE IN CURRENT RUN] Deal title '{extracted.title[:40]}' matches deal already posted in this run!")
                        max_processed_id = max(max_processed_id, msg_id)
                        record_monitored_channel_last_id(ch, msg_id)
                        record_post_handled(ch, msg_id)
                        continue

                    if extracted.product_id:
                        seen_products.add(extracted.product_id)
                    if extracted.title:
                        seen_titles.append(extracted.title)

                    # 7. Product Photo inside DealScout Neon Frame
                    img_url = extracted.image_url or source_photo_url
                    if not extracted.is_coupon_list:
                        if not img_url:
                            print(f"  [NO PHOTO] Skipping deal without product image: {extracted.product_id}")
                            max_processed_id = max(max_processed_id, msg_id)
                            record_post_handled(ch, msg_id)
                            continue

                    # 8. Build affiliate URL (Coin link 90%+, Bundle link for bundle deals)
                    deal_type = getattr(extracted, 'deal_type', None) or detect_deal_type(
                        raw_text,
                        f"{extracted.original_url} {getattr(extracted, 'final_url', '') or ''} {extracted.canonical_url}"
                    )
                    aff_link = await affiliate_service.create_affiliate_link(
                        product_url=extracted.canonical_url,
                        product_id=extracted.product_id if not extracted.is_coupon_list else None,
                        deal_type=deal_type
                    )
                    from api.coin_bot import ensure_affiliate
                    aff_link = ensure_affiliate(aff_link, pid=extracted.product_id if not extracted.is_coupon_list else None)

                    # 10. Generate caption with clean Algerian format (Single monetized referral link)
                    caption = await caption_generator.generate(
                        title=extracted.title or "AliExpress Deal",
                        usd_price=extracted.current_price,
                        eur_price=extracted.current_price_eur,
                        affiliate_url=aff_link,
                        coupon_code=extracted.coupon_code,
                        seller_coupon=extracted.seller_coupon,
                        has_points_discount=extracted.has_points_discount,
                        country_info=extracted.country_info,
                        coupon_list=extracted.coupon_list if extracted.is_coupon_list else None,
                        promo_tag=None,
                        is_price_drop=is_price_drop,
                        is_restock=is_restock,
                        coin_url=None,
                        raw_text=raw_text,
                        deal_type=deal_type
                    )

                    # 10. Prepare Image with subtle circular DealScout logo watermark
                    local_img_file = None
                    if extracted.is_coupon_list:
                        # Use competitor's official promo/coupon banner photo if available
                        if source_photo_url:
                            downloaded = await media_downloader.download_image(source_photo_url, identifier=f"coupon_{extracted.product_id}")
                            if downloaded:
                                local_img_file = downloaded

                        # Fallback to official AliExpress Choice Day banner image
                        official_banner = os.path.join(settings.BASE_DIR, "storage", "assets", "choice_day_banner.png")
                        if not local_img_file and os.path.exists(official_banner):
                            local_img_file = official_banner

                        # Fallback to rendered card only if no banner is available
                        if not local_img_file and extracted.coupon_list:
                            local_img_file = media_renderer.render_coupon_bulletin_card(
                                extracted.coupon_list,
                                promo_title="Party Ready Sale"
                            )
                    elif img_url:
                        downloaded = await media_downloader.download_image(img_url, extracted.product_id)
                        if downloaded:
                            local_img_file = media_renderer.prepare_post_image(
                                downloaded,
                                extracted.product_id,
                                extracted.title,
                                usd_price=extracted.current_price
                            )

                    if not local_img_file:
                        max_processed_id = max(max_processed_id, msg_id)
                        continue  # Must ALWAYS have a valid rendered image (coupons or product)!

                    # 11. Save record
                    async with db_context() as s:
                        ch_record = (await s.execute(
                            select(Channel).where(Channel.username == ch)
                        )).scalar_one_or_none()
                        ch_id = ch_record.id if ch_record else 1

                        data_post = block.get("data-post", "")
                        msg_id = int(data_post.split("/")[-1]) if "/" in data_post and data_post.split("/")[-1].isdigit() else 888000 + len(published_deals)

                        src = (await s.execute(
                            select(SourceMessage).where(
                                SourceMessage.channel_id == ch_id,
                                SourceMessage.telegram_message_id == msg_id
                            )
                        )).scalar_one_or_none()

                        if not src:
                            src = SourceMessage(
                                channel_id=ch_id,
                                telegram_message_id=msg_id,
                                message_url=f"https://t.me/{ch}/{msg_id}",
                                raw_text=raw_text
                            )
                            s.add(src)
                            await s.flush()

                        deal = (await s.execute(
                            select(Deal).where(Deal.source_message_id == src.id)
                        )).scalar_one_or_none()

                        if not deal:
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
                                status="PENDING"
                            )
                            s.add(deal)
                            await s.flush()
                        else:
                            deal.affiliate_url = aff_link
                            deal.current_price = extracted.current_price
                            deal.current_price_eur = extracted.current_price_eur
                            deal.coupon_code = extracted.coupon_code
                            deal.local_image_path = str(local_img_file) if local_img_file else None
                            deal.status = "PENDING"
                            await s.flush()

                        gen_post = (await s.execute(
                            select(GeneratedPost).where(GeneratedPost.deal_id == deal.id)
                        )).scalar_one_or_none()

                        if not gen_post:
                            gen_post = GeneratedPost(
                                deal_id=deal.id,
                                title=deal.title,
                                caption=caption,
                                image_path=str(local_img_file) if local_img_file else None,
                                ai_model="clean_deals_v3",
                                ai_validation_status="APPROVED",
                                status="VALIDATED"
                            )
                            s.add(gen_post)
                        else:
                            gen_post.caption = caption
                            gen_post.image_path = str(local_img_file) if local_img_file else None

                        await s.commit()

                        # 9. Send Photo + Caption to Channel
                        success, err = await telegram_publisher.publish_deal(
                            session=s,
                            deal=deal,
                            caption=caption,
                            image_path=local_img_file,
                            force=True
                        )

                        if success:
                            post_msg_id = (await s.execute(
                                select(TelegramPost.telegram_message_id)
                                .where(TelegramPost.deal_id == deal.id)
                                .order_by(desc(TelegramPost.id))
                                .limit(1)
                            )).scalars().first()

                            # Auto-pin coupon bulletins
                            if extracted.is_coupon_list and post_msg_id:
                                try:
                                    bot_tok = settings.TELEGRAM_BOT_TOKEN
                                    target_ch = settings.TELEGRAM_CHANNEL_ID
                                    async with httpx.AsyncClient(timeout=10.0) as pc:
                                        await pc.post(
                                            f"https://api.telegram.org/bot{bot_tok}/pinChatMessage",
                                            json={"chat_id": target_ch, "message_id": post_msg_id, "disable_notification": False}
                                        )
                                except Exception as pe:
                                    logger.warning(f"Failed to auto-pin coupon bulletin {post_msg_id}: {pe}")

                            record_post_published(
                                ch, msg_id, deal.product_id, deal.title,
                                channel_msg_id=post_msg_id,
                                price=deal.current_price
                            )
                            record_deal_posted_time()

                            # Check and notify watchlist subscribers for price drops
                            try:
                                from app.publisher.watchlist import notify_watchlist_users
                                if deal.current_price:
                                    alerted = await notify_watchlist_users(
                                        product_id=deal.product_id,
                                        new_price=deal.current_price,
                                        title=deal.title,
                                        affiliate_url=aff_link
                                    )
                                    if alerted > 0:
                                        print(f"  [WATCHLIST] Sent price drop alert to {alerted} user(s) for {deal.product_id}!")
                            except Exception as wl_err:
                                logger.warning(f"Watchlist notification failed: {wl_err}")

                            published_deals.append({
                                "id": deal.id,
                                "channel": ch,
                                "title": deal.title,
                                "price": f"${deal.current_price} ({deal.current_price_eur}€)" if deal.current_price else "Coupons",
                                "link": aff_link
                            })
                            try:
                                print(f"\n  [PUBLISHED #{len(published_deals)} from @{ch}]")
                                print("  " + "-" * 50)
                                for line in caption.splitlines():
                                    print("   ", line)
                                print("  " + "-" * 50)
                            except Exception:
                                pass

                            await asyncio.sleep(2.0)
                        else:
                            print(f"  [!] Failed to publish: {err}")

                        max_processed_id = max(max_processed_id, msg_id)

                # Advance high-water mark up to highest post actually processed/filtered (preserves paced deals!)
                if max_processed_id and max_processed_id > (last_seen_id or 0):
                    record_monitored_channel_last_id(ch, max_processed_id)
                elif not to_process_blocks and current_max_id > (last_seen_id or 0):
                    record_monitored_channel_last_id(ch, current_max_id)

            except Exception as e:
                import traceback
                print(f"  [ERROR] @{ch}: {e}")
                traceback.print_exc()

    print("\n" + "=" * 70)
    print(f"SUCCESS: Published {len(published_deals)} deals to {settings.TARGET_CHANNEL_ID}!")
    print("=" * 70)

    # 10. Daily Tajmi3at / Compilations (~10:00 PM UTC+1 or forced)
    try:
        from app.publisher.regrouper import check_and_publish_regrouped_bulletins
        bulletins = await check_and_publish_regrouped_bulletins(force=force_tajmi3at)
        if bulletins:
            print(f"\n[TAJMI3AT] Published {len(bulletins)} daily roundup bulletin(s):")
            for b in bulletins:
                print(f"  - {b['category']}: {b['count']} items -> Msg #{b['message_id']}")
    except Exception as e:
        print(f"[TAJMI3AT ERROR] {e}")

    return len(published_deals)

if __name__ == "__main__":
    force_run = "--force" in sys.argv or "-f" in sys.argv
    force_tajmi3at = "--tajmi3at" in sys.argv or "--force-tajmi3at" in sys.argv
    asyncio.run(collect_and_post_last_10_deals(force=force_run, force_tajmi3at=force_tajmi3at))
