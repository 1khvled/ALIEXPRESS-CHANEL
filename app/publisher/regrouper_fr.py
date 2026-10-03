"""
Daily France Deals Regrouping & Roundup Bulletin Algorithm
Aggregates published deals of the day on @francedealsdz into high-converting
index bulletins linking directly to the channel's posts at ~10:00 PM CET.
Strict Rule: If category has >= 3 items, builds category bulletin;
otherwise builds a Master Daily Roundup ("Récapitulatif des Meilleurs Bons Plans du Jour").
"""
import os
import sys
import json
import re
import asyncio
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Tuple, Optional, Set
from pathlib import Path
import httpx

from app.config.settings import settings
from app.utils.logger import logger

TARGET_FRANCE_CHANNEL = os.getenv("FRANCE_TARGET_CHANNEL_ID", "@francedealsdz")
FRANCE_STATE_FILE = Path(settings.BASE_DIR) / "storage" / "state" / "france_published_state.json"

CATEGORIES_CONFIG_FR = {
    "smartphones": {
        "header": "📱 <b>Sélection des Meilleurs Smartphones du Jour 🇫🇷🔥</b>",
        "keywords": [
            "phone", "phones", "smartphone", "smartphones", "poco", "redmi",
            "realme", "honor", "samsung", "infinix", "oppo", "vivo", "iphone",
            "oneplus", "xiaomi", "nubia", "zte", "motorola", "iqoo"
        ],
        "negative_keywords": [
            "case", "cover", "holder", "charger", "cable", "mousepad",
            "screen protector", "glass", "film", "watch", "smartwatch", "stylus"
        ]
    },
    "gaming": {
        "header": "🎮 <b>Sélection Matériel Gaming & Périphériques 🇫🇷🔥</b>",
        "keywords": [
            "mouse", "mice", "keyboard", "keyboards", "gamepad", "controller",
            "gaming", "gamer", "attack shark", "ajazz", "aula", "vgn", "scyrox",
            "zaopin", "mechanical keyboard", "wireless mouse", "mousepad", "mouse pad",
            "tapis de souris", "gaming pad", "desk mat", "manette", "easysmx",
            "gamesir", "machenike", "fantech", "darmoshark", "ak820"
        ],
        "negative_keywords": ["keycap", "switch"]
    },
    "audio": {
        "header": "🎧 <b>Sélection Écouteurs & Audio du Jour 🇫🇷🔥</b>",
        "keywords": [
            "headset", "headphone", "headphones", "earbuds", "earbud", "earphone",
            "earphones", "tws", "speaker", "soundbar", "soundcore", "qcy", "anc",
            "attack shark l80", "attack shark l90", "lenovo lp", "lenovo xt", "edifier"
        ],
        "negative_keywords": ["case", "cover", "cable"]
    },
    "tech": {
        "header": "⚡ <b>Sélection High-Tech & Gadgets du Jour 🇫🇷🔥</b>",
        "keywords": [
            "camera", "dji", "osmo", "gimbal", "drone", "tablet", "pad", "ipad",
            "scooter", "trottinette", "charger", "gan", "powerbank", "ssd", "nvme",
            "ram", "watch", "smartwatch"
        ],
        "negative_keywords": []
    }
}


