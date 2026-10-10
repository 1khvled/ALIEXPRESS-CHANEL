from __future__ import annotations
import asyncio
import re
import sys
import os
import json
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Set, Tuple, Any

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
    is_allowed_category,
    extract_telegram_html_text
)
from app.aliexpress.promos import promo_tracker
from app.aliexpress.affiliate import affiliate_service
from app.ai.generator_fr import france_caption_generator
from app.media.downloader import media_downloader
from app.media.renderer import media_renderer
from app.utils.logger import logger

TARGET_FRANCE_CHANNEL = getattr(settings, "FRANCE_TARGET_CHANNEL_ID", None) or os.getenv("FRANCE_TARGET_CHANNEL_ID", "@francedealsdz")
FRANCE_STATE_FILE = Path(settings.BASE_DIR) / "storage" / "state" / "france_published_state.json"

def get_bot_token() -> str:
    return (
        getattr(settings, "TELEGRAM_BOT_TOKEN", None)
        or getattr(settings, "ADMIN_BOT_TOKEN", None)
        or os.getenv("TELEGRAM_BOT_TOKEN", "")
        or ""
    )

# Dedicated, strictly verified French/European AliExpress channels
# NEVER include Algerian or Arabic channels here (their coins, coupons, and links do not work in France).
FRANCE_SOURCE_CHANNELS = [
    "AliFRDrop",
    "FranceCP",
    "PromoZoneFR"
]

def is_strictly_france_compatible_deal(raw_text: str, channel_username: str = "") -> Tuple[bool, str]:
    """
    Validates that a deal is strictly genuine and compatible with France / Europe.
    - Verified French channels (@AliFRDrop, @FranceCP, @PromoZoneFR) are accepted.
    - Arabic/Algerian channels are accepted ONLY if they explicitly dropped a France deal
      (e.g. they typed 'عروض ففرنسا', 'عروض فرنسا', 'خاص بفرنسا', French promo code, etc.).
    - Any deal containing domestic Algerian indicators (DZD, BaridiMob, 58 ولاية) is strictly rejected.
    """
    lower_text = (raw_text or "").lower()

    # 1. Reject any deal mentioning domestic Algerian currency, banking, or local shipping
    algerian_indicators = [
        "الجزائر", "dzd", "دينار", "بريدي موب", "بريد الجزائر", "58 ولاية",
        "yalidine", "kazi tour", "carré", "livraison algerie", "algeria", "algerie"
    ]
    if any(ind in lower_text for ind in algerian_indicators):
        return False, "Contains Algerian-specific text, currency or domestic shipping"

    clean_ch = channel_username.replace("@", "").lower()

    # 2. Verified French channels are native French sources
    verified_french_channels = {"alifrdrop", "francecp", "promozonefr"}
    if clean_ch in verified_french_channels:
        return True, "Verified French source channel"

    # 3. Check for explicit French drop indicators from other channels (e.g. 'عروض ففرنسا')
    from app.aliexpress.parser import is_france_deal
    if is_france_deal(raw_text):
        return True, "Explicit French drop detected ('عروض ففرنسا')"

    # 4. Known Algerian/Arabic channels without explicit French marker are rejected
    algerian_channels = {
        "megaphonna", "lodydeals", "zedstoreonline", "bnddeals",
        "ecksdeal", "aniscoupons", "coupon4dz", "couponsglobal"
    }
    if clean_ch in algerian_channels:
        return False, f"Channel @{channel_username} is an Algerian source without explicit France markers ('عروض ففرنسا')"

    return True, "Valid France deal"




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
        "published_deals_history": {},
        "monitored_channels": {},
        "last_run_time": 0.0,
        "last_deal_post_time": 0.0
    }

