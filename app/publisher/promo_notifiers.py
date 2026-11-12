"""
AliExpress Promo Era Notifiers & Alerts
Publishes automated alerts:
1. Before promo era ends (1 day / 24h before end): Expiration warning, coupon deadline alert, and frozen card pro-tip.
2. Before promo era starts (1 day / 24h before start): Warm-up alert, cart preparation guide, coins reminder.

Strictly deduplicated: Each alert is sent exactly once per promotion event.
"""
import os
import re
import json
import httpx
from datetime import datetime, timezone, timedelta
from typing import Optional, Tuple, Dict, Any, List
from pathlib import Path

from app.config.settings import settings
from app.aliexpress.promos import promo_tracker, PromoEvent
from app.publisher.state_tracker import (
    load_persistent_state,
    save_persistent_state
)
from app.utils.logger import logger

TARGET_CHANNEL_ID = os.getenv("TARGET_CHANNEL_ID", "@DzAliexpress0")
TELEGRAM_BOT_TOKEN = getattr(settings, "TELEGRAM_BOT_TOKEN", "") or os.getenv("TELEGRAM_BOT_TOKEN", "")
ADMIN_BOT_TOKEN = getattr(settings, "ADMIN_BOT_TOKEN", "") or os.getenv("ADMIN_BOT_TOKEN", "")

# Official DealScout Event Ended photo paths
EVENT_ENDED_IMAGE_PATHS = [
    str(Path(settings.BASE_DIR) / "assets" / "dealscout_event_ended.png"),
    str(Path(settings.BASE_DIR) / "app" / "assets" / "dealscout_event_ended.png"),
    os.path.join(os.path.dirname(__file__), "..", "assets", "dealscout_event_ended.png"),
    r"C:\Users\Abdelli\Downloads\DealScout_ انتهاء العروض.png",
]

def get_event_ended_image_path() -> Optional[str]:
    """Resolves the DealScout Event Ended photo with robust fallbacks."""
    for p in EVENT_ENDED_IMAGE_PATHS:
        if os.path.exists(p):
            return p
    return None


# Official DealScout Event Started / Kickoff photo paths
EVENT_STARTED_IMAGE_PATHS = [
    str(Path(settings.BASE_DIR) / "assets" / "11_11_warm_up_kickoff.png"),
    str(Path(settings.BASE_DIR) / "assets" / "dealscout_event_started.png"),
    str(Path(settings.BASE_DIR) / "app" / "assets" / "dealscout_event_started.png"),
    os.path.join(os.path.dirname(__file__), "..", "assets", "dealscout_event_started.png"),
    r"C:\Users\Abdelli\Downloads\DealScout AliExpress Sale Kickoff.png",
]

def get_event_started_image_path() -> Optional[str]:
    """Resolves the DealScout Event Kickoff / Start photo with robust fallbacks."""
    for p in EVENT_STARTED_IMAGE_PATHS:
        if os.path.exists(p):
            return p
    return None


DZ_TZ = timezone(timedelta(hours=1))

_ARABIC_HOUR_WORDS = {
    1: "الواحدة", 2: "الثانية", 3: "الثالثة", 4: "الرابعة",
    5: "الخامسة", 6: "السادسة", 7: "السابعة", 8: "الثامنة",
    9: "التاسعة", 10: "العاشرة", 11: "الحادية عشرة", 12: "الثانية عشرة",
}

# Year/month/noise tokens stripped when grouping the same campaign that is
# listed twice (baseline vs auto-generated recurring placeholder).
_CAMPAIGN_NOISE_RE = re.compile(
    r"\b(19|20)\d{2}\b"
    r"|\b(global shopping festival|shopping festival|main sale|main|warm up|warmup|sale)\b"
    r"|\b(january|february|march|april|may|june|july|august|september|october|november|december)\b",
    re.IGNORECASE,
)


def _is_placeholder_promo(promo: PromoEvent) -> bool:
    """True for calendar entries that only exist because the recurring generator filled a gap."""
    return (
        getattr(promo, "source", "") == "recurring"
        and not promo.coupon_tiers
        and not promo.coupon_tiers_fr
    )


def _is_shadowed_placeholder(promo: PromoEvent, calendar: List[PromoEvent]) -> bool:
    """A recurring placeholder is shadowed when a real baseline/discovered event covers its dates."""
    if not _is_placeholder_promo(promo):
        return False
    for other in calendar:
        if other is promo or getattr(other, "source", "") not in ("baseline", "discovered"):
            continue
        if other.start_date < promo.end_date and other.end_date > promo.start_date:
            return True
    return False


