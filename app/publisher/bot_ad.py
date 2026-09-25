"""
Coins & Bot Educational Reminders (Randomized Rotation)
Publishes high-converting, value-packed reminders to @DzAliexpress0:
1. PC / Laptop Shopper Guide: How to easily get max Coins discounts on computers using @Alilo07BOT.
2. Daily Coins Habit & Future Sales Reservoir: Reminding shoppers to claim daily coins before big promo events.
3. Windows/PC Automated Daily Collector: Highlighting the 1-command open-source script on GitHub.

Throttled to run at randomized intervals (every 48–72 hours) during active Algerian shopping hours.
"""
import asyncio
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional, Tuple, Dict, Any, List
import json
import httpx
from sqlalchemy import select

from app.config.settings import settings
from app.db.session import db_context
from app.db.models import Deal, TelegramPost
from app.publisher.state_tracker import (
    load_persistent_state,
    is_coin_reminder_eligible,
    record_coin_reminder_published
)
from app.utils.logger import logger, record_system_log

# --- VARIANT 0: PC & Laptop Shoppers Guide ---
POST_PC_GUIDE = """<blockquote>💻 <b>دليل متسوقي الحاسوب (PC / Laptop) | تفعيل أقصى تخفيض عملات عبر البوت!</b></blockquote>

الكثير من متسوقي AliExpress عبر الكمبيوتر أو اللابتوب يفوتهم خصم العملات (Coins Discount) لأن متصفح الويب العادي لا يُظهر عادةً الخصم المضاعف المخصص لتطبيق الهاتف.

🛠️ <b>كيف تشتري بأقل سعر من الكمبيوتر في 3 خطوات بسيطة:</b>
1️⃣ <b>نسخ الرابط:</b> افتح صفحة المنتج في متصفح الحاسوب (Chrome / Edge / Firefox) وانسخ رابطه (Copy URL).
2️⃣ <b>إرساله للبوت:</b> افتح تيليجرام على حاسوبك (Telegram Web أو Desktop) وأرسل الرابط للبوت: @Alilo07BOT
3️⃣ <b>الطلب المباشر:</b> يرسل لك البوت فوراً رابط صفحة العملات الخاصة (Coin Index)؛ اضغط عليه ليفتح لك صفحة المنتج بأقصى نسبة تخفيض للعملات، أو امسح الباركود بهاتفك لإتمام الشراء فوراً!

💡 <i>لا تشترِ أي منتج من الحاسوب بالسعر الكامل.. دع البوت يقتنص لك أفضل خصم في ثوانٍ.</i>
━━━━━━━━━━━━━━━━━
🪙 <b>بوت تخفيض العملات المباشر:</b> @Alilo07BOT
📢 <b>قناة الصفقات المعتمدة:</b> @DzAliexpress0"""

# --- VARIANT 1: Daily Coins Habit & Future Sales Reservoir ---
POST_DAILY_COINS = """<blockquote>🪙 <b>تذكير ذكي | اجمع رصيد عملاتك اليومية للتخفيضات الكبرى القادمة!</b></blockquote>

معظم المتسوقين ينتظرون حتى انطلاق التخفيضات الكبرى (مثل Choice Day أو 11.11) ثم يتفاجأون بأن رصيد عملاتهم صفر، فيضيع عليهم خصم مباشر يصل إلى <b>40% إلى 60% إضافية</b>!

📈 <b>كيف تجهز حسابك لافتراس الصفقات؟</b>
▫️ <b>الدخول اليومي:</b> افتح تطبيق AliExpress يومياً واضغط على قسم <b>Coins</b> لجمع 40 إلى 70 قطعة مجانية في 5 ثوانٍ فقط.
▫️ <b>تجميع الرصيد:</b> خلال شهر واحد ستجمع أكثر من 2,000 قطعة نقدية، مما يمنحك توفيراً حقيقياً يتراوح بين 15$ و 40$ في مشترياتك القادمة!
▫️ <b>تفعيل الخصم:</b> عند اختيارك لأي منتج، مرر رابطه عبر بوت @Alilo07BOT ليجبر النظام على خصم كامل رصيد عملاتك دفعة واحدة!

💡 <i>العملات المجانية هي سلاحك السري لشراء عتاد القيمنق والإلكترونيات بنصف سعرها.</i>
━━━━━━━━━━━━━━━━━
🪙 <b>بوت تفعيل وتضخيم خصم العملات:</b> @Alilo07BOT
📢 <b>قناة الصفقات المعتمدة:</b> @DzAliexpress0"""

# --- VARIANT 2: Windows Automated Daily Collector ---
POST_PC_COLLECTOR = """<blockquote>⚡ <b>حيلة أصحاب الحواسيب | اجمع عملات AliExpress يومياً بدون فتح التطبيق!</b></blockquote>

إذا كنت تنسى الدخول اليومي لتطبيق الهاتف لجمع العملات، يمكنك تشغيل أداة جمع العملات التلقائية المفتوحة المصدر على حاسوبك الشخصي:

💻 <b>مميزات الأداة:</b>
▫️ تعمل في الخلفية على الويندوز وتجمع رصيدك اليومي تلقائياً كل 24 ساعة.
▫️ آمنة 100% ومفتوحة المصدر على GitHub، ولا تتطلب سوى أمر تشغيل واحد وسهل.
▫️ ترسل لك إشعاراً يومياً على تيليجرام بما تم جمعه!

🔗 <b>رابط المشروع وطريقة التثبيت السريعة:</b>
https://github.com/1khvled/COIN-BOT-
━━━━━━━━━━━━━━━━━
🪙 <b>وعند الرغبة بالشراء، استعن دائماً بالبوت:</b> @Alilo07BOT
📢 <b>قناة الصفقات المعتمدة:</b> @DzAliexpress0"""

