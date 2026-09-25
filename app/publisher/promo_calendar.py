"""
AliExpress Official Promo Calendar Publisher & Automation
Handles:
1. Posting the official Sales & Promos Calendar (رزنامة التخفيضات الرسمية).
2. Automatically detecting when an active sale ends and announcing the next upcoming sale.
3. Providing 1-tap manual posting for Admin (/calendar or button).
"""
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Optional, Tuple, Dict, Any
import httpx

try:
    from sqlalchemy import select
    from app.db.session import db_context
    from app.db.models import Deal
    HAS_DB = True
except (ImportError, Exception):
    HAS_DB = False

from app.config.settings import settings
import os
import json
from app.aliexpress.promos import promo_tracker, PromoEvent
from app.utils.logger import logger

# Official AliExpress 2026 Promotion Calendar Image
LOCAL_CALENDAR_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "official_calendar_october_2026.jpg")
if not os.path.exists(LOCAL_CALENDAR_PATH):
    LOCAL_CALENDAR_PATH = r"C:\Users\Abdelli\Downloads\photo_2026-09-25_18-41-05.jpg"

CALENDAR_BANNER_IMG = "https://ae-pic-a1.aliexpress-media.com/kf/HTB18eCBQXXXXXXfXXXX760XFXXXa.png"

def build_promo_calendar_post(now: Optional[datetime] = None) -> Tuple[str, Dict[str, Any]]:
    """Builds the comprehensive, high-converting Sales Calendar post."""
    if now is None:
        now = datetime.now(timezone.utc)

    active = promo_tracker.get_active_promo(now)
    next_promo = promo_tracker.get_next_promo(now)

    lines = [
        "📅 <b>رزنامة تخفيضات ومهرجانات AliExpress الرسمية لعام 2026 🔥</b>",
        "━━━━━━━━━━━━━━━━━"
    ]

    if active:
        end_s = active.end_date.strftime("%d/%m/%Y")
        lines.append("🔥 <b>الحدث الحالي الشغال الآن:</b>")
        lines.append(f"▫️ <b>{active.name_ar}</b>")
        lines.append(f"⏳ مستمر إلى غاية: <b>{end_s}</b>\n")

    lines.append("⏳ <b>المواعيد والمهرجانات القادمة:</b>")

    upcoming = [p for p in promo_tracker.calendar if p.end_date > now]
    for p in upcoming:
        s_str = p.start_date.strftime("%d/%m")
        e_str = p.end_date.strftime("%d/%m/%Y")
        days_left = (p.start_date - now).days

        if p.start_date <= now <= p.end_date:
            tag = "🟢 شغال الآن"
        elif days_left <= 0:
            tag = "⚡ ينطلق اليوم!"
        elif days_left == 1:
            tag = "⏳ غداً ينطلق!"
        else:
            tag = f"بعد {days_left} يوم"

        lines.append(f"▫️ <b>{p.name_ar}</b>")
        lines.append(f"   🗓 من {s_str} إلى {e_str} ({tag})")

    lines.append("━━━━━━━━━━━━━━━━━")
    lines.append("💡 <i>نصيحة: احرص على جمع العملات يومياً في التطبيق واستغلال الكوبونات للحصول على أكبر نسبة خصم!</i>")
    lines.append("")
    lines.append("🪙 استخدم بوت DealScoutDz للحصول على تخفيض العملات: @Alilo07BOT")

    caption = "\n".join(lines)

    reply_markup = {
        "inline_keyboard": [
            [
                {"text": "🪙 فتح بوت تخفيض العملات", "url": "https://t.me/Alilo07BOT"}
            ],
            [
                {"text": "📢 قناة الصفقات المعتمدة", "url": "https://t.me/DzAliexpress0"}
            ]
        ]
    }

    return caption, reply_markup

