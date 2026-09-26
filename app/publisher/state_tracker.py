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
_CACHED_CHANNEL_TEXT_TIMESTAMPS: List[Tuple[str, float]] = []
_CACHED_CHANNEL_PIDS: Dict[str, float] = {}
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
        "published_product_timestamps": {},
        "published_titles": [],
        "published_title_timestamps": {},
        "published_post_keys": [],
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

def get_post_key(channel_username: str, message_id: int) -> str:
    clean_ch = channel_username.lower().lstrip("@")
    return f"{clean_ch}:{message_id}"

def is_post_already_published(channel_username: str, message_id: int) -> bool:
    """
    Validates by Telegram Post ID: has this post already been published?
    Ensures we post what channels post, but never repeat the same post.
    """
    state = load_persistent_state()
    post_key = get_post_key(channel_username, message_id)
    seen_posts = state.get("published_post_keys", [])
    return post_key in seen_posts

def record_post_published(channel_username: str, message_id: int, product_id: Optional[str] = None, title: str = ""):
    """
    Records a post as published by its Post ID and updates last_message_id for that channel.
    Also records product_id and timestamp for short-term cross-channel deduplication.
    """
    state = load_persistent_state()
    post_key = get_post_key(channel_username, message_id)
    now = time.time()

    if "published_post_keys" not in state:
        state["published_post_keys"] = []
    if post_key not in state["published_post_keys"]:
        state["published_post_keys"].append(post_key)

    # Keep published_post_keys within reasonable bounds
    if len(state["published_post_keys"]) > 1000:
        state["published_post_keys"] = state["published_post_keys"][-1000:]

    clean_ch = channel_username.lower().lstrip("@")
    if "monitored_channels" not in state:
        state["monitored_channels"] = {}
    prev = state["monitored_channels"].get(clean_ch, {}).get("last_message_id", 0)
    state["monitored_channels"][clean_ch] = {
        "last_message_id": max(prev, int(message_id)),
        "last_check_time": now
    }

    if product_id:
        p_str = str(product_id).strip()
        state.setdefault("published_product_timestamps", {})[p_str] = now
        if p_str not in state.get("published_product_ids", []):
            state.setdefault("published_product_ids", []).append(p_str)

    if title:
        t_clean = title.strip()
        state.setdefault("published_title_timestamps", {})[t_clean] = now
        if t_clean not in state.get("published_titles", []):
            state.setdefault("published_titles", []).append(t_clean)

    state["last_run_time"] = now
    save_persistent_state(state)

def is_recent_cross_channel_duplicate(product_id: Optional[str], current_channel: str = "") -> Tuple[bool, str]:
    """
    Validates cross-channel duplicates:
    If another channel posted this exact AliExpress product today (within 24h), skip it.
    Does NOT do fuzzy title matching so different products of the same brand are never blocked.
    """
    if not product_id:
        return False, ""
    state = load_persistent_state()
    now = time.time()
    from app.config.settings import settings
    cooldown_seconds = getattr(settings, "DUPLICATE_COOLDOWN_HOURS", 24) * 3600

    p_str = str(product_id).strip()
    ts_map = state.get("published_product_timestamps", {})
    if p_str in ts_map:
        age = now - ts_map[p_str]
        if age < cooldown_seconds:
            return True, f"Product ID {p_str} was already posted {age/3600:.1f}h ago from another channel"

    return False, ""

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
    global _CACHED_CHANNEL_TEXTS, _CACHED_CHANNEL_TEXT_TIMESTAMPS, _CACHED_CHANNEL_PIDS, _LAST_CHANNEL_SCRAPE_TIME
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
                text_tuples = []
                pids = {}
                for b in blocks:
                    t_div = b.find("div", class_="tgme_widget_message_text")
                    t = t_div.get_text(separator=" ").strip() if t_div else ""
                    msg_ts = now
                    time_el = b.find("time")
                    if time_el and time_el.get("datetime"):
                        try:
                            msg_dt = datetime.fromisoformat(time_el["datetime"].replace("Z", "+00:00"))
                            msg_ts = msg_dt.timestamp()
                        except Exception:
                            pass
                    if t:
                        texts.append(t)
                        text_tuples.append((t, msg_ts))
                        # Extract product ID if found in text or URLs
                        for u in re.findall(r'https?://[^\s<>"\'\)]+', t):
                            pid = extract_product_id_from_url(u)
                            if pid:
                                pids[pid] = max(pids.get(pid, 0.0), msg_ts)
                _CACHED_CHANNEL_TEXTS = texts
                _CACHED_CHANNEL_TEXT_TIMESTAMPS = text_tuples
                _CACHED_CHANNEL_PIDS = pids
                _LAST_CHANNEL_SCRAPE_TIME = now
                logger.info(f"Refreshed live channel cache: {len(_CACHED_CHANNEL_TEXTS)} messages, {len(_CACHED_CHANNEL_PIDS)} product IDs found.")
    except Exception as e:
        logger.warning(f"Could not refresh live channel cache: {e}")

