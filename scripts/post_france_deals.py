import asyncio
import re
import sys
import os
import json
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Set, Tuple

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

import httpx
from bs4 import BeautifulSoup

from app.config.settings import settings
from app.aliexpress.product import product_extractor
from app.aliexpress.parser import (
    is_spam_or_non_deal,
    detect_deal_type,
    extract_coupon_list,
    extract_prices,
    is_allowed_category
)
from app.aliexpress.promos import promo_tracker
from app.aliexpress.affiliate import affiliate_service
from app.ai.generator_fr import france_caption_generator
from app.media.downloader import media_downloader
from app.media.renderer import media_renderer
from app.utils.logger import logger

TARGET_FRANCE_CHANNEL = os.getenv("FRANCE_TARGET_CHANNEL_ID", "@francedealsdz")
FRANCE_STATE_FILE = Path(settings.BASE_DIR) / "storage" / "state" / "france_published_state.json"

FRANCE_SOURCE_CHANNELS = [
    "FranceCP"
]

def load_france_state() -> Dict:
    FRANCE_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    if FRANCE_STATE_FILE.exists():
        try:
            with open(FRANCE_STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading France state: {e}")
    return {
        "published_post_keys": [],
        "published_product_ids": [],
        "monitored_channels": {},
        "last_run_time": 0.0,
        "last_deal_post_time": 0.0
    }

def save_france_state(state: Dict):
    FRANCE_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        tmp = FRANCE_STATE_FILE.with_suffix(".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        if FRANCE_STATE_FILE.exists():
            os.replace(tmp, FRANCE_STATE_FILE)
        else:
            os.rename(tmp, FRANCE_STATE_FILE)
    except Exception as e:
        logger.error(f"Error saving France state: {e}")

async def post_deal_to_france_channel(
    caption: str,
    image_path: Optional[Path],
    affiliate_url: str,
    is_coupon_bulletin: bool = False
) -> Tuple[bool, Optional[str], Optional[int]]:
    bot_token = settings.TELEGRAM_BOT_TOKEN
    if not bot_token:
        return False, "TELEGRAM_BOT_TOKEN not configured", None

    api_url = f"https://api.telegram.org/bot{bot_token}"
    inline_keyboard = []
    if affiliate_url and affiliate_url.startswith("http"):
        btn_text = "🎟️ Voir les codes promo" if is_coupon_bulletin else "🛒 Acheter sur AliExpress"
        inline_keyboard.append([{"text": btn_text, "url": affiliate_url}])
    inline_keyboard.append([{"text": "📢 Rejoindre @francedealsdz", "url": "https://t.me/francedealsdz"}])
    reply_markup_json = json.dumps({"inline_keyboard": inline_keyboard})

    photo_bytes = None
    if image_path and image_path.exists():
        photo_bytes = image_path.read_bytes()

    async with httpx.AsyncClient(timeout=45.0) as client:
        for attempt in range(1, 4):
            try:
                if photo_bytes:
                    files = {"photo": ("france_deal.jpg", photo_bytes, "image/jpeg")}
                    data = {
                        "chat_id": TARGET_FRANCE_CHANNEL,
                        "caption": caption,
                        "parse_mode": "HTML",
                        "reply_markup": reply_markup_json
                    }
                    resp = await client.post(f"{api_url}/sendPhoto", data=data, files=files)
                else:
                    data = {
                        "chat_id": TARGET_FRANCE_CHANNEL,
                        "text": caption,
                        "parse_mode": "HTML",
                        "reply_markup": reply_markup_json
                    }
                    resp = await client.post(f"{api_url}/sendMessage", data=data)

                if resp.status_code == 200:
                    res_json = resp.json()
                    if res_json.get("ok"):
                        msg_id = res_json.get("result", {}).get("message_id")
                        return True, None, msg_id
                    return False, res_json.get("description", "Error"), None

                if resp.status_code == 403 or "not a member" in resp.text:
                    return False, f"403 Forbidden: @Alilo07BOT must be added as an Administrator to {TARGET_FRANCE_CHANNEL}", None

                logger.warning(f"France publish attempt {attempt} returned {resp.status_code}: {resp.text}")
                if attempt < 3:
                    await asyncio.sleep(2.0 * attempt)
            except Exception as e:
                logger.warning(f"France publish attempt {attempt} exception: {e}")
                if attempt < 3:
                    await asyncio.sleep(2.0 * attempt)

    return False, "Failed after 3 attempts", None

async def collect_and_post_france_deals():
    print("=" * 70)
    print("ALIEXPRESS FRANCE DEALS PUBLISHER (STRICT QUALITY & FRESHNESS)")
    print(f"Target Channel: {TARGET_FRANCE_CHANNEL}")
    print(f"Source Channels: {', '.join(FRANCE_SOURCE_CHANNELS)}")
    print("=" * 70)

    # 0. Autonomous Promo Notifiers & Event Alerts (24h start warm-up & 24h end alert)
    try:
        from app.publisher.promo_notifiers_fr import check_and_auto_post_france_promo_notifiers
        fr_alerts = await check_and_auto_post_france_promo_notifiers()
        if fr_alerts:
            print(f"  [FRANCE PROMO ALERTS] Triggered {len(fr_alerts)} alert(s): {[a.get('type') for a in fr_alerts]}")
    except Exception as e:
        print(f"  [!] France promo notifiers warning: {e}")

    state = load_france_state()
    published_keys = set(state.get("published_post_keys", []))
    published_pids = set(state.get("published_product_ids", []))
    monitored = state.get("monitored_channels", {})

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8"
    }

    published_count = 0
    # Pacing limits matching main bot: 3 deals per channel, max 4 per run
    MAX_DEALS_PER_RUN = 4
    MAX_DEALS_PER_CHANNEL = 3

    async with httpx.AsyncClient(headers=headers, timeout=20.0, follow_redirects=True) as client:
        for ch in FRANCE_SOURCE_CHANNELS:
            if published_count >= MAX_DEALS_PER_RUN:
                break

            clean_ch = ch.lower().lstrip("@")
            url = f"https://t.me/s/{clean_ch}"
            print(f"\n---> Scanning France source @{ch}...")

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
                continue

            current_max_id = max(b_id for b_id, _ in block_items)
            last_seen_id = monitored.get(clean_ch, {}).get("last_message_id")
            block_items.sort(key=lambda x: x[0])

            # FIRST RUN PROTECTION: If channel never tracked before, set baseline to current_max_id
            # so old historical backlog from days/weeks ago is NEVER dumped!
            if last_seen_id is None:
                monitored.setdefault(clean_ch, {})["last_message_id"] = current_max_id
                monitored[clean_ch]["last_check_time"] = time.time()
                state["monitored_channels"] = monitored
                save_france_state(state)
                # On first run, only evaluate the last 3 visible messages as fresh candidates
                new_blocks = [
                    (b_id, b) for b_id, b in block_items[-3:]
                    if f"{clean_ch}:{b_id}" not in published_keys
                ]
                print(f"  [FIRST RUN BASELINE] @{ch} baseline set to #{current_max_id}. Evaluating {len(new_blocks)} most recent candidate(s).")
            else:
                # Filter for posts strictly newer than last_seen_id OR unposted recent candidates
                lookback_cutoff = max(0, last_seen_id - 4)
                new_blocks = [
                    (b_id, b) for b_id, b in block_items
                    if (b_id > last_seen_id or (b_id >= lookback_cutoff and f"{clean_ch}:{b_id}" not in published_keys))
                    and f"{clean_ch}:{b_id}" not in published_keys
                ]

            print(f"  [@{ch}] Found {len(new_blocks)} candidate(s) to process (last seen #{last_seen_id})")

            # Pacing: limit per channel per cycle
            if len(new_blocks) > MAX_DEALS_PER_CHANNEL:
                print(f"  [PACING] Channel @{ch} has {len(new_blocks)} candidates. Pacing top {MAX_DEALS_PER_CHANNEL}.")
                to_process_blocks = new_blocks[:MAX_DEALS_PER_CHANNEL]
            else:
                to_process_blocks = new_blocks

            max_processed_id = last_seen_id or 0

            for msg_id, block in to_process_blocks:
                if published_count >= MAX_DEALS_PER_RUN:
                    break

                post_key = f"{clean_ch}:{msg_id}"
                t_div = block.find("div", class_="tgme_widget_message_text")
                if not t_div:
                    max_processed_id = max(max_processed_id, msg_id)
                    continue

                # Extract source post photo if present (competitor's coupon banner)
                source_photo_url = None
                photo_wrap = block.find("a", class_="tgme_widget_message_photo_wrap")
                if photo_wrap and photo_wrap.get("style"):
                    m_url = re.search(r"url\(['\"]?(https?://[^'\"]+)['\"]?\)", photo_wrap["style"])
                    if m_url:
                        source_photo_url = m_url.group(1)

                raw_text = t_div.get_text(separator="\n").strip()

                # 1. Parse message timestamp and enforce maximum 24h freshness (NO OLD DEALS!)
                time_el = block.find("time")
                msg_dt = None
                if time_el and time_el.get("datetime"):
                    try:
                        msg_dt = datetime.fromisoformat(time_el["datetime"].replace("Z", "+00:00"))
                    except Exception:
                        pass

                # 2. Strict freshness check & expired promo check
                is_fresh, freshness_reason = promo_tracker.validate_deal_freshness(raw_text, msg_dt)
                if not is_fresh:
                    print(f"  [EXPIRED / STALE SKIPPED] Post #{msg_id}: {freshness_reason}")
                    max_processed_id = max(max_processed_id, msg_id)
                    continue

                # 3. Spam & non-deal filtering
                is_spam, spam_reason = is_spam_or_non_deal(raw_text)
                if is_spam:
                    print(f"  [SPAM FILTERED] Post #{msg_id}: {spam_reason}")
                    max_processed_id = max(max_processed_id, msg_id)
                    continue

                # 4. Extract product or coupon bulletin
                extracted = await product_extractor.extract_from_message(raw_text)
                if not extracted or not extracted.is_valid:
                    max_processed_id = max(max_processed_id, msg_id)
                    continue

                # 5. Category whitelist: gaming, tech, audio, PC parts, phones, tablets, tools
                if not extracted.is_coupon_list:
                    allowed, reject_reason = is_allowed_category(
                        extracted.title or '',
                        raw_text,
                        channel_username=ch
                    )
                    if not allowed:
                        print(f"  [CATEGORY FILTERED] Post #{msg_id}: {reject_reason}")
                        max_processed_id = max(max_processed_id, msg_id)
                        continue

                # 6. Deduplicate by product ID within France channel
                if extracted.product_id and not extracted.is_coupon_list:
                    if extracted.product_id in published_pids:
                        print(f"  [DUPLICATE BLOCKED] Product {extracted.product_id} already published in France channel")
                        max_processed_id = max(max_processed_id, msg_id)
                        continue

                # 7. Official Studio Photo ONLY (or competitor's promo banner for coupons)
                img_url = extracted.image_url
                if not extracted.is_coupon_list:
                    if not img_url or not any(domain in img_url for domain in ["alicdn.com", "aliexpress-media.com", "aliexpress.com"]):
                        print(f"  [NO OFFICIAL PHOTO] Skipping deal without clean AliExpress CDN image: {extracted.product_id}")
                        max_processed_id = max(max_processed_id, msg_id)
                        continue

                # 8. Build France affiliate URL
                deal_type = detect_deal_type(raw_text, extracted.canonical_url)
                aff_link = await affiliate_service.create_affiliate_link(
                    product_url=extracted.canonical_url,
                    product_id=extracted.product_id if not extracted.is_coupon_list else None,
                    deal_type=deal_type
                )

                # 9. Generate French caption
                caption = await france_caption_generator.generate(
                    title=extracted.title or "AliExpress Deal",
                    eur_price=extracted.current_price_eur,
                    usd_price=extracted.current_price,
                    affiliate_url=aff_link,
                    coupon_code=extracted.coupon_code,
                    seller_coupon=extracted.seller_coupon,
                    has_points_discount=extracted.has_points_discount,
                    coupon_list=extracted.coupon_list if extracted.is_coupon_list else None,
                    is_price_drop=False,
                    raw_text=raw_text
                )

                # 10. Prepare image
                local_img_file = None
                if extracted.is_coupon_list:
                    if source_photo_url:
                        downloaded = await media_downloader.download_image(source_photo_url, identifier=f"fr_coupon_{extracted.product_id}")
                        if downloaded:
                            local_img_file = downloaded

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
                    continue

                # 11. Publish to France channel
                success, err, channel_msg_id = await post_deal_to_france_channel(
                    caption=caption,
                    image_path=local_img_file,
                    affiliate_url=aff_link,
                    is_coupon_bulletin=extracted.is_coupon_list
                )

                if success:
                    published_count += 1
                    published_keys.add(post_key)
                    if extracted.product_id:
                        published_pids.add(extracted.product_id)
                    max_processed_id = max(max_processed_id, msg_id)
                    print(f"  [PUBLISHED #{published_count} to {TARGET_FRANCE_CHANNEL}] Msg #{channel_msg_id}: {extracted.title}")
                    await asyncio.sleep(2.0)
                else:
                    print(f"  [!] Publish to {TARGET_FRANCE_CHANNEL} failed: {err}")
                    max_processed_id = max(max_processed_id, msg_id)
                    if "403" in str(err) or "Administrator" in str(err) or "member list is inaccessible" in str(err) or "chat not found" in str(err) or "bot is not a member" in str(err):
                        print(f"  [!] Action required: Add @Alilo07BOT as an Administrator to {TARGET_FRANCE_CHANNEL} with 'Post Messages' permission.")
                        break

            # Update high water mark
            if max_processed_id > (last_seen_id or 0):
                monitored.setdefault(clean_ch, {})["last_message_id"] = max_processed_id
                monitored[clean_ch]["last_check_time"] = time.time()

    # Save state
    state["published_post_keys"] = list(published_keys)[-1000:]
    state["published_product_ids"] = list(published_pids)[-1000:]
    state["monitored_channels"] = monitored
    state["last_run_time"] = time.time()
    if published_count > 0:
        state["last_deal_post_time"] = time.time()
    save_france_state(state)

    print("\n" + "=" * 70)
    print(f"FRANCE RUN FINISHED: Published {published_count} deals to {TARGET_FRANCE_CHANNEL}!")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(collect_and_post_france_deals())
