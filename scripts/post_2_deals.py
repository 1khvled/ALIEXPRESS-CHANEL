import asyncio
import re
import sys
from pathlib import Path
from datetime import datetime, timezone

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

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

CHANNELS = [
    "Pcgamingpart",
    "zedstoreonline",
    "aniscoupons",
    "ECKSDEAL"
]

async def post_last_2():
    await init_db()
    published = []
    seen = set()

    print("=" * 60)
    print("POSTING 2 VERIFIED DEALS TO @DzAliexpress0")
    print("=" * 60)

    async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
        for ch in CHANNELS:
            if len(published) >= 2:
                break

            url = f"https://t.me/s/{ch}"
            print(f"\n---> Scanning @{ch}...")
            resp = await client.get(url)
            if resp.status_code != 200:
                continue

            soup = BeautifulSoup(resp.text, "html.parser")
            blocks = soup.find_all("div", class_="tgme_widget_message")

            for block in reversed(blocks):
                if len(published) >= 2:
                    break

                text_div = block.find("div", class_="tgme_widget_message_text")
                if not text_div:
                    continue

                raw_text = text_div.get_text(separator="\n").strip()

                # Spam check
                is_spam, _ = is_spam_or_non_deal(raw_text)
                if is_spam:
                    continue

                # Extract product
                extracted = await product_extractor.extract_from_message(raw_text)
                if not extracted or not extracted.is_valid:
                    continue

                # Category whitelist
                allowed, reason = is_allowed_category(extracted.title or '', raw_text)
                if not allowed:
                    continue

                if extracted.product_id in seen:
                    continue
                seen.add(extracted.product_id)

                # Pure AliExpress CDN photo only
                img_url = extracted.image_url
                if not img_url or not any(d in img_url for d in ["alicdn.com", "aliexpress-media.com", "aliexpress.com"]):
                    continue

                # Build real s.click affiliate link
                aff_link = await affiliate_service.create_affiliate_link(
                    product_url=extracted.canonical_url,
                    product_id=extracted.product_id
                )

                # Generate clean caption
                caption = await caption_generator.generate(
                    title=extracted.title or "AliExpress Deal",
                    usd_price=extracted.current_price,
                    eur_price=extracted.current_price_eur,
                    affiliate_url=aff_link,
                    coupon_code=extracted.coupon_code,
                    has_points_discount=extracted.has_points_discount,
                    country_info=extracted.country_info,
                    promo_tag=promo_tracker.get_promo_header()
                )

                # Download official AliExpress studio photo & apply Option A+B card
                downloaded = await media_downloader.download_image(img_url, extracted.product_id)
                if not downloaded:
                    continue

                local_img = media_renderer.prepare_post_image(
                    downloaded,
                    extracted.product_id,
                    extracted.title,
                    usd_price=extracted.current_price
                )
                if not local_img:
                    continue

                # Save & publish to Telegram
                async with db_context() as s:
                    deal = Deal(
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
                        local_image_path=str(local_img),
                        quality_score=95,
                        status="PUBLISHED"
                    )
                    s.add(deal)
                    await s.flush()

                    success, err = await telegram_publisher.publish_deal(
                        session=s,
                        deal=deal,
                        caption=caption,
                        image_path=local_img,
                        force=True
                    )

                    if success:
                        published.append({
                            "title": deal.title,
                            "price": f"${deal.current_price}",
                            "link": aff_link,
                            "image": img_url
                        })
                        print(f"\n[SUCCESS PUBLISHED #{len(published)}]")
                        print(f"Title: {deal.title}")
                        print(f"Price: ${deal.current_price}")
                        print(f"Link:  {aff_link}")
                        await asyncio.sleep(2.0)
                    else:
                        print(f"[!] Publish error: {err}")

    print(f"\nTotal Published: {len(published)} deals to {settings.TARGET_CHANNEL_ID}")

if __name__ == "__main__":
    asyncio.run(post_last_2())