STOP_WORDS = {
    'for', 'with', 'and', 'the', 'new', 'hot', 'original', 'inch', 'piece', 'pcs',
    'livan', 'auto', 'تخفيض', 'عرض', 'سعر', 'شاحن', 'كابل', 'نسخة', 'جيغا', 'جيجا',
    'global', 'version', 'sale', 'brand', 'deals', 'deal', 'official', 'store',
    'الشراء', 'الطلب', 'رابط', 'خصم', 'عملات', 'كوبون'
}

def extract_title_tokens(title: str) -> Set[str]:
    """Extracts distinctive model/product tokens, preserving alphanumeric codes (e.g. p3, x3, 5g, 8k, r1)."""
    if not title:
        return set()
    cleaned = re.sub(r'[\$€\(\)\[\],.;:!?/\\|\-_~+]+', ' ', title.lower())
    tokens = set()
    for w in cleaned.split():
        if w in STOP_WORDS:
            continue
        # Keep words of len >= 3 OR words containing digits (e.g. p3, x3, 5g, 8k, r1)
        if len(w) >= 3 or any(c.isdigit() for c in w):
            tokens.add(w)
    return tokens

SPEC_TOKENS = {'5g', '4g', '8k', '4k', '120hz', '144hz', '165hz', '240hz', '128', '256', '512', '64', '32', '16', '8', '6', '12'}

def extract_model_identifiers(tokens: Set[str]) -> Set[str]:
    """Finds product model identifiers like r1, x3, p3, ak820, f6, gt, hy300."""
    return {t for t in tokens if any(c.isdigit() for c in t) and t not in SPEC_TOKENS}

def is_same_deal_title(title_a: str, title_b: str) -> bool:
    """Accurately identifies if two titles refer to the same product across different channels."""
    toks_a = extract_title_tokens(title_a)
    toks_b = extract_title_tokens(title_b)
    if not toks_a or not toks_b:
        return False

    # Check distinct model codes (e.g. Attack Shark R1 vs Attack Shark X3)
    models_a = extract_model_identifiers(toks_a)
    models_b = extract_model_identifiers(toks_b)
    if models_a and models_b and not models_a.intersection(models_b):
        return False

    # Check product category mismatch (e.g. realme phone vs realme pad)
    if ("pad" in toks_a and "pad" not in toks_b) or ("pad" in toks_b and "pad" not in toks_a):
        return False

    common = toks_a.intersection(toks_b)

    # 1. 3+ common distinctive keywords (e.g. "attack", "shark", "x3")
    if len(common) >= 3:
        return True

    # 2. 2 core keywords (e.g. "realme", "p3")
    if len(common) >= 2:
        min_len = min(len(toks_a), len(toks_b))
        if len(common) / min_len >= 0.5:
            return True

    return False

def _clean_title_keywords(title: str) -> List[str]:
    """Backwards-compatible wrapper returning token list."""
    return list(extract_title_tokens(title))

