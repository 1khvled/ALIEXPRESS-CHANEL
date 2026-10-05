"""
Admin Error Alerts Notifier
Sends instant notifications to the Telegram Admin Bot whenever an error occurs
during channel sweeping, deal extraction, or publishing.
Includes intelligent deduplication to prevent flood/spamming during persistent outages.
"""
import os
import html
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict
import httpx
from app.config.settings import settings
from app.utils.logger import logger

# In-memory cooldown cache: {error_key: last_sent_timestamp}
_ALERT_COOLDOWN_CACHE: Dict[str, float] = {}
COOLDOWN_SECONDS = 900.0  # 15 minutes cooldown for identical errors

def get_admin_credentials():
    token = os.getenv("ADMIN_BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN") or ""
    admin_id_raw = os.getenv("ADMIN_USER_ID") or getattr(settings, "ADMIN_USER_ID", None)
    admin_id = None
    if admin_id_raw:
        try:
            admin_id = int(str(admin_id_raw).strip())
        except (ValueError, TypeError):
            pass
    return token, admin_id

async def notify_admin_error(
    error_type: str,
    details: str,
    channel: str = "algeria",
    exc: Optional[Exception] = None
) -> bool:
    """
    Sends an error alert directly to the Admin User ID via the Admin Bot.
    Guarantees no crashes, graceful HTML escaping, and 15-minute alert deduplication.
    """
    token, admin_id = get_admin_credentials()
    if not token or not admin_id:
        logger.warning(f"[ADMIN ALERT] Skipping alert (token={bool(token)}, admin_id={admin_id}): {error_type}")
        return False

    error_msg = str(details or "")
    if exc:
        error_msg += f"\nException: {type(exc).__name__}: {str(exc)}"

    # Deduplication key based on error type and first 80 characters of message
    dedup_key = f"{channel}:{error_type}:{error_msg[:80]}"
    now = datetime.now(timezone.utc).timestamp()
    last_sent = _ALERT_COOLDOWN_CACHE.get(dedup_key, 0.0)

    if (now - last_sent) < COOLDOWN_SECONDS:
        logger.info(f"[ADMIN ALERT] Alert throttled (cooldown active): {dedup_key}")
        return False

    now_dz = datetime.now(timezone(timedelta(hours=1)))
    time_str = now_dz.strftime("%Y-%m-%d %H:%M:%S")

    escaped_details = html.escape(error_msg[:600])
    channel_display = "@DzAliexpress0 (DZ)" if channel == "algeria" else "@francedealsdz (FR)"

    text = (
        "⚠️ <b>تنبيه خطأ في نظام البوت / Bot Alert</b> ⚠️\n\n"
        f"📍 <b>نوع الخطأ:</b> {html.escape(error_type)}\n"
        f"📢 <b>القناة:</b> {channel_display}\n"
        f"⏰ <b>التوقيت:</b> <code>{time_str} (UTC+1)</code>\n\n"
        "❌ <b>تفاصيل الخطأ / Details:</b>\n"
        f"<pre>{escaped_details}</pre>\n\n"
        "🛠 <i>تم الإرسال تلقائياً لمراجعة المشكلة.</i>"
    )

    payload = {
        "chat_id": admin_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json=payload
            )
            if resp.status_code == 200 and resp.json().get("ok"):
                _ALERT_COOLDOWN_CACHE[dedup_key] = now
                logger.info(f"[ADMIN ALERT] Error alert sent to Admin ID {admin_id}: {error_type}")
                return True
            else:
                logger.error(f"[ADMIN ALERT] Telegram API error: {resp.text}")
                # Fallback to plain text if HTML parsing failed
                payload["parse_mode"] = None
                resp2 = await client.post(
                    f"https://api.telegram.org/bot{token}/sendMessage",
                    json=payload
                )
                if resp2.status_code == 200 and resp2.json().get("ok"):
                    _ALERT_COOLDOWN_CACHE[dedup_key] = now
                    return True
    except Exception as e:
        logger.error(f"[ADMIN ALERT] Failed to send error alert to admin: {e}")

    return False
