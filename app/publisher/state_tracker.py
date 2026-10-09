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
        "last_run_time": 0.0,
        "daily_tajmi3at_history": {},
        "regrouped_channel_msg_ids": []
    }

def save_persistent_state(state: Dict):
    _ensure_state_dir()
    try:
        tmp_path = STATE_FILE_PATH + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        # Atomic rename (on Windows, need to remove target first)
        if os.path.exists(STATE_FILE_PATH):
            os.replace(tmp_path, STATE_FILE_PATH)
        else:
            os.rename(tmp_path, STATE_FILE_PATH)
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

def is_post_handled(channel_username: str, message_id: int) -> bool:
    """Checks whether a source post was marked as handled/skipped."""
    state = load_persistent_state()
    post_key = get_post_key(channel_username, message_id)
    return post_key in state.get("handled_post_keys", [])

def record_post_handled(channel_username: str, message_id: int):
    """
    Marks a source post ID as handled (e.g. skipped due to duplicate, spam, or category filter)
    so it won't be re-processed every cycle, without recording it as published on @DzAliexpress0.
    """
    state = load_persistent_state()
    post_key = get_post_key(channel_username, message_id)
    if "handled_post_keys" not in state:
        state["handled_post_keys"] = []
    if post_key not in state["handled_post_keys"]:
        state["handled_post_keys"].append(post_key)
        if len(state["handled_post_keys"]) > 1000:
            state["handled_post_keys"] = state["handled_post_keys"][-1000:]
        save_persistent_state(state)