def is_recent_france_duplicate(
    product_id: Optional[str],
    current_price_eur: Optional[float] = None,
    title: str = "",
    raw_text: str = "",
    cooldown_hours: float = 24.0,
    state: Optional[Dict] = None
) -> Tuple[bool, Optional[str], bool]:
    """
    Evaluates whether a France deal is a recent duplicate or qualifies for an exception:
    1. Restock / Return Exception: If seller restocked, always allow re-posting.
    2. Price-Drop Exception: If price dropped by >= 4% or >= 3€, allow with is_price_drop=True.
    3. 24h Cooldown: If older than cooldown_hours, allow re-posting fresh.
    """
    if not product_id or str(product_id).strip() == "":
        return False, None, False

    pid = str(product_id).strip()

    # 1. Restock Exception
    from app.aliexpress.parser import detect_restock_deal
    if detect_restock_deal(raw_text):
        return False, "Restock exception: return/restock deal", False

    if state is None:
        state = load_france_state()

    deals_history = state.get("published_deals_history", {})
    record = None
    if isinstance(deals_history, dict):
        record = deals_history.get(pid)
    elif isinstance(deals_history, list):
        for item in reversed(deals_history):
            if str(item.get("product_id")) == pid:
                record = item
                break

    if not record:
        return False, None, False

    prev_time = record.get("timestamp", 0.0)
    prev_price = record.get("price_eur")
    now = datetime.now(timezone.utc).timestamp()
    age_hours = (now - prev_time) / 3600.0

    # 2. Cooldown check
    if age_hours < cooldown_hours:
        # Check price drop exception
        if current_price_eur and prev_price and prev_price > 0:
            if current_price_eur <= (prev_price * 0.96) or (current_price_eur <= prev_price - 3.0):
                return False, f"Price drop exception: {prev_price}€ -> {current_price_eur}€", True

        return True, f"Product {pid} already posted to France {age_hours:.1f}h ago (< {cooldown_hours}h cooldown)", False

    return False, None, False

def record_france_deal_published(
    state: Dict,
    product_id: Optional[str],
    title: str,
    price_eur: Optional[float],
    channel_msg_id: Optional[int],
    post_key: Optional[str] = None
):
    now = datetime.now(timezone.utc).timestamp()
    if post_key:
        state.setdefault("published_post_keys", []).append(post_key)
        state["published_post_keys"] = list(dict.fromkeys(state["published_post_keys"]))[-1000:]
    if product_id:
        pid = str(product_id).strip()
        state.setdefault("published_product_ids", []).append(pid)
        state["published_product_ids"] = list(dict.fromkeys(state["published_product_ids"]))[-1000:]
        state.setdefault("published_deals_history", {})[pid] = {
            "timestamp": now,
            "title": title,
            "price_eur": price_eur,
            "channel_msg_id": channel_msg_id
        }
    state["last_deal_post_time"] = now

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
    image_path: Optional[Any],
    affiliate_url: str,
    is_coupon_bulletin: bool = False
) -> Tuple[bool, Optional[str], Optional[int]]:
    bot_token = get_bot_token()
    if not bot_token:
        return False, "TELEGRAM_BOT_TOKEN not configured", None

    api_url = f"https://api.telegram.org/bot{bot_token}"
    photo_bytes = None
    photo_url = None
    if image_path:
        p_str = str(image_path)
        if p_str.startswith("http://") or p_str.startswith("https://"):
            photo_url = p_str
        else:
            p = Path(image_path)
            if p.exists():
                photo_bytes = p.read_bytes()

    # Premium inline buttons for French deals (Clean CTA + Bot link)
    reply_markup_json = None
    if affiliate_url and affiliate_url.startswith("http"):
        btn_text = "🎟️ Voir les codes promo AliExpress" if is_coupon_bulletin else "🛒 Voir le bon plan sur AliExpress ➔"
        inline_keyboard = [
            [{"text": btn_text, "url": affiliate_url}],
            [{"text": "🪙 Bot Pièces AliExpress (Coins)", "url": "https://t.me/Alilo07BOT"}]
        ]
        reply_markup_json = json.dumps({"inline_keyboard": inline_keyboard})

    async with httpx.AsyncClient(timeout=45.0) as client:
        for attempt in range(1, 4):
            try:
                if photo_bytes:
                    files = {"photo": ("france_deal.jpg", photo_bytes, "image/jpeg")}
                    data = {
                        "chat_id": TARGET_FRANCE_CHANNEL,
                        "caption": caption,
                        "parse_mode": "HTML"
                    }
                    if reply_markup_json:
                        data["reply_markup"] = reply_markup_json
                    resp = await client.post(f"{api_url}/sendPhoto", data=data, files=files)
                elif photo_url:
                    payload = {
                        "chat_id": TARGET_FRANCE_CHANNEL,
                        "photo": photo_url,
                        "caption": caption,
                        "parse_mode": "HTML"
                    }
                    if reply_markup_json:
                        payload["reply_markup"] = json.loads(reply_markup_json)
                    resp = await client.post(f"{api_url}/sendPhoto", json=payload)
                else:
                    data = {
                        "chat_id": TARGET_FRANCE_CHANNEL,
                        "text": caption,
                        "parse_mode": "HTML",
                        "disable_web_page_preview": False
                    }
                    if reply_markup_json:
                        data["reply_markup"] = reply_markup_json
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