async def is_product_already_published(product_id: Optional[str], title: str = "") -> Tuple[bool, str]:
    """
    Bulletproof check: Has this product or exact deal already been posted within the cooldown period?
    Checks persistent state, database, and live channel messages against DUPLICATE_COOLDOWN_HOURS (default 24h).
    Prevents cross-channel duplicate deals from being republished within 24h,
    while allowing legitimate new broadcasts of products after cooldown.
    """
    await refresh_channel_cache()
    state = load_persistent_state()
    now = time.time()
    from app.config.settings import settings
    cooldown_seconds = getattr(settings, "DUPLICATE_COOLDOWN_HOURS", 24) * 3600

    # 1. Product ID check in persistent state
    if product_id:
        p_str = str(product_id).strip()
        ts_map = state.get("published_product_timestamps", {})
        if p_str in ts_map:
            age = now - ts_map[p_str]
            if age < cooldown_seconds:
                return True, f"Product ID {p_str} already in persistent published state ({age/3600:.1f}h ago)"
        elif p_str in state.get("published_product_ids", []):
            # Legacy entry without timestamp: check DB for actual published date
            try:
                from app.db.session import db_context
                from app.db.models import Deal
                from sqlalchemy import select
                async with db_context() as s:
                    db_created = (await s.execute(
                        select(Deal.created_at).where(Deal.product_id == p_str, Deal.status == "PUBLISHED").order_by(Deal.created_at.desc()).limit(1)
                    )).scalar_one_or_none()
                    if db_created:
                        age = (datetime.now(timezone.utc) - db_created).total_seconds()
                        if age < cooldown_seconds:
                            return True, f"Product ID {p_str} already in persistent published state ({age/3600:.1f}h ago)"
                    else:
                        last_run = state.get("last_run_time", 0.0)
                        if (now - last_run) < cooldown_seconds:
                            return True, f"Product ID {p_str} already in persistent published state"
            except Exception:
                return True, f"Product ID {p_str} already in persistent published state"

        # 2. Product ID check in live channel messages
        if p_str in _CACHED_CHANNEL_PIDS:
            pid_ts = _CACHED_CHANNEL_PIDS[p_str]
            if (now - pid_ts) < cooldown_seconds:
                return True, f"Product ID {p_str} is present in live @DzAliexpress0 channel"

        # 3. Check database (deals.db) within cooldown window
        try:
            from app.db.session import db_context
            from app.db.models import Deal
            from sqlalchemy import select
            cooldown_cutoff = datetime.now(timezone.utc) - timedelta(seconds=cooldown_seconds)
            async with db_context() as s:
                db_deal = (await s.execute(
                    select(Deal.id).where(
                        Deal.product_id == p_str,
                        Deal.status == "PUBLISHED",
                        Deal.created_at >= cooldown_cutoff
                    ).limit(1)
                )).scalar_one_or_none()
                if db_deal:
                    return True, f"Product ID {p_str} already published in database within last {settings.DUPLICATE_COOLDOWN_HOURS}h (Deal #{db_deal})"
        except Exception:
            pass

    # 4. Smart Title cross-channel matching
    if title:
        title_ts_map = state.get("published_title_timestamps", {})
        # Check against previously published titles
        for pub_t in state.get("published_titles", []):
            if is_same_deal_title(title, pub_t):
                pub_ts = title_ts_map.get(pub_t)
                if pub_ts is None or (now - pub_ts) < cooldown_seconds:
                    return True, f"Product matches previously published deal: '{pub_t[:45]}'"

        # Check against live channel texts within cooldown
        for ch_t, ch_ts in _CACHED_CHANNEL_TEXT_TIMESTAMPS:
            if (now - ch_ts) < cooldown_seconds and is_same_deal_title(title, ch_t):
                return True, f"Product already visible in recent channel post: '{ch_t[:45]}'"

    return False, ""

def record_product_published(product_id: Optional[str], title: str = ""):
    """Records a published product into persistent state immediately with current timestamp."""
    state = load_persistent_state()
    changed = False
    now = time.time()

    if "published_product_timestamps" not in state:
        state["published_product_timestamps"] = {}
    if "published_title_timestamps" not in state:
        state["published_title_timestamps"] = {}

    if product_id:
        p_str = str(product_id).strip()
        state["published_product_timestamps"][p_str] = now
        if p_str not in state.get("published_product_ids", []):
            state.setdefault("published_product_ids", []).append(p_str)
        changed = True

    if title:
        t_clean = title.strip()
        state["published_title_timestamps"][t_clean] = now
        if t_clean not in state.get("published_titles", []):
            state.setdefault("published_titles", []).append(t_clean)
        changed = True

    state["last_run_time"] = now
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