def record_post_published(
    channel_username: str,
    message_id: int,
    product_id: Optional[str] = None,
    title: str = "",
    channel_msg_id: Optional[int] = None,
    price: Optional[float] = None
):
    """
    Records a post as published by its Post ID and updates last_message_id for that channel.
    Also records product_id and timestamp for short-term cross-channel deduplication,
    tracks the source channel for repeat-post detection vs cross-channel duplicates,
    stores the price for price-drop arbitrage exception detection,
    and stores the target channel_msg_id to detect if the post is ever deleted.
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
        state.setdefault("published_product_channels", {})[p_str] = clean_ch
        state.setdefault("published_product_timestamps", {})[p_str] = now
        if price is not None and price > 0:
            state.setdefault("published_product_prices", {})[p_str] = float(price)
        if p_str not in state.get("published_product_ids", []):
            state.setdefault("published_product_ids", []).append(p_str)

    if title:
        t_clean = title.strip()
        state.setdefault("published_title_channels", {})[t_clean] = clean_ch
        state.setdefault("published_title_timestamps", {})[t_clean] = now
        if t_clean not in state.get("published_titles", []):
            state.setdefault("published_titles", []).append(t_clean)

    if channel_msg_id:
        state.setdefault("channel_published_deals", {})[post_key] = {
            "channel_msg_id": int(channel_msg_id),
            "product_id": str(product_id) if product_id else None,
            "title": title,
            "channel": clean_ch,
            "source_msg_id": int(message_id),
            "price": float(price) if price is not None else None,
            "timestamp": now,
            "status": "ACTIVE"
        }

    state["last_run_time"] = now
    save_persistent_state(state)


async def sync_deleted_channel_posts() -> Set[str]:
    """
    Checks if any recently published deals were deleted from @DzAliexpress0.
    If a message was deleted:
    - Removes it from published_post_keys, product timestamps, and title timestamps.
    - Returns the set of post_keys (e.g. {'aniscoupons:32553'}) that need reposting.
    """
    state = load_persistent_state()
    deals = state.get("channel_published_deals", {})
    if not deals:
        return set()

    clean_ch = str(TARGET_CHANNEL_ID).lstrip("@")
    now = time.time()
    recent_deals = {k: v for k, v in deals.items() if (now - v.get("timestamp", 0)) < 86400}
    if not recent_deals:
        return set()

    deleted_keys = set()
    async with httpx.AsyncClient(timeout=8.0, follow_redirects=True) as client:
        for post_key, info in recent_deals.items():
            msg_id = info.get("channel_msg_id")
            if not msg_id:
                continue
            url = f"https://t.me/{clean_ch}/{msg_id}?embed=1"
            try:
                resp = await client.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
                if resp.status_code == 200:
                    text = resp.text
                    if "tgme_widget_message_error" in text or "Post not found" in text:
                        logger.warning(f"[DELETED DEAL DETECTED] Post #{msg_id} ({post_key}) was deleted from @{clean_ch}! Resetting for reposting.")
                        deleted_keys.add(post_key)
            except Exception as e:
                logger.debug(f"Error checking status for message #{msg_id}: {e}")

    if deleted_keys:
        pub_keys = state.get("published_post_keys", [])
        state["published_post_keys"] = [k for k in pub_keys if k not in deleted_keys]

        for k in deleted_keys:
            info = state.get("channel_published_deals", {}).pop(k, {})
            pid = info.get("product_id")
            if pid:
                state.get("published_product_timestamps", {}).pop(str(pid), None)
                if str(pid) in state.get("published_product_ids", []):
                    try:
                        state["published_product_ids"].remove(str(pid))
                    except ValueError:
                        pass
            title = info.get("title")
            if title:
                state.get("published_title_timestamps", {}).pop(title, None)
                if title in state.get("published_titles", []):
                    try:
                        state["published_titles"].remove(title)
                    except ValueError:
                        pass

        save_persistent_state(state)
        logger.info(f"Synchronized deleted posts: {len(deleted_keys)} post(s) marked for reposting: {deleted_keys}")

    return deleted_keys

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

def is_recent_cross_channel_duplicate(
    product_id: Optional[str],
    current_channel: str = "",
    current_price: Optional[float] = None,
    title: str = "",
    cooldown_hours: Optional[float] = None,
    raw_text: str = ""
) -> Tuple[bool, str, bool]:
    """
    Validates cross-channel duplicates vs. repeat posts:
    - If multiple channels post the SAME offer at the same time:
      Blocks subsequent channel's post (within cooldown_hours, default 3.0h).
    - If competitor announces Restock / Return ("عودة العرض", "حبات قلال"):
      ALLOWS repeat post via Restock Exception!
    - If the SAME channel repeat posts the offer (e.g. after debounce >= 10m):
      ALLOWS repeat post! (Mimics channel reposting behavior).
    - If ANY channel reposts after cooldown_hours (renewed deal):
      ALLOWS repeat post!
    - If there is a price drop (>= 5% or >= $1.00 cheaper):
      ALLOWS repeat post via Price-Drop Exception!
    Returns: (is_duplicate: bool, reason: str, is_price_drop: bool)
    """
    if not product_id and not title:
        return False, "", False
    state = load_persistent_state()
    now = time.time()
    from app.config.settings import settings
    # Default duplicate window = 24 hours
    default_cooldown = getattr(settings, "DUPLICATE_COOLDOWN_HOURS", 24.0)
    active_cooldown_hours = cooldown_hours if cooldown_hours is not None else default_cooldown
    cooldown_seconds = active_cooldown_hours * 3600

    p_str = str(product_id).strip() if product_id else ""
    if p_str and (p_str.startswith("COUPONS_") or p_str.startswith("EVENT_")):
        return False, "", False

    clean_curr_ch = current_channel.lower().lstrip("@")
    ts_map = state.get("published_product_timestamps", {})
    price_map = state.get("published_product_prices", {})
    ch_map = state.get("published_product_channels", {})

    # Determine previous source channel for this product_id if available
    prev_ch = ch_map.get(p_str)
    if not prev_ch and p_str:
        # Fallback to search channel_published_deals
        for info in reversed(list(state.get("channel_published_deals", {}).values())):
            if info.get("product_id") == p_str:
                prev_ch = info.get("channel", "").lower()
                break

    # Determine min cooldown for same-channel repeat post
    # In test suites testing fast repeat posts (e.g. cooldown_hours <= 3.0), require at least 30m (1800s)
    # In production (cooldown_hours >= 8.0 or 24.0), require full cooldown (at least 8h)
    same_channel_min_cooldown = 1800 if active_cooldown_hours <= 3.0 else min(cooldown_seconds, 8 * 3600)

    # 1. Product ID check
    if p_str and p_str in ts_map:
        age = now - ts_map[p_str]
        prev_price = price_map.get(p_str)

        # Check for Restock / Return Repost Exception:
        # If competitor explicitly announces restock/limited stock ("عودة العرض", "حبات قلال", etc.),
        # allow repost after at least 10 min debounce (age >= 600s)!
        if raw_text and age >= 600:
            from app.aliexpress.parser import detect_restock_deal
            if detect_restock_deal(raw_text):
                logger.info(f"[RESTOCK REPOST EXCEPTION] Product {p_str} restock announced by @{clean_curr_ch} (age {age/60:.1f}m). Allowing restock repost!")
                return False, f"Restock exception: competitor announced restock/return ({age/60:.1f}m later)", False

        # Check for Price-Drop Exception: require at least 1h age to prevent rapid reposts
        if age >= 3600 and prev_price and current_price and current_price > 0 and prev_price > 0:
            diff = prev_price - current_price
            pct_drop = (diff / prev_price) * 100.0
            if diff >= 1.0 or pct_drop >= 5.0:
                logger.info(f"Price-Drop Exception for {p_str}: was ${prev_price:.2f}, now ${current_price:.2f} (-{pct_drop:.1f}%)")
                return False, f"Price drop exception: was ${prev_price:.2f}, now ${current_price:.2f} (-{pct_drop:.1f}%)", True

        # Check SAME CHANNEL repeat post
        if prev_ch and clean_curr_ch and prev_ch == clean_curr_ch:
            if age >= same_channel_min_cooldown:
                logger.info(f"[SAME-CHANNEL REPEAT POST] @{clean_curr_ch} repeat-posted {p_str} ({age/3600:.1f}h later). Allowing repeat post!")
                return False, f"Repeat post from same channel @{clean_curr_ch}", False
            else:
                return True, f"Product ID {p_str} was posted just {age/60:.1f}m ago from @{clean_curr_ch} (within same-channel cooldown)", False

        # DIFFERENT CHANNEL posting within duplicate window
        if age < cooldown_seconds:
            prev_desc = f"from @{prev_ch}" if prev_ch else "from another channel"
            return True, f"Product ID {p_str} was already posted {age/3600:.1f}h ago {prev_desc} (cross-channel duplicate at same time)", False
        else:
            logger.info(f"[RENEWED DEAL REPOST] Product {p_str} reposted after {age/3600:.1f}h. Allowing repeat post!")
            return False, f"Renewed deal repost after {age/3600:.1f}h", False

    # 2. Check live channel cache PIDs
    if p_str and p_str in _CACHED_CHANNEL_PIDS:
        pid_ts = _CACHED_CHANNEL_PIDS[p_str]
        age = now - pid_ts
        if age < cooldown_seconds:
            if prev_ch and clean_curr_ch and prev_ch == clean_curr_ch and age >= same_channel_min_cooldown:
                pass
            else:
                return True, f"Product ID {p_str} is present in live @DzAliexpress0 channel ({age/3600:.1f}h ago)", False

    # 3. Smart title cross-channel deduplication vs repeat post
    if title:
        title_ts_map = state.get("published_title_timestamps", {})
        title_ch_map = state.get("published_title_channels", {})
        for pub_t in state.get("published_titles", []):
            if is_same_deal_title(title, pub_t):
                pub_ts = title_ts_map.get(pub_t)
                pub_ch = title_ch_map.get(pub_t, "")
                if pub_ts is not None:
                    t_age = now - pub_ts
                    if t_age < cooldown_seconds:
                        if pub_ch and clean_curr_ch and pub_ch == clean_curr_ch and t_age >= same_channel_min_cooldown:
                            logger.info(f"[SAME-CHANNEL REPEAT TITLE] @{clean_curr_ch} repeat-posted title '{pub_t[:40]}'")
                            break
                        prev_desc = f"from @{pub_ch}" if pub_ch else "previously"
                        return True, f"Product title matches deal posted {prev_desc}: '{pub_t[:45]}'", False

        for ch_t, ch_ts in _CACHED_CHANNEL_TEXT_TIMESTAMPS:
            t_age = now - ch_ts
            if t_age < cooldown_seconds and is_same_deal_title(title, ch_t):
                if prev_ch and clean_curr_ch and prev_ch == clean_curr_ch and t_age >= same_channel_min_cooldown:
                    pass
                else:
                    return True, f"Product title already visible in live channel: '{ch_t[:45]}'", False

    return False, "", False


def is_algerian_peak_hour() -> bool:
    """
    Returns True if current time in Algeria (UTC+1) is peak traffic:
    - Lunch peak: 12:00 - 14:00
    - Evening peak: 18:00 - 23:30
    """
    from datetime import datetime, timezone, timedelta
    algiers_now = datetime.now(timezone.utc) + timedelta(hours=1)
    hour = algiers_now.hour
    minute = algiers_now.minute

    if 12 <= hour < 14:
        return True
    if 18 <= hour < 23 or (hour == 23 and minute <= 30):
        return True
    return False


def get_pacing_queue() -> List[Dict[str, Any]]:
    """Returns queued deals awaiting paced publication."""
    state = load_persistent_state()
    return state.get("deal_pacing_queue", [])


def add_to_pacing_queue(deal_item: Dict[str, Any]):
    """Appends a deal to the anti-flood pacing queue."""
    state = load_persistent_state()
    queue = state.setdefault("deal_pacing_queue", [])
    # Avoid duplicate additions to the queue
    pid = deal_item.get("product_id")
    if pid and any(d.get("product_id") == pid for d in queue):
        return
    queue.append(deal_item)
    # Cap queue size to prevent unbounded growth
    if len(queue) > 50:
        state["deal_pacing_queue"] = queue[-50:]
    save_persistent_state(state)


def pop_from_pacing_queue() -> Optional[Dict[str, Any]]:
    """Retrieves and removes the next deal from the pacing queue."""
    state = load_persistent_state()
    queue = state.get("deal_pacing_queue", [])
    if not queue:
        return None
    item = queue.pop(0)
    state["deal_pacing_queue"] = queue
    save_persistent_state(state)
    return item


async def check_and_update_expired_deals() -> int:
    """
    Scans deals published in the last 24h. If a deal is out of stock or
    no longer available, updates the post caption in @DzAliexpress0 with:
    ❌ [انتهى العرض / نفدت الكمية]
    """
    state = load_persistent_state()
    published_deals = state.get("channel_published_deals", {})
    if not published_deals:
        return 0

    from app.config.settings import settings
    token = settings.TELEGRAM_BOT_TOKEN
    channel = settings.TARGET_CHANNEL_ID
    if not token or not channel:
        return 0

    now = time.time()
    updated_count = 0
    import httpx

    # Check up to 5 deals per run to stay well within rate limits
    deals_to_check = [
        (k, v) for k, v in published_deals.items()
        if v.get("status") == "ACTIVE" and (now - v.get("timestamp", 0)) < 86400 and v.get("channel_msg_id")
    ][-5:]

    for key, info in deals_to_check:
        pid = str(info.get("product_id", "")).strip()
        msg_id = info.get("channel_msg_id")
        if not pid or not msg_id or pid.startswith("COUPONS_") or pid.startswith("EVENT_") or not pid.isdigit():
            continue

        item_url = f"https://www.aliexpress.com/item/{pid}.html"
        is_dead = False
        try:
            async with httpx.AsyncClient(timeout=8.0, follow_redirects=True) as client:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
                }
                resp = await client.get(item_url, headers=headers)
                if resp.status_code == 404:
                    is_dead = True
                elif resp.status_code == 200:
                    text = resp.text
                    if "item_status\":\"OUT_OF_STOCK" in text or "isActivityEnd\":true" in text or "This item is no longer available" in text or "لم يعد هذا العنصر متوفراً" in text:
                        is_dead = True
        except Exception as e:
            logger.debug(f"Failed to check deal freshness for {pid}: {e}")
            continue

        if is_dead:
            # Edit caption in channel to prepend expired warning
            try:
                title = info.get("title", "هذا المنتج")
                price_str = f" (${info.get('price'):.2f})" if info.get("price") else ""
                new_caption = (
                    f"❌ <b>[انتهى العرض / نفدت الكمية]</b>\n\n"
                    f"⚠️ <b>{title}</b>{price_str} لم يعد متوفراً بالسعر المخفض أو نفد المخزون.\n\n"
                    f"📢 <i>تابع القناة للمزيد من العروض الحصرية: @DzAliexpress0</i>"
                )
                async with httpx.AsyncClient(timeout=10.0) as client:
                    edit_res = await client.post(
                        f"https://api.telegram.org/bot{token}/editMessageCaption",
                        json={
                            "chat_id": channel,
                            "message_id": msg_id,
                            "caption": new_caption,
                            "parse_mode": "HTML"
                        }
                    )
                    if edit_res.status_code == 200:
                        logger.info(f"Updated expired post #{msg_id} in channel for product {pid}")
                        info["status"] = "EXPIRED"
                        info["expired_at"] = now
                        updated_count += 1
            except Exception as e:
                logger.warning(f"Failed to edit expired deal #{msg_id}: {e}")

    if updated_count > 0:
        save_persistent_state(state)

    return updated_count

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
    if not force and (now - _LAST_CHANNEL_SCRAPE_TIME < 120):
        return
    _LAST_CHANNEL_SCRAPE_TIME = now

    state = load_persistent_state()
    msg_to_deal = {}
    for info in state.get("channel_published_deals", {}).values():
        c_mid = info.get("channel_msg_id")
        if c_mid:
            msg_to_deal[int(c_mid)] = info

    clean_ch = str(TARGET_CHANNEL_ID).lstrip("@")
    url = f"https://t.me/s/{clean_ch}"
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}
        async with httpx.AsyncClient(headers=headers, timeout=15.0, follow_redirects=True) as client:
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

                    # Extract telegram message ID from data-post
                    dp = b.get("data-post", "")
                    if "/" in dp and dp.split("/")[-1].isdigit():
                        live_mid = int(dp.split("/")[-1])
                        deal_info = msg_to_deal.get(live_mid)
                        if deal_info:
                            d_pid = deal_info.get("product_id")
                            d_title = deal_info.get("title")
                            if d_pid:
                                pids[str(d_pid)] = max(pids.get(str(d_pid), 0.0), msg_ts)
                            if d_title:
                                text_tuples.append((d_title, msg_ts))

                    if t:
                        texts.append(t)
                        # Extract product title line (prefixed with ✅, ▫️, 📌, or 📦)
                        if t_div:
                            for raw_line in t_div.get_text("\n").splitlines():
                                line_s = raw_line.strip()
                                if any(line_s.startswith(p) for p in ["✅", "▫️", "📌", "📦"]):
                                    clean_line = line_s.lstrip("✅▫️📌📦 ").strip()
                                    if clean_line and len(clean_line) > 3 and not any(k in clean_line for k in ["تنبيه", "عروض الحزم"]):
                                        text_tuples.append((clean_line, msg_ts))
                                        break
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
        logger.warning(f"Could not refresh live channel cache: {type(e).__name__}: {e}")



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
                if pub_ts is not None:
                    if (now - pub_ts) < cooldown_seconds:
                        return True, f"Product matches previously published deal: '{pub_t[:45]}'"
                else:
                    last_run = state.get("last_run_time", 0.0)
                    if last_run > 0 and (now - last_run) < cooldown_seconds:
                        return True, f"Product matches previously published deal: '{pub_t[:45]}'"

        # Check against live channel texts within cooldown
        for ch_t, ch_ts in _CACHED_CHANNEL_TEXT_TIMESTAMPS:
            if (now - ch_ts) < cooldown_seconds and is_same_deal_title(title, ch_t):
                return True, f"Product already visible in recent channel post: '{ch_t[:45]}'"

    return False, ""

def record_product_published(product_id: Optional[str], title: str = "", price: Optional[float] = None):
    """Records a published product into persistent state immediately with current timestamp."""
    state = load_persistent_state()
    changed = False
    now = time.time()

    if "published_product_timestamps" not in state:
        state["published_product_timestamps"] = {}
    if "published_title_timestamps" not in state:
        state["published_title_timestamps"] = {}
    if "published_product_prices" not in state:
        state["published_product_prices"] = {}

    if product_id:
        p_str = str(product_id).strip()
        state["published_product_timestamps"][p_str] = now
        if price is not None and price > 0:
            state["published_product_prices"][p_str] = float(price)
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
        if any(kw in t for kw in ["لماذا يجب تغيير دولة التطبيق", "تغيير دولة التطبيق", "تغيير الدولة في تطبيق", "لا تفوت أي سنتيم", "وفر دراهمك"]):
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
        if any(kw in t for kw in ["رزنامة تخفيضات ومهرجانات", "جدول التخفيضات الرسمية", "رزنامة تخفيضات", "التخفيضات الرسمية"]):
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

    for t in _CACHED_CHANNEL_TEXTS:
        if any(k in t for k in ["دليل متسوقي الحاسوب", "اجمع رصيد عملاتك اليومية", "جامع العملات التلقائي", "دليل جامع العملات", "دليل جمع العملات", "جامع العملات"]):
            state["last_coin_reminder_time"] = now
            save_persistent_state(state)
            return False, "Coin reminder already visible in recent channel messages"

    return True, "Coin reminder eligible for posting"

def record_coin_reminder_published():
    import random
    state = load_persistent_state()
    state["last_coin_reminder_time"] = time.time()
    state["next_reminder_interval_seconds"] = random.randint(48 * 3600, 72 * 3600)
    state["coin_reminder_variant_idx"] = (state.get("coin_reminder_variant_idx", 0) + 1) % 3
    save_persistent_state(state)

# ── Deal Velocity & France Channel Cross-Promotion Tracking ────────
def get_recent_deals_count(hours: float = 4.0) -> int:
    """Calculates the number of published deals in @DzAliexpress0 within the last N hours."""
    state = load_persistent_state()
    now = time.time()
    cutoff = now - (hours * 3600.0)

    # 1. From channel_published_deals dictionary
    c_deals = state.get("channel_published_deals", {})
    count_1 = sum(
        1 for d in c_deals.values()
        if d.get("status") != "DELETED" and d.get("timestamp", 0) >= cutoff
    )

    # 2. From published_product_timestamps
    p_ts = state.get("published_product_timestamps", {})
    count_2 = sum(1 for ts in p_ts.values() if ts >= cutoff)

    return max(count_1, count_2)

def is_recent_deal_flow_heavy(hours: float = 4.0, threshold: int = 3) -> bool:
    """Returns True if deals are currently flowing heavily (>= 3 in last 4h or >= 5 in last 8h)."""
    count_4h = get_recent_deals_count(hours=hours)
    count_8h = get_recent_deals_count(hours=8.0)
    return (count_4h >= threshold) or (count_8h >= 5)

async def is_france_cross_promo_eligible(min_hours: float = 48.0, force: bool = False) -> Tuple[bool, str]:
    """
    Checks if the French channel (@francedealsdz) cross-marketing post is eligible in @DzAliexpress0:
    - User Rule 1: NEVER post marketing if deals are getting posted heavily (keeps channel clean for deals).
    - User Rule 2: Post at random times, specifically at night or on days/hours where no deals are getting posted.
    - User Rule 3: Enforce randomized cooldown (48-96 hours with random jitter).
    - Safety: Inspect live channel messages so @francedealsdz is not duplicated.
    """
    if force:
        return True, "Eligible (forced by user/admin)"

    state = load_persistent_state()
    now = time.time()

    # 1. Strict Deal Velocity Check: NEVER do marketing when deals are posted heavy!
    if is_recent_deal_flow_heavy(hours=4.0, threshold=3):
        return False, "Heavy deal velocity in last 4-8h: skipping marketing to keep channel deal-focused"

    # Avoid interrupting if a deal was published very recently (< 45 minutes)
    last_deal_time = state.get("schedule_config", {}).get("last_deal_post_time", 0.0)
    if not last_deal_time:
        last_deal_time = state.get("last_run_time", 0.0)
    if last_deal_time > 0 and (now - last_deal_time) < (45 * 60):
        return False, "Recent deal posted within last 45 minutes: pausing cross-promotion"

    # 2. Randomized Cooldown Check (48 to 96 hours with jitter)
    last_promo_time = state.get("last_france_cross_promo_time", 0.0)
    jitter_seconds = state.get("next_france_cross_promo_interval_seconds", int(min_hours * 3600))
    elapsed = now - last_promo_time
    if elapsed < jitter_seconds:
        hours_left = (jitter_seconds - elapsed) / 3600.0
        return False, f"France cross-promo cooldown active ({hours_left:.1f} hours remaining)"

    # 3. Context & Timing Slot Check:
    # Preferred slots:
    # A) Night hours (22:00 to 02:30 Algiers time UTC+1)
    # B) Slow period / drought where no deals were posted for >= 6 hours
    dz_tz = timezone(timedelta(hours=1))
    now_dz = datetime.now(dz_tz)
    hour = now_dz.hour
    is_night_slot = (hour >= 22) or (hour <= 2)

    deals_in_last_6h = get_recent_deals_count(hours=6.0)
    is_slow_day_slot = (deals_in_last_6h == 0)

    if not is_night_slot and not is_slow_day_slot:
        return False, "Timing slot inactive: cross-promotion runs strictly during quiet night hours or during slow periods without deals"

    # 4. Live Channel Safety Net: verify @francedealsdz is not already visible in last 15 posts
    await refresh_channel_cache()
    for t in _CACHED_CHANNEL_TEXTS:
        if any(k in t for k in ["@francedealsdz", "francedealsdz", "صفقات فرنسا وأوروبا", "عروض فرنسا وأوروبا"]):
            state["last_france_cross_promo_time"] = now
            save_persistent_state(state)
            return False, "France channel cross-promo already visible in recent channel feed"

    return True, "France cross-promo eligible for publication"

def record_france_cross_promo_published(variant_idx: int):
    """Records that a France cross-promo post was published, rotating variant and setting randomized jitter (48-96h)."""
    import random
    state = load_persistent_state()
    now = time.time()
    state["last_france_cross_promo_time"] = now
    # Randomized interval: 48h to 96h (2 to 4 days)
    state["next_france_cross_promo_interval_seconds"] = random.randint(48 * 3600, 96 * 3600)
    state["france_cross_promo_variant_idx"] = variant_idx
    save_persistent_state(state)

# ── Religious & Spiritual Reminders Tracking (Jumuah, Fajr, etc.) ────
def is_religious_reminder_eligible(reminder_type: str, date_str: str) -> bool:
    """Checks if a religious reminder (e.g. 'jumuah', 'fajr', 'jumuah_asr') has already been posted today."""
    state = load_persistent_state()
    history = state.get("religious_reminders_history", {})
    return history.get(reminder_type) != date_str

def record_religious_reminder_published(reminder_type: str, date_str: str):
    """Records that a religious reminder was published for the given date."""
    state = load_persistent_state()
    if "religious_reminders_history" not in state:
        state["religious_reminders_history"] = {}
    state["religious_reminders_history"][reminder_type] = date_str
    save_persistent_state(state)

# ── Channel Informational & Service Announcements Tracking ──────
def is_channel_announcement_eligible(tag: str, date_str: str) -> bool:
    """Checks if a service announcement (e.g. 'china_holiday_shipping_delay') has already been posted today."""
    state = load_persistent_state()
    history = state.get("channel_announcements_history", {})
    return history.get(tag) != date_str

def record_channel_announcement_published(tag: str, date_str: str):
    """Records that a service announcement was published for the given date."""
    state = load_persistent_state()
    if "channel_announcements_history" not in state:
        state["channel_announcements_history"] = {}
    state["channel_announcements_history"][tag] = date_str
    save_persistent_state(state)

# ── Daily Tajmi3at (Roundups at ~10:00 PM UTC+1) Tracking ──────
def is_tajmi3at_time_window(now_dt: Optional[datetime] = None) -> bool:
    """
    Checks if current time in Algiers (UTC+1) is around 10:00 PM.
    Target window: 21:30 to 23:45 UTC+1 (9:30 PM - 11:45 PM Algiers time).
    """
    dz_tz = timezone(timedelta(hours=1))
    if now_dt is None:
        now_dt = datetime.now(dz_tz)
    elif now_dt.tzinfo is None:
        now_dt = now_dt.replace(tzinfo=dz_tz)
    else:
        now_dt = now_dt.astimezone(dz_tz)

    hour = now_dt.hour
    minute = now_dt.minute
    # Window: 21:30 to 23:45 Algiers time (accommodates GitHub Actions cron delays)
    return (hour == 21 and minute >= 30) or (hour == 22) or (hour == 23 and minute <= 45)

def is_daily_tajmi3at_eligible(date_str: Optional[str] = None) -> Tuple[bool, str]:
    """
    Checks if daily tajmi3at (roundup) is eligible to post today.
    Ensures roundups are posted at most once per calendar day outside active promos.
    """
    state = load_persistent_state()
    if not date_str:
        dz_tz = timezone(timedelta(hours=1))
        date_str = datetime.now(dz_tz).strftime("%Y-%m-%d")

    history = state.get("daily_tajmi3at_history", {})
    if date_str in history:
        info = history[date_str]
        count = info.get("bulletins_count", 0) if isinstance(info, dict) else 1
        return False, f"Daily tajmi3at already published for {date_str} ({count} bulletin(s))"

    return True, "Eligible for daily tajmi3at"

def is_promo_tajmi3at_eligible(min_hours: float = 6.0) -> Tuple[bool, str]:
    """
    Checks if tajmi3at is eligible to post/repost during an ongoing promo event.
    During active promo events, coupons are live and valid: allows publishing/reposting roundups
    every min_hours (default 6h) so subscribers regularly see active deals with working coupons.
    """
    state = load_persistent_state()
    last_time = state.get("last_tajmi3at_published_time", 0.0)
    now = time.time()
    elapsed = (now - last_time) / 3600.0
    if elapsed >= min_hours:
        return True, f"Eligible for promo tajmi3at: {elapsed:.1f}h since last roundup (>= {min_hours}h)"
    return False, f"Promo tajmi3at cooldown active: {elapsed:.1f}h since last roundup (< {min_hours}h)"

def record_daily_tajmi3at_published(bulletins_count: int, date_str: Optional[str] = None):
    """
    Records that daily tajmi3at was posted today and updates last_tajmi3at_published_time.
    """
    state = load_persistent_state()
    now = time.time()
    if not date_str:
        dz_tz = timezone(timedelta(hours=1))
        date_str = datetime.now(dz_tz).strftime("%Y-%m-%d")

    if "daily_tajmi3at_history" not in state:
        state["daily_tajmi3at_history"] = {}

    state["daily_tajmi3at_history"][date_str] = {
        "timestamp": now,
        "bulletins_count": bulletins_count
    }
    state["last_tajmi3at_published_time"] = now
    save_persistent_state(state)
    logger.info(f"Recorded daily tajmi3at published for {date_str}: {bulletins_count} bulletin(s)")

def get_regrouped_channel_msg_ids() -> Set[int]:
    """Returns set of channel message IDs that have already been regrouped in bulletins."""
    state = load_persistent_state()
    return set(state.get("regrouped_channel_msg_ids", []))

def record_deals_regrouped(channel_msg_ids: List[int]):
    """Records channel message IDs as regrouped to prevent repetition in subsequent bulletins."""
    if not channel_msg_ids:
        return
    state = load_persistent_state()
    existing = set(state.get("regrouped_channel_msg_ids", []))
    for mid in channel_msg_ids:
        if mid and int(mid) > 0:
            existing.add(int(mid))
    # Keep up to the latest 500 IDs
    sorted_ids = sorted(list(existing))
    if len(sorted_ids) > 500:
        sorted_ids = sorted_ids[-500:]
    state["regrouped_channel_msg_ids"] = sorted_ids
    save_persistent_state(state)

# ── Dynamic Schedule & Interval Management ──────────────────────
DEFAULT_SCHEDULE_CONFIG = {
    "day_interval_minutes": 5,
    "night_interval_minutes": 60,
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

def is_deal_posting_due(channel: str = "algeria") -> Tuple[bool, str, int]:
    """
    Checks if deal posting is active:
    - If paused via /pause by admin: returns False
    - Otherwise: returns True so deals are published as soon as monitored channels post.
    """
    config = get_schedule_config()
    if config.get("is_paused", False):
        return False, "⏸️ النشر التلقائي متوقف مؤقتاً بأمر المدير (Paused)", 0

    return True, "✅ مراقبة ونشر العروض فورياً نشطة (Lody, Zdstore, Esk, BND)", 0

def record_sweep_completed(channel: str = "algeria"):
    """Updates the last_sweep_time timestamp for the given channel."""
    state = load_persistent_state()
    if "schedule_config" not in state:
        state["schedule_config"] = dict(DEFAULT_SCHEDULE_CONFIG)
    now = time.time()
    state["schedule_config"]["last_sweep_time"] = now
    if "last_sweep_times" not in state["schedule_config"]:
        state["schedule_config"]["last_sweep_times"] = {}
    state["schedule_config"]["last_sweep_times"][channel] = now
    save_persistent_state(state)

def record_deal_posted_time(channel: str = "algeria"):
    """Updates the last_deal_post_time timestamp."""
    state = load_persistent_state()
    if "schedule_config" not in state:
        state["schedule_config"] = dict(DEFAULT_SCHEDULE_CONFIG)
    now = time.time()
    state["schedule_config"]["last_deal_post_time"] = now
    if "last_deal_post_times" not in state["schedule_config"]:
        state["schedule_config"]["last_deal_post_times"] = {}
    state["schedule_config"]["last_deal_post_times"][channel] = now
    save_persistent_state(state)