def _campaign_key(promo: PromoEvent) -> str:
    """Collapses '11.11 ... Main Sale 2026' and '11.11 ... Main Sale' into one campaign key."""
    name = (promo.name or "").lower().replace("&", " and ")
    name = _CAMPAIGN_NOISE_RE.sub(" ", name)
    name = re.sub(r"[^a-z0-9.]+", " ", name)
    name = re.sub(r"\s+", " ", name).strip()
    return re.sub(r"\s+", "_", name) or "promo"


def _campaign_notifier_key(prefix: str, promo: PromoEvent) -> str:
    """One dedupe key per campaign occurrence, regardless of which duplicate entry triggers it."""
    return f"{prefix}_{_campaign_key(promo)}_{promo.start_date.strftime('%Y%m')}"


def _promo_that_keeps_sale_running(
    promo: PromoEvent,
    active_promos: List[PromoEvent],
    min_extra: timedelta = timedelta(hours=36)
) -> Optional[PromoEvent]:
    """
    Returns a real active event that continues well past `promo`.
    Used to avoid announcing "the sale ends tomorrow" while a bigger event
    (e.g. 11.11) is still running for several more days.
    """
    for other in active_promos:
        if other is promo or _is_placeholder_promo(other):
            continue
        if other.end_date <= promo.end_date + min_extra:
            continue
        if other.is_major or other.coupon_tiers or other.coupon_tiers_fr:
            return other
    return None


def _relative_day_label(target: datetime, now: datetime) -> str:
    """Returns 'اليوم' / 'غدا' / 'يوم DD/MM' in Algeria time."""
    target_dz = target.astimezone(DZ_TZ)
    now_dz = now.astimezone(DZ_TZ)
    day_delta = (target_dz.date() - now_dz.date()).days
    if day_delta <= 0:
        return "اليوم"
    if day_delta == 1:
        return "غدا"
    return f"يوم {target_dz.strftime('%d/%m')}"


def _dz_end_label(end_date: datetime, now: datetime) -> str:
    """Builds an Algerian-time relative label such as 'غدا صباحا على الساعة التاسعة (09:00 بتوقيت الجزائر)'."""
    end_dz = end_date.astimezone(DZ_TZ)
    now_dz = now.astimezone(DZ_TZ)

    # AliExpress cutoffs are stored at :59:59 — round up to the marketing hour (08:00, not 07:59).
    if end_dz.second >= 30 or end_dz.microsecond >= 500_000:
        end_dz = (end_dz + timedelta(minutes=1)).replace(second=0, microsecond=0)
    else:
        end_dz = end_dz.replace(second=0, microsecond=0)

    day_delta = (end_dz.date() - now_dz.date()).days
    if day_delta <= 0:
        day_label = "اليوم"
    elif day_delta == 1:
        day_label = "غدا"
    else:
        day_label = f"يوم {end_dz.strftime('%d/%m')}"

    period = "صباحا" if end_dz.hour < 12 else "مساء"
    hour_word = _ARABIC_HOUR_WORDS.get(end_dz.hour % 12 or 12, str(end_dz.hour))
    return f"{day_label} {period} على الساعة {hour_word} ({end_dz.strftime('%H:%M')} بتوقيت الجزائر)"


def build_promo_ending_alert(
    promo: Optional[PromoEvent] = None,
    end_hour_str: Optional[str] = None,
    now: Optional[datetime] = None
) -> Tuple[str, Dict[str, Any]]:
    """
    Builds the ending notifier post:
    - Blockquote alert with the REAL end day/hour derived from the promo (Algeria time)
    - Names the event that is actually ending, so it can't be mistaken for a bigger running sale
    - Last chance for coupons
    - 20-day frozen card reservation trick
    - Links to bot and telegram channel
    - Inline keyboard buttons
    """
    if now is None:
        now = datetime.now(timezone.utc)

    if end_hour_str:
        hour_label = "الثامنة" if end_hour_str in ["08:00", "الثامنة", "8:00", "8"] else end_hour_str
        when_label = f"غدا صباحا على الساعة {hour_label}"
    elif promo is not None and getattr(promo, "end_date", None):
        when_label = _dz_end_label(promo.end_date, now)
    else:
        when_label = "غدا صباحا على الساعة الثامنة"

    lines = [
        f"<blockquote>⚠️ <b>تنتهي التخفيضات {when_label}</b></blockquote>",
        "",
    ]

    event_name = (getattr(promo, "name_ar", None) or getattr(promo, "name", None)) if promo else None
    if event_name:
        lines.extend([f"🏁 <b>الحدث:</b> {event_name}", ""])

    lines.extend([
        "❌ <b>آخر فرصة للإستفادة من الكوبونات</b>",
        "",
        "✅ <b>يمكن حجز بعض المنتجات ببطاقة مجمدة لمدة تصل الى 20 يوم بعد انتهاء التخفيضات</b>",
        "",
        "🤖 <b>البوت لتخفيض الاسعار :</b> https://t.me/Alilo07BOT",
        "",
        "📢 <b>قناة التيليغرام للمزيد من العروض :</b> https://t.me/DzAliexpress0"
    ])

    text = "\n".join(lines)
    reply_markup = {
        "inline_keyboard": [
            [
                {"text": "🪙 البوت لتخفيض الأسعار", "url": "https://t.me/Alilo07BOT"}
            ],
            [
                {"text": "📢 قناة الصفقات المعتمدة", "url": "https://t.me/DzAliexpress0"}
            ]
        ]
    }
    return text, reply_markup


