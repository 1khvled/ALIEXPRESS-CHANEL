"""
Central State & Anti-Spam Deduplication Tracker
Prevents any duplicate product, disclaimer, or promo calendar from ever being reposted to @DzAliexpress0.
Integrates triple-layer protection:
1. Committed persistent JSON storage (storage/state/published_state.json)
2. Local database records (deals.db)
3. Live target channel scraping (https://t.me/s/DzAliexpress0)
"""
import os
import json
import time
import re
from datetime import datetime, timezone, timedelta
from typing import Set, List, Dict, Tuple, Optional, Any
import httpx
from bs4 import BeautifulSoup

from app.utils.logger import logger
from app.aliexpress.urls import extract_product_id_from_url

TARGET_CHANNEL_ID = os.getenv("TARGET_CHANNEL_ID", "@DzAliexpress0")
STATE_FILE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "storage", "state", "published_state.json"
)

# In-memory cached channel content to prevent hammering Telegram web
_CACHED_CHANNEL_TEXTS: List[str] = []
_CACHED_CHANNEL_PIDS: Set[str] = set()
_LAST_CHANNEL_SCRAPE_TIME: float = 0.0

def _ensure_state_dir():
    os.makedirs(os.path.dirname(STATE_FILE_PATH), exist_ok=True)

