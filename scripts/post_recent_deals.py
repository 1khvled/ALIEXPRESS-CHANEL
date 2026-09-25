import asyncio
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

from datetime import datetime, timezone
import httpx
from bs4 import BeautifulSoup
from sqlalchemy import select

from app.config.settings import settings
from app.db.session import init_db, db_context
from app.db.models import Channel, SourceMessage, Deal, GeneratedPost
from app.aliexpress.product import product_extractor
from app.aliexpress.parser import is_spam_or_non_deal, is_allowed_category, detect_deal_type
from app.aliexpress.promos import promo_tracker
from app.aliexpress.affiliate import affiliate_service
from app.ai.generator import caption_generator
from app.media.downloader import media_downloader
from app.media.renderer import media_renderer
from app.publisher.publisher import telegram_publisher
from app.utils.logger import logger
# Channels to monitor for deals (photos are fetched exclusively from AliExpress CDN)
CHANNELS = [
    "Pcgamingpart",
    "zedstoreonline",
    "aniscoupons",
    "ECKSDEAL",
    "lodydeals",
    "BNDDEALS"
]

async def collect_and_post_last_10_deals():
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

    published_deals = []
    seen_products = set()



    # Load existing published products
    async with db_context() as s:
        existing_pids = (await s.execute(
            select(Deal.product_id).where(Deal.status == "PUBLISHED")
        )).scalars().all()
        for pid in existing_pids:
            if pid:
                seen_products.add(pid)

    print(f"Loaded {len(seen_products)} existing published products for deduplication.")

    MAX_DEALS_PER_RUN = 2

    async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
        for ch in CHANNELS:
            if len(published_deals) >= MAX_DEALS_PER_RUN:
                break

            url = f"https://t.me/s/{ch}"
            print(f"\n---> Scanning channel @{ch}...")
            try:
                resp = await client.get(url)
                if resp.status_code != 200:
                    print(f"  [!] HTTP {resp.status_code} for @{ch}")
                    continue

                soup = BeautifulSoup(resp.text, "html.parser")
                blocks = soup.find_all("div", class_="tgme_widget_message")
                print(f"  Found {len(blocks)} message blocks in @{ch}")

                for block in reversed(blocks):
                    if len(published_deals) >= MAX_DEALS_PER_RUN:
                        break

                    text_div = block.find("div", class_="tgme_widget_message_text")
                    if not text_div:
                        continue

                    raw_text = text_div.get_text(separator="\n").strip()

                    # 1. Parse message timestamp and enforce maximum 24h freshness
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
                        continue

                    # 3. Smart spam filtering
                    is_spam, spam_reason = is_spam_or_non_deal(raw_text)
                    if is_spam:
                        continue

                    # 4. Extract deal or coupon list
                    extracted = await product_extractor.extract_from_message(raw_text)
                    if not extracted or not extracted.is_valid:
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
                            continue

                    # 6. Strict Deduplication check (Persistent JSON State + DB + Live Channel text)
                    from app.publisher.state_tracker import is_product_already_published, record_product_published
                    already_pub, pub_reason = await is_product_already_published(extracted.product_id, extracted.title or "")
                    if already_pub:
                        print(f"  [DUPLICATE STRICT SKIPPED] {pub_reason}")
                        continue

                    if extracted.product_id in seen_products:
                        print(f"  [DUPLICATE SKIPPED] '{extracted.product_id}' already seen in current run.")
                        continue

                    seen_products.add(extracted.product_id)

                    # 7. Official Studio Photo ONLY — NEVER use competitor Telegram channel photos!
                    # Only accept official AliExpress CDN images (alicdn.com, aliexpress-media.com)
                    img_url = extracted.image_url
                    if not extracted.is_coupon_list:
                        if not img_url or not any(domain in img_url for domain in ["alicdn.com", "aliexpress-media.com", "aliexpress.com"]):
                            print(f"  [NO OFFICIAL PHOTO] Skipping deal without clean AliExpress CDN image: {extracted.product_id}")
                            continue

                    # 8. Build affiliate URL (Coin link 90%+, Bundle link for bundle deals)
                    deal_type = detect_deal_type(raw_text, extracted.canonical_url)
                    aff_link = await affiliate_service.create_affiliate_link(
                        product_url=extracted.canonical_url,
                        product_id=extracted.product_id if not extracted.is_coupon_list else None,
                        deal_type=deal_type
                    )

                    # 9. Generate caption with promo banner if active
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

                    # 10. Prepare Image with subtle circular DealScout logo watermark
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
                        continue  # Must have valid rendered product image unless it's a coupon list bulletin

                    # 11. Save record
                    async with db_context() as s:
                        ch_record = (await s.execute(
                            select(Channel).where(Channel.username == ch)
                        )).scalar_one_or_none()
                        ch_id = ch_record.id if ch_record else 1

                        data_post = block.get("data-post", "")
                        msg_id = int(data_post.split("/")[-1]) if "/" in data_post and data_post.split("/")[-1].isdigit() else 888000 + len(published_deals)

                        src = SourceMessage(
                            channel_id=ch_id,
                            telegram_message_id=msg_id,
                            message_url=f"https://t.me/{ch}/{msg_id}",
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
                            ai_model="clean_deals_v3",
                            ai_validation_status="APPROVED",
                            status="VALIDATED"
                        )
                        s.add(gen_post)
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
                            record_product_published(deal.product_id, deal.title)
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

            except Exception as e:
                import traceback
                print(f"  [ERROR] @{ch}: {e}")
                traceback.print_exc()

    print("\n" + "=" * 70)
    print(f"SUCCESS: Published {len(published_deals)} deals to {settings.TARGET_CHANNEL_ID}!")
    print("=" * 70)

    # 10. Check if homogeneous product regrouping is ready (>= 4 of same category)
    try:
        from app.publisher.regrouper import check_and_publish_regrouped_bulletins
        bulletins = await check_and_publish_regrouped_bulletins()
        if bulletins:
            print(f"\n[REGROUP] Published {len(bulletins)} regrouped bulletin(s):")
            for b in bulletins:
                print(f"  - {b['category']}: {b['count']} items -> Msg #{b['message_id']}")
    except Exception as e:
        print(f"[REGROUP ERROR] {e}")

if __name__ == "__main__":
    asyncio.run(collect_and_post_last_10_deals())