def build_next_sale_transition_post(ended_promo: PromoEvent, next_promo: PromoEvent, now: Optional[datetime] = None) -> Tuple[str, Dict[str, Any]]:
    """Builds the transition announcement post when one promo ends and the next approaches."""
    if now is None:
        now = datetime.now(timezone.utc)

    days_left = max(0, (next_promo.start_date - now).days)
    s_str = next_promo.start_date.strftime("%d/%m")
    e_str = next_promo.end_date.strftime("%d/%m/%Y")

    lines = [
        f"🚨 <b>انتهاء {ended_promo.name_ar} والتحضير للحدث القادم! ⏳</b>",
        "━━━━━━━━━━━━━━━━━",
        f"انتهت رسمياً فعالية <b>{ended_promo.name}</b>.",
        "",
        "🎯 <b>الحدث التخفيضي الكبير القادم:</b>",
        f"▫️ <b>{next_promo.name_ar}</b>",
        f"🗓 الموعد: من <b>{s_str}</b> إلى <b>{e_str}</b>",
        f"⏳ المتبقي للانطلاق: <b>{days_left} أيام فقط!</b>",
        "━━━━━━━━━━━━━━━━━",
        "💡 <i>استغل هذه الأيام لجمع أكبر رصيد من العملات المجانية اليومية داخل تطبيق AliExpress لتكون مستعداً لأكبر التخفيضات!</i>",
        "",
        "🪙 استخدم بوت DealScoutDz لحساب خصم العملات: @Alilo07BOT"
    ]

    caption = "\n".join(lines)

    reply_markup = {
        "inline_keyboard": [
            [
                {"text": "🪙 فتح بوت تخفيض العملات", "url": "https://t.me/Alilo07BOT"}
            ],
            [
                {"text": "📢 قناة الصفقات المعتمدة", "url": "https://t.me/DzAliexpress0"}
            ]
        ]
    }

    return caption, reply_markup

async def publish_calendar_to_channel(bot_token: Optional[str] = None, channel_id: Optional[str] = None) -> Tuple[bool, Optional[str], Optional[int]]:
    """Directly publishes the official promo calendar post to the Telegram channel."""
    token = bot_token or settings.TELEGRAM_BOT_TOKEN
    target = channel_id or settings.TARGET_CHANNEL_ID

    caption, markup = build_promo_calendar_post()

    api_url = f"https://api.telegram.org/bot{token}"
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            if os.path.exists(LOCAL_CALENDAR_PATH):
                with open(LOCAL_CALENDAR_PATH, "rb") as f:
                    files = {"photo": ("official_aliexpress_calendar_2026.jpg", f, "image/jpeg")}
                    data = {
                        "chat_id": target,
                        "caption": caption[:1024],
                        "parse_mode": "HTML",
                        "reply_markup": json.dumps(markup)
                    }
                    resp = await client.post(f"{api_url}/sendPhoto", data=data, files=files)
            else:
                resp = await client.post(
                    f"{api_url}/sendPhoto",
                    json={
                        "chat_id": target,
                        "photo": CALENDAR_BANNER_IMG,
                        "caption": caption[:1024],
                        "parse_mode": "HTML",
                        "reply_markup": markup
                    }
                )
            data = resp.json()
            if resp.status_code == 200 and data.get("ok"):
                msg_id = data.get("result", {}).get("message_id")
                return True, None, msg_id
            else:
                # Text fallback if photo fails
                resp_text = await client.post(
                    f"{api_url}/sendMessage",
                    json={
                        "chat_id": target,
                        "text": caption,
                        "parse_mode": "HTML",
                        "reply_markup": markup
                    }
                )
                data_text = resp_text.json()
                if resp_text.status_code == 200 and data_text.get("ok"):
                    msg_id = data_text.get("result", {}).get("message_id")
                    return True, None, msg_id
                return False, data.get("description", "Failed to send message"), None
    except Exception as e:
        return False, str(e), None

async def check_and_auto_post_promo_transitions() -> Tuple[bool, Optional[str]]:
    """
    Automated check designed to run in background / cron:
    1. Checks if a promo has ended within the last 24h and the next transition post hasn't been posted yet.
    2. Checks if weekly calendar refresh is due (every 7 days) using central state tracker.
    """
    from app.publisher.state_tracker import is_calendar_eligible, record_calendar_published

    eligible, reason = await is_calendar_eligible()
    if not eligible:
        return False, reason

    now = datetime.now(timezone.utc)
    success, err, msg_id = await publish_calendar_to_channel()
    if success:
        record_calendar_published()
        if HAS_DB:
            try:
                async with db_context() as session:
                    record = Deal(
                        product_id=f"PROMO_CALENDAR_{now.strftime('%Y%m%d')}",
                        original_url="https://aliexpress.com",
                        title="رزنامة تخفيضات ومهرجانات AliExpress",
                        status="PUBLISHED"
                    )
                    session.add(record)
                    await session.commit()
            except Exception:
                pass
        return True, f"Published official promo calendar (Msg ID: {msg_id})"
    return False, err
