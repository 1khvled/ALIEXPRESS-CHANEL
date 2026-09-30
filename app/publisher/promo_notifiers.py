"""
AliExpress Promo Era Notifiers & Alerts
Publishes automated alerts:
1. Before promo era ends (1 day / 24h before end): Expiration warning, coupon deadline alert, and frozen card pro-tip.
2. Before promo era starts (1 day / 24h before start): Warm-up alert, cart preparation guide, coins reminder.

Strictly deduplicated: Each alert is sent exactly once per promotion event.
"""
import os
import json
import httpx
from datetime import datetime, timezone, timedelta
from typing import Optional, Tuple, Dict, Any, List

from app.config.settings import settings
from app.aliexpress.promos import promo_tracker, PromoEvent
from app.publisher.state_tracker import (
    load_persistent_state,
    save_persistent_state
)
from app.utils.logger import logger

TARGET_CHANNEL_ID = os.getenv("TARGET_CHANNEL_ID", "@DzAliexpress0")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8900887118:AAELbFHyV2joUO-4EJ0fPSoZurkQNuENbfY")
ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN", "8708965924:AAH7SoSX7VV3Nx_yI_J39VzWjlsc-XPgXAQ")


def build_promo_ending_alert(promo: PromoEvent, end_hour_str: str = "08:00") -> Tuple[str, Dict[str, Any]]:
    """
    Builds the ending notifier post matching the reference channel alert:
    - Native Telegram blockquote alert
    - Coupon deadline notification
    - Pro-tip: Freezing/empty card price lock trick (حجز ببطاقة مجمدة 20 يوم)
    - Branded DealScout theme & inline links
    """
    lines = [
        f"<blockquote>⚠️ <b>تنتهي التخفيضات غداً صباحاً عند الساعة {end_hour_str}!</b></blockquote>",
        "",
        f"📌 <b>الفعالية الحالية:</b> {promo.name_ar}",
        "",
        "❌ <b>آخر فرصة للاستفادة من الكوبونات:</b>",
        "جميع قسائم التخفيض وأكواد الخصم الحالية ستتوقف عن العمل فور انتهاء الموعد.",
        "",
        "✅ <b>حيلة المحترفين (حجز وتثبيت السعر):</b>",
        "يمكنك حجز المنتجات المستهدفة الآن واختيار الدفع ببطاقة بنكية فارغة أو مجمدة (RedotPay / Paysera / Pyypl) لتثبيت سعر التخفيض في حسابك لمدة تصل إلى <b>20 يوماً</b>، وإتمام الدفع لاحقاً بعد انتهاء الفعالية!",
        "━━━━━━━━━━━━━━━━━",
        "🪙 <b>بوت مضاعفة تخفيض العملات:</b> @Alilo07BOT",
        "📢 <b>قناة الصفقات المعتمدة:</b> @DzAliexpress0"
    ]

    text = "\n".join(lines)
    reply_markup = {
        "inline_keyboard": [
            [
                {"text": "🪙 بوت تخفيض العملات DealScout", "url": "https://t.me/Alilo07BOT"}
            ],
            [
                {"text": "📢 قناة الصفقات المعتمدة", "url": "https://t.me/DzAliexpress0"}
            ]
        ]
    }
    return text, reply_markup


def build_promo_starting_alert(promo: PromoEvent, start_hour_str: str = "08:00") -> Tuple[str, Dict[str, Any]]:
    """
    Builds the warm-up starting notifier post matching authentic Algerian deal channels:
    - Lists active official coupons
    - Explains coupon booking / saving tutorial using high-value phone link
    - Sets 08:00 AM booking alert
    """
    lines = [
        f"🚨 <b>كوبونات حدث {promo.name_ar} لشهر أكتوبر!</b> 🛍️",
        f"تنطلق غداً <b>01 أكتوبر وتستمر إلى غاية 07 أكتوبر</b> 🗓️",
        "",
        "🎟️ <b>كوبون 2/15$ :</b> <code>OTPRD02</code>",
        "🎟️ <b>كوبون 4/30$ :</b> <code>OTPRD04</code>",
        "🎟️ <b>كوبون 8/65$ :</b> <code>OTPRD08</code>",
        "🎟️ <b>كوبون 15/119$ :</b> <code>OTPRD15</code>",
        "🎟️ <b>كوبون 29/229$ :</b> <code>OTPRD28</code>",
        "🎟️ <b>كوبون 42/339$ :</b> <code>OTPRD42</code>",
        "🎟️ <b>كوبون 55/449$ :</b> <code>OTPRD55</code>",
        "",
        f"⭕️ <b>طريقة حجز الكوبونات وتثبيتها في حسابك (طبقوها غداً على {start_hour_str} صباحاً 🔥👌🏽):</b>",
        "⚠️ <b>ابدأ دائماً بالكوبونات الكبيرة ($55 ثم $42...)</b> ثم البقية واحداً تلو الآخر باه يبقاو في حسابك طيلة التخفيضات وما يهربلكش الستوك ✅",
        "",
        "🔹 <b>طبقوا الآن كامل الكوبونات على هذا المنتج باه تبقالكم في الحساب (كل الكوبونات مقبولة عليه) ⤵️</b>",
        "https://s.click.aliexpress.com/e/_c3ecIizb",
        "",
        "لا تنسى استخدام البوت للشراء بأقل الأسعار ومضاعفة خصم العملات :",
        "👉 t.me/Alilo07BOT",
        "━━━━━━━━━━━━━━━━━",
        "📢 <b>قناة الصيدات والصفقات:</b> @DzAliexpress0",
        "🔍 <i>#عروض_علي_اكسبرس #كوبونات_علي_اكسبرس #ChoiceDay</i>"
    ]

    text = "\n".join(lines)
    reply_markup = {
        "inline_keyboard": [
            [
                {"text": "🛒 رابط حجز وتثبيت الكوبونات في الحساب", "url": "https://s.click.aliexpress.com/e/_c3ecIizb"}
            ],
            [
                {"text": "🪙 بوت تخفيض العملات DealScout", "url": "https://t.me/Alilo07BOT"}
            ]
        ]
    }
    return text, reply_markup


