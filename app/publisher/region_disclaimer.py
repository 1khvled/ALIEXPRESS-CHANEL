"""
AliExpress Region Switching Guide & Disclaimer
Explains why users need to switch region to Canada 🇨🇦 or Korea 🇰🇷 to unlock 70%+ Coins discount.
Posts and pins to @DzAliexpress0, recurring every 14 days.
"""
import os
import time
from typing import Tuple, Optional
import httpx
from app.utils.logger import logger

TARGET_CHANNEL_ID = os.getenv("TARGET_CHANNEL_ID", "@DzAliexpress0")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8900887118:AAFuAFcxS1Xa2K4g0tlpD_YutPrsco3Y-Vo")
ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN", "8708965924:AAGi9HgLDxKsvaOzPOnCDRhI4c9WAfUvkOk")

DISCLAIMER_TEXT = """❝ ❓ <b>لماذا يجب تغيير دولة التطبيق في AliExpress؟</b> ❞

بعض الدول مثل <b>الجزائر 🇩🇿</b> تكون فيها نسبة تخفيض العملات منخفضة (1% ~ 5%)، عكس بعض الدول مثل <b>كندا 🇨🇦</b> أو <b>كوريا 🇰🇷</b> التي تكون فيها نسبة تخفيض العملات مرتفعة جداً وتصل حتى <b>70%</b>! 🔥

💡 <b>الحل للحصول على أفضل وأرخص سعر:</b>
هو <b>تغيير دولة التطبيق</b> إلى الدولة الموضحة في المنشور (غالباً <b>كندا 🇨🇦</b> أو <b>كوريا 🇰🇷</b>) مع ترك <b>عنوان الشحن الفعلي الخاص بك (الجزائر 🇩🇿)</b> دون أي تغيير!

📌 <b>خطوات التغيير بكل بساطة في ثوانٍ:</b>
1️⃣ افتح تطبيق AliExpress.
2️⃣ اذهب إلى: <b>الحساب (Account)</b> ⬅️ <b>الإعدادات (Settings ⚙️)</b>.
3️⃣ اضغط على: <b>البلد / المنطقة (Ship to / Region)</b>.
4️⃣ اختر <b>كندا 🇨🇦</b> أو <b>كوريا 🇰🇷</b> (واترك العملة بالدولار $ أو الأورو €).
5️⃣ ادخل الآن عبر روابط العروض واشترِ بالعملات مباشرة بأرخص سعر! 💸

🪙 <b>البوت المباشر لزيادة تخفيض العملات:</b> @Alilo07BOT
📢 <b>قناة التيليغرام للمزيد من العروض والصيدات:</b> @DzAliexpress0"""

DISCLAIMER_KEYBOARD = {
    "inline_keyboard": [
        [
            {"text": "🪙 بوت تخفيض العملات DealScoutDz", "url": "https://t.me/Alilo07BOT"}
        ],
        [
            {"text": "📢 انضم لقناة العروض @DzAliexpress0", "url": "https://t.me/DzAliexpress0"}
        ]
    ]
}

# Timestamp tracking file (in /tmp for Vercel/Linux, or local storage)
_TIMESTAMP_FILE = "/tmp/last_disclaimer_pinned.txt" if os.path.exists("/tmp") else os.path.join(os.path.dirname(__file__), "last_disclaimer_pinned.txt")

def _get_last_pinned_time() -> float:
    try:
        if os.path.exists(_TIMESTAMP_FILE):
            with open(_TIMESTAMP_FILE, "r", encoding="utf-8") as f:
                return float(f.read().strip())
    except Exception:
        pass
    return 0.0

def _set_last_pinned_time(t: float):
    try:
        with open(_TIMESTAMP_FILE, "w", encoding="utf-8") as f:
            f.write(str(t))
    except Exception:
        pass

async def publish_and_pin_disclaimer(bot_token: Optional[str] = None) -> Tuple[bool, Optional[str], Optional[int]]:
    """
    Publishes the region switching guide to @DzAliexpress0 and pins it in the channel.
    """
    token = bot_token or ADMIN_BOT_TOKEN or TELEGRAM_BOT_TOKEN
    api_url = f"https://api.telegram.org/bot{token}"

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            # 1. Send Message
            send_resp = await client.post(
                f"{api_url}/sendMessage",
                json={
                    "chat_id": TARGET_CHANNEL_ID,
                    "text": DISCLAIMER_TEXT,
                    "parse_mode": "HTML",
                    "reply_markup": DISCLAIMER_KEYBOARD,
                    "disable_web_page_preview": True
                }
            )
            data = send_resp.json()
            if send_resp.status_code != 200 or not data.get("ok"):
                err = data.get("description", f"HTTP {send_resp.status_code}")
                logger.error(f"Failed to publish region disclaimer: {err}")
                return False, err, None

            msg_id = data["result"]["message_id"]

            # 2. Pin Message in Channel
            try:
                pin_resp = await client.post(
                    f"{api_url}/pinChatMessage",
                    json={
                        "chat_id": TARGET_CHANNEL_ID,
                        "message_id": msg_id,
                        "disable_notification": False
                    }
                )
                logger.info(f"Pinned region disclaimer #{msg_id} in {TARGET_CHANNEL_ID}: {pin_resp.status_code}")
            except Exception as e:
                logger.warning(f"Could not pin message #{msg_id}: {e}")

            _set_last_pinned_time(time.time())
            try:
                from app.publisher.state_tracker import record_disclaimer_published
                record_disclaimer_published()
            except Exception:
                pass
            return True, None, msg_id

    except Exception as e:
        logger.exception(f"Error publishing disclaimer: {e}")
        return False, str(e), None

async def check_and_auto_post_disclaimer(force: bool = False) -> Tuple[bool, str]:
    """
    Enforces 14-day recurrence for the region disclaimer using central state tracker.
    """
    if not force:
        from app.publisher.state_tracker import is_disclaimer_eligible
        eligible, reason = await is_disclaimer_eligible()
        if not eligible:
            return False, reason

    success, err, msg_id = await publish_and_pin_disclaimer()
    if success:
        return True, f"Region disclaimer successfully published and pinned as message #{msg_id} in {TARGET_CHANNEL_ID}"
    return False, f"Failed to publish disclaimer: {err}"