def build_promo_concluded_alert(promo: Optional[PromoEvent] = None) -> Tuple[str, Dict[str, Any]]:
    """
    Builds the event concluded post when the sale has officially ended:
    - Official conclusion announcement
    - Invalidation of coupons
    - 20-day frozen card reminder
    - Links to bot and channel
    - Inline keyboard buttons
    """
    promo_name = f" ({promo.name_ar})" if promo and getattr(promo, "name_ar", None) else ""
    lines = [
        f"<blockquote>🛑 <b>انتهت رسمياً عروض وتخفيضات علي اكسبرس{promo_name} 🔥</b></blockquote>",
        "",
        "❌ <b>انتهت صلاحية جميع الكوبونات وأكواد الخصم الخاصة بهذا الحدث.</b>",
        "",
        "✅ <b>يمكن لمن حجز المنتجات ببطاقة مجمدة إتمام الدفع بنفس سعر التخفيض لمدة تصل إلى 20 يوم بعد انتهاء التخفيضات!</b>",
        "",
        "🤖 <b>البوت لتخفيض الاسعار :</b> https://t.me/Alilo07BOT",
        "",
        "📢 <b>قناة التيليغرام للمزيد من العروض :</b> https://t.me/DzAliexpress0"
    ]
    text = "\n".join(lines)
    reply_markup = {
        "inline_keyboard": [
            [
                {"text": "🪙 البوت لتخفيض الأسعار", "url": "https://t.me/Alilo07BOT"}
            ],
            [
                {"text": "📢 قناة الصفقات المعتمدة", "url": "https://t.me/DzAliexpress0"}
            ]
        ]
    }
    return text, reply_markup