def load_france_state() -> Dict:
    if FRANCE_STATE_FILE.exists():
        try:
            with open(FRANCE_STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading France state: {e}")
    return {}

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

def is_france_roundup_time_window(now_dt: Optional[datetime] = None) -> bool:
    """Target window: 21:30 to 23:45 Paris local time (Europe/Paris CEST/CET)."""
    try:
        import zoneinfo
        paris_tz = zoneinfo.ZoneInfo("Europe/Paris")
    except Exception:
        paris_tz = timezone(timedelta(hours=2))

    if now_dt is None:
        now_dt = datetime.now(paris_tz)
    elif now_dt.tzinfo is None:
        now_dt = now_dt.replace(tzinfo=paris_tz)
    else:
        now_dt = now_dt.astimezone(paris_tz)

    hour = now_dt.hour
    minute = now_dt.minute
    return (hour == 21 and minute >= 30) or (hour == 22) or (hour == 23 and minute <= 45)

def is_france_roundup_eligible(date_str: Optional[str] = None) -> Tuple[bool, str]:
    state = load_france_state()
    if not date_str:
        try:
            import zoneinfo
            paris_tz = zoneinfo.ZoneInfo("Europe/Paris")
        except Exception:
            paris_tz = timezone(timedelta(hours=2))
        date_str = datetime.now(paris_tz).strftime("%Y-%m-%d")

    history = state.get("daily_roundup_history", {})
    if date_str in history:
        return False, f"Daily roundup already published for {date_str}"
    return True, "Eligible for daily roundup"

def record_france_roundup_published(date_str: str, bulletins_count: int, msg_ids: List[int]):
    state = load_france_state()
    state.setdefault("daily_roundup_history", {})[date_str] = {
        "timestamp": datetime.now(timezone.utc).timestamp(),
        "count": bulletins_count,
        "message_ids": msg_ids
    }
    save_france_state(state)

def classify_france_deal_category(title: str, text: str = "") -> Optional[str]:
    if not title:
        return None
    combined = f"{title} {text}".lower()

    for cat_name, config in CATEGORIES_CONFIG_FR.items():
        has_negative = any(neg in combined for neg in config["negative_keywords"])
        if has_negative:
            continue
        for kw in config["keywords"]:
            if kw in combined:
                return cat_name
    return None

def clean_item_title_fr(raw_title: str, max_chars: int = 55) -> str:
    """Produces clean, readable French title for the bulletin line without slicing words in half."""
    t = raw_title or "Bon Plan AliExpress"
    t = re.sub(r'[\$€].*$', '', t).strip()
    t = re.sub(r'^[❗️🔖📌🔥🚨⚡💥✨📦🛒🎁📢✅💎💰🔻ـ\s\-:]+', '', t).strip()
    t = re.sub(r'(\s*-\s*AliExpress.*$|\s*\|\s*AliExpress.*$)', '', t, flags=re.IGNORECASE).strip()
    t = re.sub(r'\b(Version\s+Globale|Global\s+Version|Original|Hot\s+Sale|Brand\s+New|Top\s+Selling|202[4-9])\b', '', t, flags=re.IGNORECASE).strip()
    t = re.sub(r'\s+', ' ', t).strip()

    if len(t) <= max_chars:
        return t

    truncated = t[:max_chars].rsplit(' ', 1)[0].strip()
    if len(truncated) < 18:
        truncated = t[:max_chars].strip()

    truncated = truncated.rstrip(" -,/:;|")
    dangling_words = {'avec', 'pour', 'et', 'de', 'du', 'en', 'sur', 'dans', 'with', 'for', 'and'}
    words = truncated.split()
    if words and words[-1].lower() in dangling_words:
        truncated = " ".join(words[:-1]).rstrip(" -,/:;|")

    return truncated or t[:max_chars].strip()

def get_france_deal_dedup_key(product_id: Optional[Any], raw_title: str, msg_id: int) -> str:
    """Builds a unique deduplication key for France deals."""
    if product_id:
        p_clean = str(product_id).strip()
        if p_clean and p_clean.lower() not in ("none", "null", "0", "") and not p_clean.startswith("msg_"):
            return f"pid_{p_clean}"

    t = (raw_title or "").lower()
    t = re.sub(r'[\$€].*$', '', t)
    t = re.sub(r'^[❗️🔖📌🔥🚨⚡💥✨📦🛒🎁📢✅💎💰🔻ـ\s\-:]+', '', t)
    t = re.sub(r'[^\w\s]', ' ', t)
    stop_words = {
        'original', 'global', 'version', 'new', 'hot', 'sale', 'official',
        'free', 'shipping', 'edition', 'bon', 'plan', 'deal'
    }
    tokens = [w for w in t.split() if len(w) > 2 and w not in stop_words]
    if len(tokens) >= 2:
        return "norm_" + "_".join(tokens[:4])
    elif tokens:
        return f"norm_{tokens[0]}"
    return f"msg_{msg_id}"

def is_better_france_deal(candidate: Dict[str, Any], current: Dict[str, Any]) -> bool:
    """Selects the best deal entry between duplicate posts of the same product for France."""
    cand_price = float(candidate.get("price_eur") or 0.0)
    curr_price = float(current.get("price_eur") or 0.0)

    if cand_price > 0 and curr_price > 0:
        if cand_price < curr_price:
            return True
        if curr_price < cand_price:
            return False
    elif cand_price > 0 and curr_price <= 0:
        return True
    elif curr_price > 0 and cand_price <= 0:
        return False

    return int(candidate.get("channel_msg_id") or 0) > int(current.get("channel_msg_id") or 0)

async def get_recent_france_published_deals(max_age_hours: float = 24.0) -> List[Dict[str, Any]]:
    """
    Retrieves deals published to @francedealsdz within the last 24h.
    Merges state deals history and public channel scraping for 100% accuracy.
    Deduplicates identical products posted multiple times during the day.
    """
    state = load_france_state()
    deals_history = state.get("published_deals_history", {})
    now = datetime.now(timezone.utc).timestamp()
    max_age_sec = max_age_hours * 3600.0

    collected: Dict[str, Dict[str, Any]] = {}

    # 1. From state history
    target_clean = TARGET_FRANCE_CHANNEL.replace("@", "")
    for pid, info in deals_history.items():
        msg_id = info.get("channel_msg_id")
        if not msg_id or int(msg_id) <= 0:
            continue
        ts = info.get("timestamp", 0)
        if (now - ts) > max_age_sec:
            continue

        msg_id_int = int(msg_id)
        raw_title = info.get("title", "")
        title = clean_item_title_fr(raw_title)
        price_eur = float(info.get("price_eur") or 0.0)
        category = classify_france_deal_category(raw_title)

        deal_entry = {
            "channel_msg_id": msg_id_int,
            "product_id": pid,
            "title": title,
            "price_eur": price_eur,
            "timestamp": ts,
            "category": category,
            "channel_url": f"https://t.me/{target_clean}/{msg_id_int}"
        }

        dedup_key = get_france_deal_dedup_key(pid, raw_title, msg_id_int)
        if dedup_key not in collected:
            collected[dedup_key] = deal_entry
        else:
            if is_better_france_deal(deal_entry, collected[dedup_key]):
                collected[dedup_key] = deal_entry

    # 2. Complement from channel scraping if state history was sparse
    if len(collected) < 3:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                r = await client.get(f"https://t.me/s/{target_clean}")
                if r.status_code == 200:
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(r.text, "html.parser")
                    blocks = soup.find_all("div", class_="tgme_widget_message")
                    for b in blocks:
                        dp = b.get("data-post", "")
                        if "/" not in dp:
                            continue
                        msg_id_int = int(dp.split("/")[-1])

                        # Check message age
                        time_el = b.find("time")
                        if time_el and time_el.get("datetime"):
                            try:
                                dt = datetime.fromisoformat(time_el["datetime"].replace("Z", "+00:00"))
                                if (datetime.now(timezone.utc) - dt).total_seconds() > max_age_sec:
                                    continue
                            except Exception:
                                pass

                        t_div = b.find("div", class_="tgme_widget_message_text")
                        if not t_div:
                            continue
                        text = t_div.get_text("\n")
                        # Skip roundups or bulletins themselves
                        if "Récapitulatif" in text or "Sélection" in text or "#AliExpressFrance" in text:
                            continue

                        # Extract title and price
                        first_line = ""
                        for line in text.splitlines():
                            l = line.strip()
                            if l.startswith("✅"):
                                first_line = l.replace("✅", "").strip()
                                break
                        if not first_line:
                            for line in text.splitlines():
                                l = line.strip()
                                if l and not l.startswith("🔥") and not l.startswith("<blockquote>") and not l.startswith("🚚"):
                                    first_line = l
                                    break

                        # Extract price
                        m_p = re.search(r'([0-9]+(?:\.[0-9]{1,2})?)\s*€', text)
                        price = float(m_p.group(1)) if m_p else 0.0

                        if first_line and price > 0:
                            title = clean_item_title_fr(first_line)
                            scraped_entry = {
                                "channel_msg_id": msg_id_int,
                                "product_id": f"msg_{msg_id_int}",
                                "title": title,
                                "price_eur": price,
                                "timestamp": now,
                                "category": classify_france_deal_category(first_line, text),
                                "channel_url": f"https://t.me/{target_clean}/{msg_id_int}"
                            }
                            dedup_key = get_france_deal_dedup_key(None, first_line, msg_id_int)
                            if dedup_key not in collected:
                                collected[dedup_key] = scraped_entry
                            else:
                                if is_better_france_deal(scraped_entry, collected[dedup_key]):
                                    collected[dedup_key] = scraped_entry
        except Exception as e:
            logger.warning(f"France channel scraping error: {e}")

    return list(collected.values())

def format_france_deal_line(item: Dict[str, Any], channel_username: str = "francedealsdz") -> str:
    title = item.get("title") or "Bon plan"
    price_val = float(item.get("price_eur") or 0.0)
    price_str = f"<b>{price_val:.2f}€</b>" if price_val > 0 else "<b>Prix réduit</b>"
    clean_ch = channel_username.replace("@", "")
    post_url = item.get("channel_url") or f"https://t.me/{clean_ch}/{item['channel_msg_id']}"
    return f"▫️ <b>{title}</b>\n   💰 Prix : {price_str} ▫️ <a href=\"{post_url}\">Voir le deal ➔</a>\n"

def build_france_category_bulletin(category_name: str, items: List[Dict[str, Any]], channel_username: str = "francedealsdz") -> Tuple[str, List[Dict[str, Any]]]:
    cat_config = CATEGORIES_CONFIG_FR.get(category_name, {
        "header": f"📦 <b>Sélection {category_name} du Jour 🇫🇷🔥</b>"
    })

    header_lines = [
        cat_config["header"],
        "━━━━━━━━━━━━━━━━━"
    ]
    footer_lines = [
        "━━━━━━━━━━━━━━━━━",
        "💡 <i>Cliquez sur (Voir le deal ➔) pour accéder à l'offre sur le canal.</i>",
        "🪙 <b>Réduction pièces (Coins) :</b> @Alilo07BOT",
        "📢 @francedealsdz"
    ]
    footer_text = "\n".join(footer_lines)

    selected_items: List[Dict[str, Any]] = []
    body_lines: List[str] = []

    for item in items:
        line = format_france_deal_line(item, channel_username)
        cand = "\n".join(header_lines + body_lines + [line, footer_text])
        if len(cand) > 980:
            break
        body_lines.append(line)
        selected_items.append(item)

    full_caption = "\n".join(header_lines + body_lines + footer_lines)
    return full_caption, selected_items

classify_deal_category = classify_france_deal_category

def format_france_bulletin(category_name: str, items: List[Dict[str, Any]], channel_username: str = "francedealsdz") -> str:
    caption, _ = build_france_category_bulletin(category_name, items, channel_username)
    return caption

def build_france_master_roundup(deals: List[Dict[str, Any]], channel_username: str) -> Tuple[str, List[Dict[str, Any]]]:
    header_lines = [
        "🌙 <b>Récapitulatif des Meilleurs Bons Plans du Jour 🇫🇷🔥</b>",
        "━━━━━━━━━━━━━━━━━"
    ]
    footer_lines = [
        "━━━━━━━━━━━━━━━━━",
        "💡 <i>Les meilleures offres AliExpress sélectionnées aujourd'hui !</i>",
        "🪙 <b>Réduction pièces (Coins) :</b> @Alilo07BOT",
        "📢 @francedealsdz"
    ]
    footer_text = "\n".join(footer_lines)

    selected_items: List[Dict[str, Any]] = []
    body_lines: List[str] = []

    sorted_deals = sorted(deals, key=lambda x: x.get("price_eur", 0), reverse=True)

    for item in sorted_deals:
        line = format_france_deal_line(item, channel_username)
        cand = "\n".join(header_lines + body_lines + [line, footer_text])
        if len(cand) > 980:
            break
        body_lines.append(line)
        selected_items.append(item)

    full_caption = "\n".join(header_lines + body_lines + footer_lines)
    return full_caption, selected_items

async def check_and_publish_france_regrouped_bulletins(
    force: bool = False,
    min_items: int = 3
) -> List[Dict[str, Any]]:
    """
    Publishes daily roundups to @francedealsdz at ~10 PM CET.
    """
    token = settings.TELEGRAM_BOT_TOKEN
    target = TARGET_FRANCE_CHANNEL
    target_clean = target.replace("@", "")

    if not token:
        logger.warning("[FRANCE ROUNDUP] TELEGRAM_BOT_TOKEN not configured.")
        return []

    # 1. Timing & Idempotency check
    if not force:
        if not is_france_roundup_time_window():
            logger.info("[FRANCE ROUNDUP] Not in 10 PM CET window (21:30 - 23:45). Skipping.")
            return []

        eligible, reason = is_france_roundup_eligible()
        if not eligible:
            logger.info(f"[FRANCE ROUNDUP] Not eligible: {reason}. Skipping.")
            return []

    logger.info("[FRANCE ROUNDUP] Starting daily roundup collection...")
    today_deals = await get_recent_france_published_deals(max_age_hours=24.0)
    if not today_deals or len(today_deals) < 2:
        logger.info("[FRANCE ROUNDUP] Insufficient deals published today (< 2). Skipping.")
        return []

    # Group by category
    by_category: Dict[str, List[Dict[str, Any]]] = {k: [] for k in CATEGORIES_CONFIG_FR.keys()}
    other_deals: List[Dict[str, Any]] = []

    for d in today_deals:
        cat = d.get("category")
        if cat and cat in by_category:
            by_category[cat].append(d)
        else:
            other_deals.append(d)

    bulletins_to_post: List[Tuple[str, str, List[Dict[str, Any]]]] = []

    # Check for category-specific bulletins meeting min_items
    for cat_name, cat_items in by_category.items():
        if len(cat_items) >= min_items:
            caption, selected = build_france_category_bulletin(cat_name, cat_items, target_clean)
            if selected:
                bulletins_to_post.append((cat_name, caption, selected))

    # If no category reached min_items, build a Master Daily Roundup
    if not bulletins_to_post:
        caption, selected = build_france_master_roundup(today_deals, target_clean)
        if selected and len(selected) >= 2:
            bulletins_to_post.append(("master_roundup", caption, selected))

    if not bulletins_to_post:
        logger.info("[FRANCE ROUNDUP] No qualifying bulletins to post.")
        return []

    published_results: List[Dict[str, Any]] = []
    published_msg_ids: List[int] = []

    # Prepare banner image
    banner_path = Path(settings.BASE_DIR) / "storage" / "assets" / "choice_day_banner.png"
    if not banner_path.exists():
        banner_path = Path(settings.BASE_DIR) / "storage" / "assets" / "tajmi3at_banner.png"

    photo_bytes = banner_path.read_bytes() if banner_path.exists() else None

    reply_markup = {
        "inline_keyboard": [
            [{"text": "🛍️ Voir tous les bons plans sur le canal", "url": f"https://t.me/{target_clean}"}],
            [{"text": "🪙 Bot Pièces AliExpress (Coins)", "url": "https://t.me/Alilo07BOT"}]
        ]
    }
    reply_markup_json = json.dumps(reply_markup)

    api_url = f"https://api.telegram.org/bot{token}"

    async with httpx.AsyncClient(timeout=30.0) as client:
        for cat_name, caption, items in bulletins_to_post:
            try:
                if photo_bytes:
                    files = {"photo": ("roundup.png", photo_bytes, "image/png")}
                    data = {
                        "chat_id": target,
                        "caption": caption,
                        "parse_mode": "HTML",
                        "reply_markup": reply_markup_json
                    }
                    resp = await client.post(f"{api_url}/sendPhoto", data=data, files=files)
                else:
                    data = {
                        "chat_id": target,
                        "text": caption,
                        "parse_mode": "HTML",
                        "disable_web_page_preview": True,
                        "reply_markup": reply_markup_json
                    }
                    resp = await client.post(f"{api_url}/sendMessage", data=data)

                if resp.status_code == 200 and resp.json().get("ok"):
                    msg_id = resp.json()["result"]["message_id"]
                    published_msg_ids.append(msg_id)
                    published_results.append({
                        "category": cat_name,
                        "count": len(items),
                        "message_id": msg_id
                    })
                    logger.info(f"[FRANCE ROUNDUP PUBLISHED] {cat_name}: {len(items)} items -> Msg #{msg_id}")
                    await asyncio.sleep(2.0)
                else:
                    logger.error(f"[FRANCE ROUNDUP FAILED] {cat_name}: {resp.status_code} {resp.text}")
            except Exception as e:
                logger.error(f"[FRANCE ROUNDUP EXCEPTION] {cat_name}: {e}")

    if published_results:
        cet = timezone(timedelta(hours=1))
        today_str = datetime.now(cet).strftime("%Y-%m-%d")
        record_france_roundup_published(today_str, len(published_results), published_msg_ids)

    return published_results