def is_promo_notifier_already_sent(notifier_key: str) -> bool:
    """Checks whether this specific promo notifier key has already been posted."""
    state = load_persistent_state()
    sent_notifiers = state.get("sent_promo_notifiers", [])
    return notifier_key in sent_notifiers


def record_promo_notifier_sent(notifier_key: str):
    """Records that a promo notifier has been posted to prevent duplicate alerts."""
    state = load_persistent_state()
    if "sent_promo_notifiers" not in state:
        state["sent_promo_notifiers"] = []
    if notifier_key not in state["sent_promo_notifiers"]:
        state["sent_promo_notifiers"].append(notifier_key)
    save_persistent_state(state)


async def send_promo_alert_to_channel(
    text: str,
    reply_markup: Dict[str, Any],
    bot_token: Optional[str] = None,
    channel_id: Optional[str] = None
) -> Tuple[bool, Optional[str], Optional[int]]:
    """Dispatches the alert message to the target Telegram channel using photo banner if available."""
    token = bot_token or ADMIN_BOT_TOKEN or TELEGRAM_BOT_TOKEN
    target = channel_id or TARGET_CHANNEL_ID

    api_url = f"https://api.telegram.org/bot{token}"
    banner_path = os.path.join(settings.BASE_DIR, "storage", "assets", "choice_day_banner.png")

    try:
        async with httpx.AsyncClient(timeout=25.0) as client:
            if os.path.exists(banner_path) and len(text) <= 1024:
                with open(banner_path, "rb") as pf:
                    resp = await client.post(
                        f"{api_url}/sendPhoto",
                        data={
                            "chat_id": target,
                            "caption": text,
                            "parse_mode": "HTML",
                            "reply_markup": json.dumps(reply_markup)
                        },
                        files={"photo": ("choice_day_banner.png", pf, "image/png")}
                    )
            else:
                resp = await client.post(
                    f"{api_url}/sendMessage",
                    json={
                        "chat_id": target,
                        "text": text,
                        "parse_mode": "HTML",
                        "reply_markup": reply_markup,
                        "disable_web_page_preview": True
                    }
                )
            data = resp.json()
            if resp.status_code == 200 and data.get("ok"):
                msg_id = data.get("result", {}).get("message_id")
                return True, None, msg_id
            return False, data.get("description", "Telegram API returned non-OK"), None
    except Exception as e:
        logger.error(f"Failed to send promo alert: {e}")
        return False, str(e), None


async def check_and_auto_post_promo_notifiers(
    now: Optional[datetime] = None,
    bot_token: Optional[str] = None,
    channel_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Autonomous engine check called on schedule (every 30 mins):
    1. Checks if any active promo ends within 12 to 36 hours (~1 day before end).
       If yes, posts the Promo Ending Alert (with card freeze pro-tip).
    2. Checks if any upcoming promo starts within 12 to 36 hours (~1 day before start).
       If yes, posts the Promo Starting Alert (with warm-up guide).
    """
    if now is None:
        now = datetime.now(timezone.utc)

    results = []

    for promo in promo_tracker.calendar:
        # --- 1. CHECK PROMO ENDING ALERT (1 DAY BEFORE END) ---
        # If promo is currently active or ending tomorrow:
        if promo.start_date <= now <= promo.end_date:
            time_until_end = promo.end_date - now
            # Within ~24 hours before end (between 6h and 36h)
            if timedelta(hours=6) <= time_until_end <= timedelta(hours=36):
                notifier_key = f"END_ALERT_{promo.name}_{promo.end_date.strftime('%Y%m%d')}"
                if not is_promo_notifier_already_sent(notifier_key):
                    logger.info(f"Triggering Promo Ending Alert for {promo.name} (Ends in {time_until_end.total_seconds()/3600:.1f}h)")
                    text, markup = build_promo_ending_alert(promo)
                    success, err, msg_id = await send_promo_alert_to_channel(text, markup, bot_token, channel_id)
                    if success:
                        record_promo_notifier_sent(notifier_key)
                        results.append({
                            "type": "promo_ending_alert",
                            "promo": promo.name,
                            "message_id": msg_id,
                            "status": "published"
                        })
                    else:
                        logger.error(f"Failed to post promo ending alert: {err}")

        # --- 2. CHECK PROMO STARTING ALERT (1 DAY BEFORE START) ---
        elif now < promo.start_date:
            time_until_start = promo.start_date - now
            # Within ~24 hours before start (between 6h and 36h)
            if timedelta(hours=6) <= time_until_start <= timedelta(hours=36):
                notifier_key = f"START_ALERT_{promo.name}_{promo.start_date.strftime('%Y%m%d')}"
                if not is_promo_notifier_already_sent(notifier_key):
                    logger.info(f"Triggering Promo Starting Alert for {promo.name} (Starts in {time_until_start.total_seconds()/3600:.1f}h)")
                    text, markup = build_promo_starting_alert(promo)
                    success, err, msg_id = await send_promo_alert_to_channel(text, markup, bot_token, channel_id)
                    if success:
                        record_promo_notifier_sent(notifier_key)
                        results.append({
                            "type": "promo_starting_alert",
                            "promo": promo.name,
                            "message_id": msg_id,
                            "status": "published"
                        })
                    else:
                        logger.error(f"Failed to post promo starting alert: {err}")

    return results