def build_promo_starting_alert(
    promo: PromoEvent,
    start_hour_str: str = "08:00",
    now: Optional[datetime] = None
) -> Tuple[str, Dict[str, Any]]:
    """
    Builds the warm-up starting notifier post matching authentic Algerian deal channels:
    - Lists active official coupons dynamically from the promo event
    - Explains coupon booking / saving tutorial using high-value phone link
    - Sets 08:00 AM booking alert
    """
    if now is None:
        now = datetime.now(timezone.utc)
    start_label = _relative_day_label(promo.start_date, now)
    coupons = promo.coupon_tiers if promo.coupon_tiers else []
    coupon_lines = []
    for c in coupons:
        t = c.get("tier", "").strip()
        code = c.get("code", "").strip()
        if t and code:
            coupon_lines.append(f"🎟️ <b>كوبون {t} :</b> <code>{code}</code>")

    if coupon_lines:
        is_brand_day = "brand" in promo.name.lower()
        if is_brand_day:
            lines = [
                f"🚨 <b>كوبونات حدث {promo.name_ar}!</b> 🛍️",
                f"تنطلق {start_label} <b>{promo.start_date.strftime('%d/%m')} وتستمر إلى غاية {promo.end_date.strftime('%d/%m/%Y')}</b> 🗓️",
                "",
                *coupon_lines,
                "",
                "⚠️ <b>الكوبونات تعمل في بعض المنتجات فقط الموجودة في هذه الصفحة :</b>",
                "https://s.click.aliexpress.com/e/_c3F40Fvf",
                "",
                "🪙 <b>بوت مضاعفة تخفيض العملات:</b> @Alilo07BOT",
                "━━━━━━━━━━━━━━━━━",
                "🌐 <b>موقع الصفقات والكوبونات:</b> https://dealscoutgreen.vercel.app/",
                "📢 <b>قناة الصفقات الرسمية:</b> @DzAliexpress0",
                "🔍 <i>#عروض_علي_اكسبرس #كوبونات_علي_اكسبرس #Brand_Day</i>"
            ]
            reply_markup = {
                "inline_keyboard": [
                    [
                        {"text": "🛍️ صفحة المنتجات المؤهلة للكوبونات", "url": "https://s.click.aliexpress.com/e/_c3F40Fvf"}
                    ],
                    [
                        {"text": "🪙 بوت تخفيض العملات", "url": "https://t.me/Alilo07BOT"},
                        {"text": "🇫🇷 قناة عروض فرنسا", "url": "https://t.me/francedealsdz"}
                    ]
                ]
            }
            return "\n".join(lines), reply_markup

        big_coupons_str = " ثم ".join([f"${c.get('tier', '').split('/')[0]}" for c in reversed(coupons[-2:]) if '/' in c.get('tier', '')]) or "$70 ثم $53"
        lines = [
            f"🚨 <b>كوبونات حدث {promo.name_ar}!</b> 🛍️",
            f"تنطلق {start_label} <b>{promo.start_date.strftime('%d/%m')} وتستمر إلى غاية {promo.end_date.strftime('%d/%m/%Y')}</b> 🗓️",
            "",
            *coupon_lines,
            "",
            f"⭕️ <b>طريقة حجز الكوبونات وتثبيتها في حسابك (طبقوها {start_label} على {start_hour_str} صباحاً 🔥👌🏽):</b>",
            f"⚠️ <b>ابدأ دائماً بالكوبونات الكبيرة ({big_coupons_str}...)</b> ثم البقية واحداً تلو الآخر باه يبقاو في حسابك طيلة التخفيضات وما يهربلكش الستوك ✅",
            "",
            "🔹 <b>طبقوا الآن كامل الكوبونات على هذا المنتج باه تبقالكم في الحساب ⤵️</b>",
            "https://s.click.aliexpress.com/e/_c3d8Osgp",
            "",
            "لا تنسى استخدام البوت للشراء بأقل الأسعار ومضاعفة خصم العملات :",
            "👉 t.me/Alilo07BOT",
            "━━━━━━━━━━━━━━━━━",
            "🌐 <b>موقع الصفقات والكوبونات:</b> https://dealscoutgreen.vercel.app/",
            "📢 <b>قناة الصفقات الرسمية:</b> @DzAliexpress0",
            "🔍 <i>#عروض_علي_اكسبرس #كوبونات_علي_اكسبرس</i>"
        ]
    else:
        lines = [
            f"🚨 <b>اقتراب انطلاق فعاليات {promo.name_ar}!</b> 🛍️",
            f"الموعد: من <b>{promo.start_date.strftime('%d/%m')} إلى {promo.end_date.strftime('%d/%m/%Y')}</b> 🗓️",
            "",
            "💡 <b>تفاصيل التخفيض:</b>",
            "الحدث يعتمد على <b>تخفيضات العملات المضاعفة 🪙</b> وقسائم المتاجر الحصرية (Store Coupons).",
            "احرصوا على جمع العملات يومياً في التطبيق لتكونوا جاهزين لأقوى الصفقات والعروض!",
            "",
            "🔥 <b>إجمع العملات من هنا ⤵️</b>",
            "👉 https://s.click.aliexpress.com/e/_c4l391NX",
            "",
            "لا تنسى استخدام البوت للشراء بأقل الأسعار ومضاعفة الخصم :",
            "👉 t.me/Alilo07BOT",
            "━━━━━━━━━━━━━━━━━",
            "🌐 <b>موقع الصفقات والكوبونات:</b> https://dealscoutgreen.vercel.app/",
            "📢 <b>قناة الصفقات الرسمية:</b> @DzAliexpress0"
        ]

    text = "\n".join(lines)
    reply_markup = {}
    return text, reply_markup