async def publish_extracted_deal_to_france(
    extracted: Any,
    raw_text: str,
    source_photo_url: Optional[str] = None,
    channel_username: str = "",
    msg_id: int = 0
) -> bool:
    """
    Directly format and publish an extracted AliExpress deal to the France channel (@francedealsdz).
    Used when a French/European deal is routed from another monitor or webhook.
    """
    state = load_france_state()
    published_keys = set(state.get("published_post_keys", []))
    published_pids = set(state.get("published_product_ids", []))
    clean_ch = channel_username.replace("@", "").lower()
    post_key = f"{clean_ch}:{msg_id}" if clean_ch and msg_id else None

    if post_key and post_key in published_keys:
        logger.info(f"[FRANCE ROUTER] Skipping already published post key: {post_key}")
        return False

    valid_fr, fr_reason = is_strictly_france_compatible_deal(raw_text, channel_username=channel_username)
    if not valid_fr:
        logger.info(f"[FRANCE ROUTER] Rejected non-France deal: {fr_reason}")
        return False

    from app.aliexpress.parser import detect_restock_deal
    is_restock = detect_restock_deal(raw_text)

    if extracted.product_id and not extracted.is_coupon_list:
        is_dup, dup_reason, is_price_drop = is_recent_france_duplicate(
            product_id=extracted.product_id,
            current_price_eur=extracted.current_price_eur,
            title=extracted.title or "",
            raw_text=raw_text,
            cooldown_hours=24.0,
            state=state
        )
        if is_dup:
            logger.info(f"[FRANCE ROUTER] Duplicate product ID blocked: {dup_reason}")
            return False
    else:
        is_price_drop = False

    # Check category whitelist if not coupon list
    if not extracted.is_coupon_list:
        allowed, reject_reason = is_allowed_category(
            extracted.title or '',
            raw_text,
            channel_username=channel_username
        )
        if not allowed:
            logger.info(f"[FRANCE ROUTER] Category filtered: {reject_reason}")
            return False

    # Affiliate link
    deal_type = getattr(extracted, 'deal_type', None) or detect_deal_type(
        raw_text,
        f"{extracted.original_url} {getattr(extracted, 'final_url', '') or ''} {extracted.canonical_url}"
    )
    aff_link = await affiliate_service.create_affiliate_link(
        product_url=extracted.canonical_url,
        product_id=extracted.product_id if not extracted.is_coupon_list else None,
        deal_type=deal_type
    )

    # Caption
    caption = await france_caption_generator.generate(
        title=extracted.title or "AliExpress Deal",
        eur_price=extracted.current_price_eur,
        usd_price=extracted.current_price,
        affiliate_url=aff_link,
        coupon_code=extracted.coupon_code,
        seller_coupon=extracted.seller_coupon,
        has_points_discount=extracted.has_points_discount,
        coupon_list=extracted.coupon_list if extracted.is_coupon_list else None,
        is_price_drop=is_price_drop,
        is_restock=is_restock,
        deal_type=deal_type,
        country_info=getattr(extracted, 'country_info', None),
        raw_text=raw_text
    )

    # Image preparation
    local_img_file = None
    img_url = extracted.image_url or source_photo_url
    if extracted.is_coupon_list:
        if extracted.coupon_list:
            active_p = promo_tracker.get_active_promo()
            promo_title = active_p.name if active_p else "Brand Day"
            local_img_file = media_renderer.render_coupon_bulletin_card(
                extracted.coupon_list,
                promo_title=promo_title,
                channel_handle="@francedealsdz",
                is_french=True
            )

        if not local_img_file and source_photo_url:
            downloaded = await media_downloader.download_image(source_photo_url, identifier=f"fr_coupon_{extracted.product_id or 'list'}")
            if downloaded:
                local_img_file = downloaded

        official_banner = os.path.join(settings.BASE_DIR, "storage", "assets", "choice_day_banner.png")
        if not local_img_file and os.path.exists(official_banner):
            local_img_file = Path(official_banner)
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
        logger.warning(f"[FRANCE ROUTER] Failed to prepare image for deal {extracted.product_id}")
        return False

    success, err, channel_msg_id = await post_deal_to_france_channel(
        caption=caption,
        image_path=local_img_file,
        affiliate_url=aff_link,
        is_coupon_bulletin=extracted.is_coupon_list
    )

    if success:
        record_france_deal_published(
            state=state,
            product_id=extracted.product_id,
            title=extracted.title or "Deal",
            price_eur=extracted.current_price_eur,
            channel_msg_id=channel_msg_id,
            post_key=post_key
        )
        save_france_state(state)
        print(f"  [FRANCE ROUTED PUBLISHED] Msg #{channel_msg_id}: {extracted.title}")

        if extracted.is_coupon_list and channel_msg_id:
            try:
                bot_tok = get_bot_token()
                async with httpx.AsyncClient(timeout=10.0) as pc:
                    await pc.post(
                        f"https://api.telegram.org/bot{bot_tok}/pinChatMessage",
                        json={"chat_id": TARGET_FRANCE_CHANNEL, "message_id": channel_msg_id, "disable_notification": False}
                    )
            except Exception as pe:
                logger.warning(f"Failed to auto-pin France coupon bulletin {channel_msg_id}: {pe}")
        return True
    else:
        logger.warning(f"[FRANCE ROUTER] Publish to {TARGET_FRANCE_CHANNEL} failed: {err}")
        return False