def load_persistent_state() -> Dict:
    _ensure_state_dir()
    if os.path.exists(STATE_FILE_PATH):
        try:
            with open(STATE_FILE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading state file: {e}")
    return {
        "published_product_ids": [],
        "published_titles": [],
        "last_disclaimer_time": 0.0,
        "last_calendar_time": 0.0,
        "last_run_time": 0.0
    }

def save_persistent_state(state: Dict):
    _ensure_state_dir()
    try:
        with open(STATE_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error saving state file: {e}")

def get_monitored_channel_last_id(channel_username: str) -> Optional[int]:
    """Returns the highest telegram message ID seen for this monitored source channel."""
    state = load_persistent_state()
    ch_state = state.get("monitored_channels", {})
    ch_info = ch_state.get(channel_username.lower().lstrip("@"), {})
    return ch_info.get("last_message_id")

def record_monitored_channel_last_id(channel_username: str, last_message_id: int):
    """Saves the highest seen telegram message ID for this monitored channel."""
    state = load_persistent_state()
    if "monitored_channels" not in state:
        state["monitored_channels"] = {}
    ch_key = channel_username.lower().lstrip("@")
    prev = state["monitored_channels"].get(ch_key, {}).get("last_message_id", 0)
    state["monitored_channels"][ch_key] = {
        "last_message_id": max(prev, int(last_message_id)),
        "last_check_time": time.time()
    }
    save_persistent_state(state)


async def refresh_channel_cache(force: bool = False):
    """Scrapes the public preview of @DzAliexpress0 to inspect the actual live channel messages."""
    global _CACHED_CHANNEL_TEXTS, _CACHED_CHANNEL_PIDS, _LAST_CHANNEL_SCRAPE_TIME
    now = time.time()
    if not force and _CACHED_CHANNEL_TEXTS and (now - _LAST_CHANNEL_SCRAPE_TIME < 120):
        return

    clean_ch = str(TARGET_CHANNEL_ID).lstrip("@")
    url = f"https://t.me/s/{clean_ch}"
    try:
        async with httpx.AsyncClient(timeout=12.0, follow_redirects=True) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                blocks = soup.find_all("div", class_="tgme_widget_message")
                texts = []
                pids = set()
                for b in blocks:
                    t_div = b.find("div", class_="tgme_widget_message_text")
                    t = t_div.get_text(separator=" ").strip() if t_div else ""
                    if t:
                        texts.append(t)
                        # Extract product ID if found in text or URLs
                        for u in re.findall(r'https?://[^\s<>"\'\)]+', t):
                            pid = extract_product_id_from_url(u)
                            if pid:
                                pids.add(pid)
                _CACHED_CHANNEL_TEXTS = texts
                _CACHED_CHANNEL_PIDS = pids
                _LAST_CHANNEL_SCRAPE_TIME = now
                logger.info(f"Refreshed live channel cache: {len(_CACHED_CHANNEL_TEXTS)} messages, {len(_CACHED_CHANNEL_PIDS)} product IDs found.")
    except Exception as e:
        logger.warning(f"Could not refresh live channel cache: {e}")

def _clean_title_keywords(title: str) -> List[str]:
    """Extracts distinctive model/product keywords for title-based deduplication."""
    if not title:
        return []
    cleaned = re.sub(r'[\$€\(\)\[\],.;:!?/\\|\-_~+]+', ' ', title.lower())
    stop_words = {'for', 'with', 'and', 'the', 'new', 'hot', 'original', 'inch', 'piece', 'pcs', 'pro', 'max', 'livan', 'auto', 'تخفيض', 'عرض', 'سعر', 'شاحن', 'كابل'}
    words = [w for w in cleaned.split() if len(w) >= 3 and w not in stop_words]
    return words

async def is_product_already_published(product_id: Optional[str], title: str = "") -> Tuple[bool, str]:
    """
    Bulletproof check: Has this product or exact deal already been posted?
    Checks persistent state, database, and live channel messages.
    """
    await refresh_channel_cache()
    state = load_persistent_state()

    # 1. Product ID check in persistent state
    if product_id:
        p_str = str(product_id).strip()
        if p_str in state.get("published_product_ids", []):
            return True, f"Product ID {p_str} already in persistent published state"

        # 2. Product ID check in live channel messages
        if p_str in _CACHED_CHANNEL_PIDS:
            return True, f"Product ID {p_str} is present in live @DzAliexpress0 channel"

    # 3. Title distinctive keyword matching against channel messages
    if title:
        words = _clean_title_keywords(title)
        if len(words) >= 2:
            # Check against previously published titles
            for pub_t in state.get("published_titles", []):
                pub_words = _clean_title_keywords(pub_t)
                common = set(words).intersection(set(pub_words))
                if len(common) >= 3 or (len(words) == 2 and len(common) == 2):
                    return True, f"Title closely matches previously published deal: '{pub_t[:40]}'"

            # Check against live channel texts
            for ch_t in _CACHED_CHANNEL_TEXTS:
                ch_words = _clean_title_keywords(ch_t)
                common = set(words).intersection(set(ch_words))
                if len(common) >= 3:
                    return True, f"Distinctive product keywords {list(common)[:3]} already found in channel post"

    return False, ""

def record_product_published(product_id: Optional[str], title: str = ""):
    """Records a published product into persistent state immediately."""
    state = load_persistent_state()
    changed = False

    if product_id:
        p_str = str(product_id).strip()
        if p_str not in state["published_product_ids"]:
            state["published_product_ids"].append(p_str)
            changed = True

    if title:
        t_clean = title.strip()
        if t_clean not in state["published_titles"]:
            state["published_titles"].append(t_clean)
            changed = True

    state["last_run_time"] = time.time()
    save_persistent_state(state)

async def is_disclaimer_eligible() -> Tuple[bool, str]:
    """Checks if the 14-day region disclaimer can be posted."""
    await refresh_channel_cache()
    state = load_persistent_state()
    now = time.time()
    last_pinned = state.get("last_disclaimer_time", 0.0)

    # 14 days = 14 * 86400 = 1,209,600 seconds
    cooldown_seconds = 14 * 86400
    if (now - last_pinned) < cooldown_seconds:
        days_left = (cooldown_seconds - (now - last_pinned)) / 86400
        return False, f"Disclaimer cooldown active ({days_left:.1f} days remaining)"

    # Live channel text check: is disclaimer already in recent messages?
    for t in _CACHED_CHANNEL_TEXTS:
        if "لماذا يجب تغيير دولة التطبيق" in t or "تغيير دولة التطبيق في AliExpress" in t:
            # Update state so we don't re-check repeatedly
            state["last_disclaimer_time"] = now
            save_persistent_state(state)
            return False, "Disclaimer was recently posted and visible in channel"

    return True, "Disclaimer eligible for posting"

def record_disclaimer_published():
    state = load_persistent_state()
    state["last_disclaimer_time"] = time.time()
    save_persistent_state(state)

async def is_calendar_eligible() -> Tuple[bool, str]:
    """Checks if the promo calendar is eligible for auto-posting (7 days interval)."""
    await refresh_channel_cache()
    state = load_persistent_state()
    now = time.time()
    last_cal = state.get("last_calendar_time", 0.0)

    # 7 days = 7 * 86400 = 604,800 seconds
    cooldown_seconds = 7 * 86400
    if (now - last_cal) < cooldown_seconds:
        days_left = (cooldown_seconds - (now - last_cal)) / 86400
        return False, f"Calendar cooldown active ({days_left:.1f} days remaining)"

    # Live channel check
    for t in _CACHED_CHANNEL_TEXTS:
        if "رزنامة تخفيضات ومهرجانات AliExpress" in t:
            state["last_calendar_time"] = now
            save_persistent_state(state)
            return False, "Calendar already visible in recent channel messages"

    return True, "Calendar eligible for posting"

def record_calendar_published():
    state = load_persistent_state()
    state["last_calendar_time"] = time.time()
    save_persistent_state(state)

async def is_coin_reminder_eligible(min_hours: float = 48.0) -> Tuple[bool, str]:
    """Checks if the educational Coins & PC guide reminder is eligible (randomized 48-72h interval)."""
    await refresh_channel_cache()
    state = load_persistent_state()
    now = time.time()
    last_rem = state.get("last_coin_reminder_time", 0.0)

    jitter_seconds = state.get("next_reminder_interval_seconds", int(min_hours * 3600))
    if (now - last_rem) < jitter_seconds:
        hours_left = (jitter_seconds - (now - last_rem)) / 3600
        return False, f"Coin reminder cooldown active ({hours_left:.1f} hours remaining)"

    if _CACHED_CHANNEL_TEXTS and any(k in _CACHED_CHANNEL_TEXTS[0] for k in ["دليل متسوقي الحاسوب", "اجمع رصيد عملاتك اليومية", "جامع العملات التلقائي"]):
        return False, "Coin reminder was recently posted and at the top of the channel"

    return True, "Coin reminder eligible for posting"

def record_coin_reminder_published():
    import random
    state = load_persistent_state()
    state["last_coin_reminder_time"] = time.time()
    state["next_reminder_interval_seconds"] = random.randint(48 * 3600, 72 * 3600)
    state["coin_reminder_variant_idx"] = (state.get("coin_reminder_variant_idx", 0) + 1) % 3
    save_persistent_state(state)

# ── Dynamic Schedule & Interval Management ──────────────────────
DEFAULT_SCHEDULE_CONFIG = {
    "day_interval_minutes": 5,
    "night_interval_minutes": 30,
    "current_interval_minutes": 5,
    "is_paused": False,
    "night_mode_enabled": True,
    "last_deal_post_time": 0.0,
    "night_start_hour_dz": 0,   # 00:00 Algerian time
    "night_end_hour_dz": 8      # 08:00 Algerian time
}

def get_schedule_config() -> Dict[str, Any]:
    """Loads current schedule configuration with defaults."""
    state = load_persistent_state()
    saved = state.get("schedule_config", {})
    merged = dict(DEFAULT_SCHEDULE_CONFIG)
    merged.update(saved)
    return merged

def update_schedule_config(updates: Dict[str, Any]) -> Dict[str, Any]:
    """Updates and persists schedule configuration."""
    state = load_persistent_state()
    saved = state.get("schedule_config", {})
    merged = dict(DEFAULT_SCHEDULE_CONFIG)
    merged.update(saved)
    merged.update(updates)
    state["schedule_config"] = merged
    save_persistent_state(state)
    logger.info(f"Updated schedule config: {merged}")
    return merged

def is_deal_posting_due() -> Tuple[bool, str, int]:
    """
    Checks if enough time has passed to post a new deal based on:
    - User-configured interval (5m, 10m, 15m, 30m, etc.)
    - Day vs Night mode (automatic 30m after midnight)
    - Pause switch
    Returns: (is_due, reason_message, active_interval_minutes)
    """
    config = get_schedule_config()
    if config.get("is_paused", False):
        return False, "⏸️ النشر التلقائي متوقف مؤقتاً بأمر المدير (Paused)", 0

    now_utc = datetime.now(timezone.utc)
    # Algeria is UTC+1
    algeria_hour = (now_utc.hour + 1) % 24
    is_night = (algeria_hour >= config.get("night_start_hour_dz", 0) and algeria_hour < config.get("night_end_hour_dz", 8))

    if is_night and config.get("night_mode_enabled", True):
        active_interval = config.get("night_interval_minutes", 30)
        mode_desc = f"الوضع الليلي 🌙 ({active_interval} دقيقة)"
    else:
        active_interval = config.get("current_interval_minutes", config.get("day_interval_minutes", 5))
        mode_desc = f"الوضع النهاري ☀️ ({active_interval} دقائق)"

    now_ts = time.time()
    last_post_ts = config.get("last_deal_post_time", 0.0)
    elapsed_seconds = now_ts - last_post_ts
    required_seconds = active_interval * 60

    if last_post_ts > 0 and elapsed_seconds < required_seconds:
        remaining_minutes = (required_seconds - elapsed_seconds) / 60
        return False, f"⏳ في فترة الانتظار: {mode_desc} - متبقي {remaining_minutes:.1f} دقيقة", active_interval

    return True, f"✅ جاهز للنشر: {mode_desc}", active_interval

def record_deal_posted_time():
    """Updates the last_deal_post_time timestamp."""
    state = load_persistent_state()
    if "schedule_config" not in state:
        state["schedule_config"] = dict(DEFAULT_SCHEDULE_CONFIG)
    state["schedule_config"]["last_deal_post_time"] = time.time()
    save_persistent_state(state)