REMINDER_VARIANTS: List[Dict[str, Any]] = [
    {
        "id": "pc_guide",
        "caption": POST_PC_GUIDE,
        "buttons": [
            [{"text": "🪙 جرب بوت تخفيض العملات @Alilo07BOT", "url": "https://t.me/Alilo07BOT"}],
            [{"text": "📢 تابع أحدث العروض @DzAliexpress0", "url": "https://t.me/DzAliexpress0"}]
        ]
    },
    {
        "id": "daily_coins",
        "caption": POST_DAILY_COINS,
        "buttons": [
            [{"text": "🪙 افتح البوت لتخفيض أي رابط @Alilo07BOT", "url": "https://t.me/Alilo07BOT"}],
            [{"text": "📢 تابع أحدث العروض @DzAliexpress0", "url": "https://t.me/DzAliexpress0"}]
        ]
    },
    {
        "id": "pc_collector",
        "caption": POST_PC_COLLECTOR,
        "buttons": [
            [{"text": "🪙 بوت تخفيض العملات @Alilo07BOT", "url": "https://t.me/Alilo07BOT"}],
            [{"text": "⚡ كود جامع العملات للحاسوب (GitHub)", "url": "https://github.com/1khvled/COIN-BOT-"}],
            [{"text": "📢 تابع أحدث العروض @DzAliexpress0", "url": "https://t.me/DzAliexpress0"}]
        ]
    }
]

def get_next_coin_reminder_variant(variant_idx: Optional[int] = None) -> Tuple[Dict[str, Any], int]:
    """Returns the variant to post, either specified or rotated from state."""
    state = load_persistent_state()
    idx = variant_idx if variant_idx is not None else state.get("coin_reminder_variant_idx", 0)
    idx = idx % len(REMINDER_VARIANTS)
    return REMINDER_VARIANTS[idx], idx

async def post_bot_advertisement(force: bool = False, variant_idx: Optional[int] = None) -> Tuple[bool, Optional[str]]:
    """
    Publishes the rotating Coin & PC guide educational reminder to @DzAliexpress0.
    Enforces randomized 48–72h cooldown unless force=True.
    """
    if not force:
        eligible, reason = await is_coin_reminder_eligible(min_hours=48.0)
        if not eligible:
            return False, reason

    now = datetime.now(timezone.utc)
    variant, used_idx = get_next_coin_reminder_variant(variant_idx)

    # Prepare banner image
    banner_path = settings.BASE_DIR / "assets" / "bot_promo_banner.jpg"
    if not banner_path.exists():
        banner_path = settings.BASE_DIR / "assets" / "logo.png"

    bot_token = settings.TELEGRAM_BOT_TOKEN
    target_channel = settings.TARGET_CHANNEL_ID
    if not bot_token or not target_channel:
        return False, "Bot credentials not configured"

    reply_markup = {"inline_keyboard": variant["buttons"]}
    reply_markup_json = json.dumps(reply_markup)

    api_url = f"https://api.telegram.org/bot{bot_token}"
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            if banner_path.exists():
                with open(banner_path, "rb") as f:
                    data = {
                        "chat_id": target_channel,
                        "caption": variant["caption"],
                        "parse_mode": "HTML",
                        "reply_markup": reply_markup_json
                    }
                    files = {"photo": f}
                    resp = await client.post(f"{api_url}/sendPhoto", data=data, files=files)
            else:
                data = {
                    "chat_id": target_channel,
                    "text": variant["caption"],
                    "parse_mode": "HTML",
                    "reply_markup": reply_markup_json,
                    "disable_web_page_preview": True
                }
                resp = await client.post(f"{api_url}/sendMessage", data=data)

            result = resp.json()
            if resp.status_code == 200 and result.get("ok"):
                msg_id = result.get("result", {}).get("message_id")

                # Record in persistent state (rotates index and randomizes next cooldown)
                record_coin_reminder_published()

                # Record in DB
                async with db_context() as session:
                    deal = Deal(
                        product_id=f"COIN_REMINDER_{variant['id'].upper()}_{now.strftime('%Y%m%d')}",
                        original_url="https://t.me/Alilo07BOT",
                        normalized_url="https://t.me/Alilo07BOT",
                        affiliate_url="https://t.me/Alilo07BOT",
                        title=f"تذكير عملات وبوت ({variant['id']})",
                        quality_score=100,
                        status="PUBLISHED"
                    )
                    session.add(deal)
                    await session.flush()

                    post = TelegramPost(
                        deal_id=deal.id,
                        telegram_message_id=msg_id,
                        channel_id=str(target_channel),
                        status="PUBLISHED",
                        published_at=now,
                        permalink=f"https://t.me/{str(target_channel).lstrip('@')}/{msg_id}"
                    )
                    session.add(post)
                    await session.commit()

                logger.info(f"Published educational Coin Reminder ({variant['id']}) to {target_channel} (msg #{msg_id})")
                await record_system_log("INFO", "publisher", f"Published coin reminder ({variant['id']}) to {target_channel} (msg #{msg_id})")
                return True, f"Published variant '{variant['id']}' (Msg #{msg_id})"
            else:
                err = result.get("description", f"HTTP {resp.status_code}")
                logger.error(f"Failed to publish coin reminder: {err}")
                return False, err

    except Exception as e:
        logger.exception(f"Exception publishing coin reminder: {e}")
        return False, str(e)