async def collect_and_post_france_deals(force: bool = False, force_tajmi3at: bool = False) -> int:
    print("=" * 70)
    print("ALIEXPRESS FRANCE DEALS PUBLISHER (STRICT QUALITY & FRESHNESS)")
    print(f"Target Channel: {TARGET_FRANCE_CHANNEL}")
    print(f"Source Channels: {', '.join(FRANCE_SOURCE_CHANNELS)}")
    print("=" * 70)

    # 0. Autonomous Promo Notifiers & Event Alerts (24h start warm-up & 24h end alert + pinned coupon bulletin)
    try:
        from app.publisher.promo_notifiers_fr import check_and_auto_post_france_promo_notifiers
        fr_alerts = await check_and_auto_post_france_promo_notifiers()
        if fr_alerts:
            print(f"  [FRANCE PROMO ALERTS] Triggered {len(fr_alerts)} alert(s): {[a.get('type') for a in fr_alerts]}")
    except Exception as e:
        print(f"  [!] France promo notifiers warning: {e}")

    # 0.5. Daily Tajmi3at / Compilations (~10:00 PM CET 21:30 - 23:45 or forced)
    try:
        from app.publisher.regrouper_fr import check_and_publish_france_regrouped_bulletins
        bulletins = await check_and_publish_france_regrouped_bulletins(force=force_tajmi3at)
        if bulletins:
            print(f"\n[FRANCE ROUNDUP] Published {len(bulletins)} daily roundup bulletin(s): {[b['category'] for b in bulletins]}")
    except Exception as e:
        print(f"  [!] France daily roundup check error: {e}")

    # 0.6. Automated Check: Day-to-Day Card & Cashback Affiliate Marketing (Bybit 100% Free + Cashback, RedotPay Visa, Binance SEPA)
    try:
        from app.publisher.card_affiliates import post_card_affiliate_france
        force_cards = "--cards" in sys.argv or "--force-cards" in sys.argv
        fr_card_success, fr_card_msg = await post_card_affiliate_france(force=force_cards)
        if fr_card_success:
            print(f"  [FRANCE CARD AFFILIATE AUTO-POST] {fr_card_msg}")
    except Exception as e:
        print(f"  [!] France card affiliate check error: {e}")

    # 0.7. Dynamic Interval & Day/Night Schedule Check (40 min daytime sweep, night paused)
    from app.publisher.state_tracker import is_deal_posting_due, record_sweep_completed
    is_due, schedule_msg, active_interval = is_deal_posting_due(channel="france")
    print(f"\n[FRANCE SCHEDULE EVALUATION] {schedule_msg}")
    if not is_due and not force:
        print(f"--> Skipping France deal collection this run. ({schedule_msg})")
        return 0

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
                handled_keys = set(state.get("handled_post_keys", []))
                lookback_cutoff = max(0, last_seen_id - 15)
                new_blocks = [
                    (b_id, b) for b_id, b in block_items
                    if (b_id > last_seen_id or (b_id >= lookback_cutoff and f"{clean_ch}:{b_id}" not in published_keys and f"{clean_ch}:{b_id}" not in handled_keys))
                    and f"{clean_ch}:{b_id}" not in published_keys
                ]

            # Pre-filter for message freshness (< 24h normally, or < 72h during active promo/force)
            fresh_blocks = []
            active_promo = promo_tracker.get_active_promo()
            max_age_hours = 72.0 if (active_promo or force) else 24.0
            for b_id, b in new_blocks:
                time_el = b.find("time")
                msg_dt = None
                if time_el and time_el.get("datetime"):
                    try:
                        msg_dt = datetime.fromisoformat(time_el["datetime"].replace("Z", "+00:00"))
                    except Exception:
                        pass
                if msg_dt:
                    age_h = (datetime.now(timezone.utc) - msg_dt).total_seconds() / 3600.0
                    if age_h > max_age_hours:
                        if f"{clean_ch}:{b_id}" not in state.get("handled_post_keys", []):
                            state.setdefault("handled_post_keys", []).append(f"{clean_ch}:{b_id}")
                        continue
                fresh_blocks.append((b_id, b))

            save_france_state(state)
            print(f"  [@{ch}] Found {len(fresh_blocks)} fresh candidate(s) to process (last seen #{last_seen_id})")

            # Pacing: limit per channel per cycle
            if len(fresh_blocks) > MAX_DEALS_PER_CHANNEL:
                print(f"  [PACING] Channel @{ch} has {len(fresh_blocks)} candidates. Pacing top {MAX_DEALS_PER_CHANNEL}.")
                to_process_blocks = fresh_blocks[:MAX_DEALS_PER_CHANNEL]
            else:
                to_process_blocks = fresh_blocks

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

                raw_text = extract_telegram_html_text(t_div)

                # Strict France-specific validation: reject any Arabic/Algerian deal or non-compatible source
                valid_fr, fr_reason = is_strictly_france_compatible_deal(raw_text, channel_username=ch)
                if not valid_fr:
                    print(f"  [NOT FRANCE COMPATIBLE] Post #{msg_id} from @{ch}: {fr_reason}")
                    published_keys.add(post_key)
                    max_processed_id = max(max_processed_id, msg_id)
                    continue

                # Autonomous Event Knower: Sniff any official promo festivals, sale announcements, or coupon batches
                try:
                    sniffed_ev = promo_tracker.sniff_and_register_event(raw_text, media_url=source_photo_url)
                    if sniffed_ev:
                        print(f"  [EVENT KNOWER FR] Discovered & registered event: {sniffed_ev.name} ({sniffed_ev.start_date.strftime('%d/%m')} - {sniffed_ev.end_date.strftime('%d/%m')}) with {len(sniffed_ev.coupon_tiers_fr or [])} FR codes, {len(sniffed_ev.coupon_tiers)} DZ codes")
                except Exception as ev_err:
                    logger.debug(f"Event sniffing skipped: {ev_err}")

                # 1. Parse message timestamp and enforce maximum freshness
                time_el = block.find("time")
                msg_dt = None
                if time_el and time_el.get("datetime"):
                    try:
                        msg_dt = datetime.fromisoformat(time_el["datetime"].replace("Z", "+00:00"))
                    except Exception:
                        pass

                # 2. Strict freshness check & expired promo check
                is_fresh, freshness_reason = promo_tracker.validate_deal_freshness(raw_text, msg_dt, max_hours=int(max_age_hours))
                if not is_fresh:
                    print(f"  [EXPIRED / STALE SKIPPED] Post #{msg_id}: {freshness_reason}")
                    published_keys.add(post_key)
                    max_processed_id = max(max_processed_id, msg_id)
                    continue

                # 3. Spam & non-deal filtering
                is_spam, spam_reason = is_spam_or_non_deal(raw_text)
                if is_spam:
                    print(f"  [SPAM FILTERED] Post #{msg_id}: {spam_reason}")
                    published_keys.add(post_key)
                    max_processed_id = max(max_processed_id, msg_id)
                    continue

                # 4. Extract product or coupon bulletin
                extracted = await product_extractor.extract_from_message(raw_text, media_path=source_photo_url)
                if not extracted or not extracted.is_valid:
                    has_ali_link = bool(re.search(r'(?:aliexpress\.(?:com|ru)|s\.click\.aliexpress\.com)', raw_text, re.IGNORECASE))
                    if has_ali_link:
                        print(f"  [TRANSIENT EXTRACTION FAILURE] Post #{msg_id} has AliExpress link but extraction was incomplete. Leaving for retry.")
                        continue
                    published_keys.add(post_key)
                    max_processed_id = max(max_processed_id, msg_id)
                    continue

                # 5. Category whitelist & Coupon bulletin check
                if extracted.is_coupon_list:
                    if not promo_tracker.get_active_promo():
                        print(f"  [COUPON BULLETIN BLOCKED] No active promo. Skipping coupon list: #{msg_id}")
                        published_keys.add(post_key)
                        max_processed_id = max(max_processed_id, msg_id)
                        continue
                else:
                    allowed, reject_reason = is_allowed_category(
                        extracted.title or '',
                        raw_text,
                        channel_username=ch
                    )
                    if not allowed:
                        print(f"  [CATEGORY FILTERED] Post #{msg_id}: {reject_reason}")
                        published_keys.add(post_key)
                        max_processed_id = max(max_processed_id, msg_id)
                        continue

                # 6. Deduplicate by product ID within France channel (24h cooldown, restock & price drop exceptions)
                from app.aliexpress.parser import detect_restock_deal
                is_restock = detect_restock_deal(raw_text)

                if extracted.product_id and not extracted.is_coupon_list:
                    is_dup, dup_reason, is_price_drop = is_recent_france_duplicate(
                        product_id=extracted.product_id,
                        current_price_eur=extracted.current_price_eur,
                        title=extracted.title or "",
                        raw_text=raw_text,
                        cooldown_hours=24.0,
                        state=state
                    )
                    if is_dup:
                        print(f"  [DUPLICATE BLOCKED] {dup_reason}")
                        published_keys.add(post_key)
                        max_processed_id = max(max_processed_id, msg_id)
                        continue
                else:
                    is_price_drop = False

                # 7. Official Studio Photo ONLY (Never leak competitor channel watermarks)
                img_url = extracted.image_url
                if not img_url and extracted.product_id:
                    img_url = await product_extractor._fetch_clean_aliexpress_image(extracted.product_id)
                if not extracted.is_coupon_list:
                    if not img_url or not any(domain in str(img_url) for domain in ["alicdn.com", "aliexpress-media.com", "aliexpress.com"]):
                        print(f"  [NO OFFICIAL PHOTO] Skipping deal without clean AliExpress CDN image: {extracted.product_id}")
                        published_keys.add(post_key)
                        max_processed_id = max(max_processed_id, msg_id)
                        continue

                # 8. Build France affiliate URL
                deal_type = getattr(extracted, 'deal_type', None) or detect_deal_type(
                    raw_text,
                    f"{extracted.original_url} {getattr(extracted, 'final_url', '') or ''} {extracted.canonical_url}"
                )
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
                    is_price_drop=is_price_drop,
                    is_restock=is_restock,
                    deal_type=deal_type,
                    country_info=getattr(extracted, 'country_info', None),
                    raw_text=raw_text
                )

                # 10. Prepare image
                local_img_file = None
                if extracted.is_coupon_list:
                    if extracted.coupon_list:
                        active_p = promo_tracker.get_active_promo()
                        promo_title = active_p.name if active_p else "Brand Day"
                        local_img_file = media_renderer.render_coupon_bulletin_card(
                            extracted.coupon_list,
                            promo_title=promo_title,
                            channel_handle="@francedealsdz",
                            is_french=True
                        )

                    if not local_img_file and source_photo_url:
                        downloaded = await media_downloader.download_image(source_photo_url, identifier=f"fr_coupon_{extracted.product_id}")
                        if downloaded:
                            local_img_file = downloaded

                    # Fallback to official AliExpress Choice Day banner image
                    official_banner = os.path.join(settings.BASE_DIR, "storage", "assets", "choice_day_banner.png")
                    if not local_img_file and os.path.exists(official_banner):
                        local_img_file = Path(official_banner)
                elif img_url:
                    downloaded = await media_downloader.download_image(img_url, extracted.product_id)
                    if downloaded:
                        local_img_file = media_renderer.prepare_post_image(
                            downloaded,
                            extracted.product_id,
                            extracted.title,
                            usd_price=extracted.current_price
                        )

                if not local_img_file and img_url:
                    local_img_file = img_url

                if not local_img_file:
                    print(f"  [IMAGE MISSING] Could not prepare image for product #{extracted.product_id}. Skipping.")
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
                    record_france_deal_published(
                        state=state,
                        product_id=extracted.product_id,
                        title=extracted.title or "Deal",
                        price_eur=extracted.current_price_eur,
                        channel_msg_id=channel_msg_id,
                        post_key=post_key
                    )
                    max_processed_id = max(max_processed_id, msg_id)
                    print(f"  [PUBLISHED #{published_count} to {TARGET_FRANCE_CHANNEL}] Msg #{channel_msg_id}: {extracted.title}")

                    # Auto-pin coupon bulletins
                    if extracted.is_coupon_list and channel_msg_id:
                        try:
                            bot_tok = get_bot_token()
                            async with httpx.AsyncClient(timeout=10.0) as pc:
                                await pc.post(
                                    f"https://api.telegram.org/bot{bot_tok}/pinChatMessage",
                                    json={"chat_id": TARGET_FRANCE_CHANNEL, "message_id": channel_msg_id, "disable_notification": False}
                                )
                        except Exception as pe:
                            logger.warning(f"Failed to auto-pin France coupon bulletin {channel_msg_id}: {pe}")

                    await asyncio.sleep(2.0)
                else:
                    print(f"  [!] Publish to {TARGET_FRANCE_CHANNEL} failed: {err}")
                    try:
                        from app.publisher.admin_alerts import notify_admin_error
                        await notify_admin_error("فشل نشر صفقة فرنسا (FR Deal Publish Failed)", f"Product {extracted.product_id} ({extracted.title[:50]}): {err}", channel="france")
                    except Exception:
                        pass
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
    record_sweep_completed(channel="france")

    print("\n" + "=" * 70)
    print(f"FRANCE RUN FINISHED: Published {published_count} deals to {TARGET_FRANCE_CHANNEL}!")
    print("=" * 70)

    # 10. Daily Tajmi3at / Compilations (~10:00 PM CET or forced)
    try:
        from app.publisher.regrouper_fr import check_and_publish_france_regrouped_bulletins
        bulletins = await check_and_publish_france_regrouped_bulletins(force=force_tajmi3at)
        if bulletins:
            print(f"\n[FRANCE ROUNDUP] Published {len(bulletins)} daily roundup bulletin(s):")
            for b in bulletins:
                print(f"  - {b['category']}: {b['count']} items -> Msg #{b['message_id']}")
    except Exception as e:
        print(f"[FRANCE ROUNDUP ERROR] {e}")

    return published_count

if __name__ == "__main__":
    force_run = "--force" in sys.argv or "-f" in sys.argv
    force_tajmi3at = "--tajmi3at" in sys.argv or "--force-tajmi3at" in sys.argv
    try:
        res = asyncio.run(collect_and_post_france_deals(force=force_run, force_tajmi3at=force_tajmi3at))
        sys.exit(0)
    except Exception as e:
        logger.critical(f"FATAL ERROR in France deals publisher: {e}", exc_info=True)
        sys.exit(1)