def build_promo_launch_alert(promo: PromoEvent, start_hour_str: str = "08:00") -> Tuple[str, Dict[str, Any]]:
    """Builds the launch alert when promo officially starts at 08:00 AM Algerian Time."""
    coupons = promo.coupon_tiers if promo.coupon_tiers else []
    coupon_lines = []
    for c in coupons:
        t = c.get("tier", "").strip()
        code = c.get("code", "").strip()
        if t and code:
            coupon_lines.append(f"🎟️ <b>كوبون {t} :</b> <code>{code}</code>")

    if coupon_lines:
        is_brand_day = "brand" in promo.name.lower()
        if is_brand_day:
            lines = [
                f"🚀 <b>انطلاق تخفيضات {promo.name_ar} رسمياً الآن! 🛍️🔥</b>",
                f"⏰ <b>الكوبونات شغالة ومتاحة حالياً (صالحة لغاية {promo.end_date.strftime('%d/%m/%Y')} 🗓️):</b>",
                "سارعوا باستغلالها قبل نفاد الكميات المحدودة! 🏃💨",
                "",
                *coupon_lines,
                "",
                "⚠️ <b>الكوبونات تعمل في بعض المنتجات فقط الموجودة في هذه الصفحة :</b>",
                "https://s.click.aliexpress.com/e/_c3F40Fvf",
                "",
                "🪙 <b>بوت مضاعفة تخفيض العملات:</b> @Alilo07BOT",
                "━━━━━━━━━━━━━━━━━",
                "🌐 <b>موقع الصفقات والكوبونات:</b> https://dealscoutgreen.vercel.app/",
                "📢 <b>قناة الصفقات الرسمية:</b> @DzAliexpress0",
                "🔍 <i>#عروض_علي_اكسبرس #كوبونات_علي_اكسبرس #Brand_Day</i>"
            ]
            reply_markup = {
                "inline_keyboard": [
                    [
                        {"text": "🛍️ صفحة المنتجات المؤهلة للكوبونات", "url": "https://s.click.aliexpress.com/e/_c3F40Fvf"}
                    ],
                    [
                        {"text": "🪙 بوت تخفيض العملات", "url": "https://t.me/Alilo07BOT"},
                        {"text": "🇫🇷 قناة عروض فرنسا", "url": "https://t.me/francedealsdz"}
                    ]
                ]
            }
            return "\n".join(lines), reply_markup

        lines = [
            f"🚀 <b>انطلاق تخفيضات {promo.name_ar} رسمياً الآن! 🛍️🔥</b>",
            f"⏰ <b>الكوبونات اشتغلت وبدأت بالعمل في هذه اللحظات ({start_hour_str} صباحاً بتوقيت الجزائر 🇩🇿):</b>",
            "سارعوا بحجزها وتطبيقها فوراً في حساباتكم قبل نفاد الكميات المحدودة! 🏃💨",
            "",
            *coupon_lines,
            "",
            f"⭕️ <b>طريقة حجز الكوبونات وتثبيتها في حسابك الآن 🔥👌🏽:</b>",
            "⚠️ <b>ابدأ دائماً بالكوبونات الكبيرة ($55 ثم $42...)</b> ثم البقية واحداً تلو الآخر باه يبقاو في حسابك طيلة التخفيضات وما يهربلكش الستوك ✅",
            "",
            "🔹 <b>طبقوا الآن كامل الكوبونات على هذا المنتج باه تبقالكم في الحساب ⤵️</b>",
            "https://s.click.aliexpress.com/e/_c3d8Osgp",
            "",
            "لا تنسى استخدام البوت للشراء بأقل الأسعار :",
            "https://t.me/Alilo07BOT",
            "━━━━━━━━━━━━━━━━━",
            "🌐 <b>موقع الصفقات والكوبونات:</b> https://dealscoutgreen.vercel.app/",
            "📢 <b>قناة الصفقات الرسمية:</b> @DzAliexpress0"
        ]
        reply_markup = {}
        return "\n".join(lines), reply_markup
    else:
        lines = [
            f"🚀 <b>انطلاق فعاليات {promo.name_ar} رسمياً الآن! 🛍️🔥</b>",
            f"⏰ <b>بدأت التخفيضات في هذه اللحظات ({start_hour_str} صباحاً بتوقيت الجزائر 🇩🇿):</b>",
            "استغلوا تخفيضات العملات المباشرة وقسائم المتاجر الحصرية على أفضل المنتجات! 🏃💨",
            "",
            "🔥 <b>رابط تفعيل وجمع العملات ⤵️</b>",
            "👉 https://s.click.aliexpress.com/e/_c4l391NX",
            "",
            "لا تنسى استخدام البوت للشراء بأقل الأسعار :",
            "https://t.me/Alilo07BOT",
            "━━━━━━━━━━━━━━━━━",
            "🌐 <b>موقع الصفقات والكوبونات:</b> https://dealscoutgreen.vercel.app/",
            "📢 <b>قناة الصفقات الرسمية:</b> @DzAliexpress0"
        ]
    return "\n".join(lines), {}


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
    channel_id: Optional[str] = None,
    coupon_list: Optional[List[Dict[str, str]]] = None,
    promo_title: str = "Choice Day",
    image_path: Optional[str] = None
) -> Tuple[bool, Optional[str], Optional[int]]:
    """Dispatches the alert message to the target Telegram channel using generated card graphic or DealScout photo."""
    from app.media.renderer import media_renderer
    token = bot_token or ADMIN_BOT_TOKEN or TELEGRAM_BOT_TOKEN
    target = channel_id or TARGET_CHANNEL_ID

    api_url = f"https://api.telegram.org/bot{token}"
    card_path = image_path

    # If no specific image_path provided, check if this is an ending or starting event alert
    if not card_path:
        if any(kw in text for kw in ["تنتهي التخفيضات", "انتهت التخفيضات", "انتهت رسمياً", "آخر فرصة للإستفادة"]):
            card_path = get_event_ended_image_path()
        elif any(kw in text for kw in ["انطلاق تخفيضات", "انطلاق فعاليات", "بدأت التخفيضات", "بداية تخفيضات", "كوبونات حدث", "اقتراب انطلاق"]):
            card_path = get_event_started_image_path()

    if not card_path and coupon_list:
        card_path = media_renderer.render_coupon_bulletin_card(
            coupon_list,
            promo_title=promo_title,
            channel_handle="@DzAliexpress0",
            is_french=False
        )
    if not card_path or not os.path.exists(card_path):
        banner_candidate = os.path.join(os.path.dirname(__file__), "..", "assets", "official_calendar_october_2026.jpg")
        if os.path.exists(banner_candidate):
            card_path = banner_candidate

    try:
        async with httpx.AsyncClient(timeout=25.0) as client:
            if card_path and os.path.exists(card_path) and len(text) <= 1024:
                data_payload = {
                    "chat_id": target,
                    "caption": text,
                    "parse_mode": "HTML"
                }
                if reply_markup:
                    data_payload["reply_markup"] = json.dumps(reply_markup)
                with open(card_path, "rb") as pf:
                    resp = await client.post(
                        f"{api_url}/sendPhoto",
                        data=data_payload,
                        files={"photo": ("promo_alert.png", pf, "image/png")}
                    )
            else:
                resp = await client.post(
                    f"{api_url}/sendMessage",
                    json={
                        "chat_id": target,
                        "text": text,
                        "parse_mode": "HTML",
                        "disable_web_page_preview": True,
                        **({"reply_markup": reply_markup} if reply_markup else {})
                    }
                )
            data = resp.json()
            if resp.status_code == 200 and data.get("ok"):
                msg_id = data.get("result", {}).get("message_id")
                if msg_id:
                    try:
                        await client.post(
                            f"{api_url}/pinChatMessage",
                            json={"chat_id": target, "message_id": msg_id, "disable_notification": False}
                        )
                    except Exception as pe:
                        logger.warning(f"Failed to auto-pin message {msg_id}: {pe}")
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
    1. Checks if any active promo ends within 12 to 30 hours (~1 day before end).
       If yes, posts the Promo Ending Alert with DealScout event ended image.
    2. Checks if any upcoming promo starts within 12 to 36 hours (~1 day before start).
       If yes, posts the Promo Starting Alert (with warm-up guide).
    3. Unpins expired coupon bulletins for ended promos.
    """
    if now is None:
        now = datetime.now(timezone.utc)

    results = []
    calendar = list(promo_tracker.calendar)
    active_promos = [p for p in calendar if p.start_date <= now <= p.end_date]

    for promo in calendar:
        # --- 1. CHECK PROMO ENDING ALERT (FINAL 30 HOURS BEFORE END) ---
        # If promo is currently active or ending tomorrow:
        if promo.start_date <= now <= promo.end_date:
            # Auto-generated recurring entries are fallback calendar filler. When a real
            # baseline/discovered event covers the same dates, only the real one may alert.
            if _is_shadowed_placeholder(promo, calendar):
                logger.info(
                    f"[PROMO NOTIFIER] Skipping placeholder '{promo.name}': "
                    "its dates are covered by a real baseline/discovered event"
                )
                continue

            time_until_end = promo.end_date - now
            # Within ~24-30 hours before end (between 0h and 30h)
            if timedelta(hours=0) < time_until_end <= timedelta(hours=30):
                continuing = _promo_that_keeps_sale_running(promo, active_promos)
                notifier_key = _campaign_notifier_key("END_ALERT", promo)
                if continuing:
                    logger.info(
                        f"[PROMO NOTIFIER] Suppressed ending alert for '{promo.name}': "
                        f"'{continuing.name}' keeps the sale running until {continuing.end_date.isoformat()}"
                    )
                elif not is_promo_notifier_already_sent(notifier_key):
                    logger.info(f"Triggering Promo Ending Alert for {promo.name} (Ends in {time_until_end.total_seconds()/3600:.1f}h)")
                    text, markup = build_promo_ending_alert(promo, now=now)
                    img_path = get_event_ended_image_path()
                    success, err, msg_id = await send_promo_alert_to_channel(
                        text, markup, bot_token, channel_id,
                        promo_title=promo.name,
                        image_path=img_path
                    )
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

            # --- 3. CHECK PROMO LAUNCH ALERT (OFFICIAL START HOUR - 08:00 AM DZ) ---
            time_since_start = now - promo.start_date
            if timedelta(hours=0) <= time_since_start <= timedelta(hours=6):
                notifier_key = _campaign_notifier_key("LAUNCH_ALERT", promo)
                if not is_promo_notifier_already_sent(notifier_key):
                    logger.info(f"Triggering Official Promo Launch Alert for {promo.name}")
                    text, markup = build_promo_launch_alert(promo)
                    img_path = get_event_started_image_path()
                    success, err, msg_id = await send_promo_alert_to_channel(
                        text, markup, bot_token, channel_id,
                        coupon_list=promo.coupon_tiers,
                        promo_title=promo.name,
                        image_path=img_path
                    )
                    if success:
                        record_promo_notifier_sent(notifier_key)
                        results.append({
                            "type": "promo_launch_alert",
                            "promo": promo.name,
                            "message_id": msg_id,
                            "status": "published"
                        })
                    else:
                        logger.error(f"Failed to post promo launch alert: {err}")

        # --- 1B. CLEAN UP PINNED COUPONS ONCE EVENT ENDS ---
        elif now > promo.end_date:
            try:
                state = load_persistent_state()
                pinned_promos = state.get("pinned_promo_events", {})
                promo_key = f"{promo.name}_{promo.start_date.strftime('%Y%m%d')}"
                pinned_id = pinned_promos.get(promo_key)
                if pinned_id:
                    token = bot_token or ADMIN_BOT_TOKEN or TELEGRAM_BOT_TOKEN
                    target = channel_id or TARGET_CHANNEL_ID
                    api_url = f"https://api.telegram.org/bot{token}"
                    async with httpx.AsyncClient(timeout=10.0) as client:
                        await client.post(
                            f"{api_url}/unpinChatMessage",
                            json={"chat_id": target, "message_id": pinned_id}
                        )
                    del pinned_promos[promo_key]
                    save_persistent_state(state)
                    logger.info(f"Unpinned expired coupon bulletin #{pinned_id} for ended promo {promo.name}")
            except Exception as ue:
                logger.debug(f"Unpin expired coupons check: {ue}")

        # --- 2. CHECK PROMO STARTING ALERT (1 DAY BEFORE START) ---
        elif now < promo.start_date:
            # Do not post coupons before the event actually starts!
            pass

    return results

async def ensure_active_promo_coupons_pinned(
    now: Optional[datetime] = None,
    bot_token: Optional[str] = None,
    channel_id: Optional[str] = None,
    force_post: bool = False
) -> Optional[int]:
    """
    Guarantees that during EVERY active promo event (e.g. Choice Day, Mega Brands),
    an official promo coupon bulletin is published and PINNED at the top of @DzAliexpress0.
    If already published and pinned for this event, verifies it remains pinned via Telegram API.
    """
    if now is None:
        now = datetime.now(timezone.utc)

    promo = promo_tracker.get_active_promo(now)
    if not promo or not promo.coupon_tiers:
        return None

    state = load_persistent_state()
    pinned_promos = state.get("pinned_promo_events", {})
    promo_key = f"{promo.name}_{promo.start_date.strftime('%Y%m%d')}"

    existing_msg_id = pinned_promos.get(promo_key)
    token = bot_token or ADMIN_BOT_TOKEN or TELEGRAM_BOT_TOKEN
    target = channel_id or TARGET_CHANNEL_ID

    # If already published for this event, re-verify it remains pinned in the channel
    if existing_msg_id and not force_post:
        try:
            api_url = f"https://api.telegram.org/bot{token}"
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    f"{api_url}/pinChatMessage",
                    json={"chat_id": target, "message_id": existing_msg_id, "disable_notification": True}
                )
                if resp.status_code == 200 and resp.json().get("ok"):
                    logger.info(f"[PROMO PIN] Verified active promo coupon bulletin #{existing_msg_id} remains PINNED for {promo.name}")
                    return existing_msg_id
        except Exception as e:
            logger.warning(f"Error checking pinned status: {e}")
        return existing_msg_id

    # Build and post the official coupon bulletin for this active event
    logger.info(f"[PROMO PIN] Publishing and pinning official event coupon bulletin for {promo.name}...")
    text, markup = build_promo_launch_alert(promo)
    img_path = get_event_started_image_path()
    success, err, msg_id = await send_promo_alert_to_channel(
        text, markup, token, target,
        coupon_list=promo.coupon_tiers,
        promo_title=promo.name,
        image_path=img_path
    )
    if success and msg_id:
        if "pinned_promo_events" not in state:
            state["pinned_promo_events"] = {}
        state["pinned_promo_events"][promo_key] = msg_id
        save_persistent_state(state)
        logger.info(f"[PROMO PIN] Successfully published & PINNED coupon bulletin for {promo.name} (Msg #{msg_id}) to {target}")
        return msg_id
    else:
        logger.error(f"[PROMO PIN] Failed to publish & pin coupon bulletin: {err}")
        return None


async def check_and_auto_post_coupon_restock_alert(
    now: Optional[datetime] = None,
    bot_token: Optional[str] = None,
    channel_id: Optional[str] = None,
    force: bool = False
) -> Optional[int]:
    """
    Autonomous 09:00 AM Coupon Restock Notifier:
    Checks if current time in Algiers (UTC+1) is around 09:00 AM (08:55 AM - 09:40 AM)
    during 11.11 sale era. If not yet posted today, publishes the official
    coupon claim & booking post with our verified affiliate links to @DzAliexpress0.
    """
    from app.publisher.state_tracker import (
        is_coupon_restock_time_window,
        is_coupon_restock_alert_eligible,
        record_coupon_restock_alert_published
    )

    dz_tz = timezone(timedelta(hours=1))
    now_dz = now.astimezone(dz_tz) if (now and now.tzinfo) else (now.replace(tzinfo=dz_tz) if now else datetime.now(dz_tz))
    today_str = now_dz.strftime("%Y-%m-%d")

    # Time window check (unless forced)
    if not force and not is_coupon_restock_time_window(now_dz):
        return None

    # Deduplication check: once per day
    if not force and not is_coupon_restock_alert_eligible(today_str):
        return None

    logger.info(f"[COUPON RESTOCK] Triggering official 09:00 AM coupon restock alert for {today_str}...")

    # Verified official affiliate links for Coupon Center and 11.11 Top Deals
    claim_url = "https://s.click.aliexpress.com/e/_c3OOlDBD"
    deals_url = "https://s.click.aliexpress.com/e/_c30KcdBp"

    text = (
        "<blockquote>🔥 <b>تجدد الكوبونات وتوفرها رسمياً الآن! سارعوا بالحجز ⤵️</b></blockquote>\n\n"
        "تتوفر الكوبونات الآن لحسابات الجزائر بكميات محدودة جداً على الساعة <b>09:00 صباحاً</b> مع انطلاق تحديثات وتخفيضات 11.11! ⏰\n\n"
        "🇩🇿 <b>ضع البلد الجزائر</b> من إعدادات التطبيق قبل الدخول للرابط.\n\n"
        "🎟️ <b>رابط صفحة حجز وجمع الكوبونات المباشر:</b>\n"
        f"👉 {claim_url}\n\n"
        "🔥 <b>رابط أقوى عروض وتخفيضات 11.11:</b>\n"
        f"👉 {deals_url}\n\n"
        "💡 <b>ادخلوا للرابط وقوموا بتحصيل (Collect) لجميع الكوبونات فوراً لتثبيتها في حساباتكم قبل نفاد الكمية! ⚡</b>\n\n"
        "لا تنسى استخدام البوت للشراء بأقل الأسعار ومضاعفة خصم العملات :\n"
        "https://t.me/Alilo07BOT\n\n"
        "قناة التليغرام للمزيد من العروض : @DzAliexpress0\n"
        "https://t.me/DzAliexpress0"
    )

    reply_markup = {
        "inline_keyboard": [
            [
                {"text": "🎟️ حجز الكوبونات المباشر", "url": claim_url}
            ],
            [
                {"text": "🪙 البوت لتخفيض الأسعار", "url": "https://t.me/Alilo07BOT"},
                {"text": "📢 قناة الصفقات الرسمية", "url": "https://t.me/DzAliexpress0"}
            ]
        ]
    }

    img_path = get_event_started_image_path()
    token = bot_token or ADMIN_BOT_TOKEN or TELEGRAM_BOT_TOKEN
    target = channel_id or TARGET_CHANNEL_ID

    success, err, msg_id = await send_promo_alert_to_channel(
        text=text,
        reply_markup=reply_markup,
        bot_token=token,
        channel_id=target,
        image_path=img_path
    )

    if success and msg_id:
        record_coupon_restock_alert_published(today_str)
        logger.info(f"[COUPON RESTOCK] Successfully published restock alert (Msg #{msg_id}) to {target}")
        return msg_id
    else:
        logger.error(f"[COUPON RESTOCK] Failed to post restock alert: {err}")
        return None
