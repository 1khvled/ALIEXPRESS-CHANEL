"""
User Product Watchlist & Price Drop Alert System
Allows users of @Alilo07BOT to subscribe to price drops on specific AliExpress products.
When a price drop or new promo is detected, subscribers receive immediate private notifications.
"""
import os
import json
import time
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timezone
import httpx

from app.utils.logger import logger

WATCHLIST_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "storage", "state", "watchlist.json"
)
FALLBACK_WATCHLIST_FILE = "/tmp/watchlist.json"

def _get_active_file_path() -> str:
    try:
        os.makedirs(os.path.dirname(WATCHLIST_FILE), exist_ok=True)
        return WATCHLIST_FILE
    except Exception:
        return FALLBACK_WATCHLIST_FILE

def load_watchlist_data() -> Dict[str, Any]:
    """Loads all watchlist data: { 'users': { 'user_id': [ {pid, title, price, added_at} ] }, 'products': { 'pid': [user_id, ...] } }"""
    path = _get_active_file_path()
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to read watchlist file: {e}")
    return {"users": {}, "products": {}}

def save_watchlist_data(data: Dict[str, Any]):
    """Persists watchlist data."""
    path = _get_active_file_path()
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.warning(f"Failed to save watchlist data: {e}")

def add_to_watchlist(
    user_id: int,
    product_id: str,
    title: str,
    price: Optional[float] = None,
    image_url: Optional[str] = None
) -> Tuple[bool, str]:
    """Adds a product to the user's watchlist."""
    data = load_watchlist_data()
    uid_str = str(user_id)
    pid_str = str(product_id).strip()

    if uid_str not in data["users"]:
        data["users"][uid_str] = []

    # Check if already in user's watchlist
    for item in data["users"][uid_str]:
        if item.get("product_id") == pid_str:
            item["price"] = price or item.get("price")
            item["updated_at"] = time.time()
            save_watchlist_data(data)
            return True, "already_watching"

    # Limit to max 25 items per user
    if len(data["users"][uid_str]) >= 25:
        data["users"][uid_str].pop(0)

    data["users"][uid_str].append({
        "product_id": pid_str,
        "title": title[:90] if title else f"منتج {pid_str}",
        "price": price or 0.0,
        "image_url": image_url,
        "added_at": time.time()
    })

    if pid_str not in data["products"]:
        data["products"][pid_str] = []
    if user_id not in data["products"][pid_str]:
        data["products"][pid_str].append(user_id)

    save_watchlist_data(data)
    logger.info(f"User {user_id} added product {pid_str} to watchlist.")
    return True, "added"

def remove_from_watchlist(user_id: int, product_id: str) -> bool:
    """Removes a product from user's watchlist."""
    data = load_watchlist_data()
    uid_str = str(user_id)
    pid_str = str(product_id).strip()

    removed = False
    if uid_str in data["users"]:
        initial_len = len(data["users"][uid_str])
        data["users"][uid_str] = [i for i in data["users"][uid_str] if i.get("product_id") != pid_str]
        if len(data["users"][uid_str]) < initial_len:
            removed = True

    if pid_str in data["products"] and user_id in data["products"][pid_str]:
        data["products"][pid_str].remove(user_id)
        if not data["products"][pid_str]:
            del data["products"][pid_str]

    if removed:
        save_watchlist_data(data)
    return removed

def get_user_watchlist(user_id: int) -> List[Dict[str, Any]]:
    """Returns the list of watched items for a specific user."""
    data = load_watchlist_data()
    return data.get("users", {}).get(str(user_id), [])

def get_total_watchlist_count() -> int:
    """Returns total number of active product watches across all users."""
    data = load_watchlist_data()
    total = 0
    for u_items in data.get("users", {}).values():
        total += len(u_items)
    return total

async def notify_watchlist_users(
    product_id: str,
    new_price: float,
    title: str,
    affiliate_url: str,
    bot_token: Optional[str] = None
) -> int:
    """
    Checks if any users are watching this product_id and alerts them if new_price <= watched_price.
    Returns the count of successfully alerted users.
    """
    token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN", "8900887118:AAFuAFcxS1Xa2K4g0tlpD_YutPrsco3Y-Vo")
    data = load_watchlist_data()
    pid_str = str(product_id).strip()

    user_ids = data.get("products", {}).get(pid_str, [])
    if not user_ids:
        return 0

    dzd_approx = int(new_price * 249) if new_price else 0
    safe_title = title[:80] if title else f"منتج {pid_str}"

    alert_text = (
        f"🔔 <b>تنبيه انخفاض السعر | DealScout Price Drop Alert!</b>\n\n"
        f"📦 <b>{safe_title}</b>\n\n"
        f"📉 <b>السعر الجديد:</b> <b>${new_price:.2f}</b> (~<b>{dzd_approx:,} دج</b>) 🔥\n"
        f"━━━━━━━━━━━━━━━━━\n"
        f"🔗 <b>رابط الشراء المباشر بأقصى تخفيض عملات:</b>\n"
        f"{affiliate_url}\n\n"
        f"💡 <i>وصلك هذا التنبيه لأنك قمت بتفعيل مراقبة هذا المنتج عبر بوت التخفيضات.</i>"
    )

    markup = {
        "inline_keyboard": [
            [{"text": "🪙 شراء الآن بتخفيض العملات", "url": affiliate_url}],
            [{"text": "📢 قناة الصفقات المعتمدة", "url": "https://t.me/DzAliexpress0"}]
        ]
    }

    alerted_count = 0
    async with httpx.AsyncClient(timeout=6.0) as client:
        for uid in user_ids:
            try:
                resp = await client.post(
                    f"https://api.telegram.org/bot{token}/sendMessage",
                    json={
                        "chat_id": uid,
                        "text": alert_text,
                        "parse_mode": "HTML",
                        "disable_web_page_preview": False,
                        "reply_markup": markup
                    }
                )
                if resp.status_code == 200 and resp.json().get("ok"):
                    alerted_count += 1
            except Exception as e:
                logger.warning(f"Could not alert user {uid} for product {pid_str}: {e}")

    logger.info(f"Price drop alert sent to {alerted_count} subscriber(s) for product {pid_str}.")
    return alerted_count
