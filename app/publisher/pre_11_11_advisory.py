"""
Pre-11.11 & Black Friday Warm-up & Currency Advisories
Publishes high-value buyer advisories to @DzAliexpress0 before the November mega sales (11.11 & Black Friday):
1. Currency Preparation Tip: Advising Algerian shoppers to acquire USD/EUR early before exchange rates spike in Square / P2P.
2. Budget & Card Readiness: Ensuring bank cards (RedotPay, Bybit, Paysera) and balances are loaded ahead of time.
3. Daily Coins Reservoir: Reminding shoppers to hoard AliExpress Coins daily for massive 11.11 discounts.

Strict Rules:
- Active strictly during the Pre-11.11 season (October 10th to November 10th). Never for any other event.
- Randomized interval: Once every 3 to 4 days (72 to 96 hours with randomized jitter).
"""
import os
import sys
import json
import httpx
from datetime import datetime, timezone
from typing import Optional, Tuple, Dict, Any, List
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app.config.settings import settings
from app.publisher.state_tracker import (
    load_persistent_state,
    is_pre_11_11_season,
    is_pre_11_11_advisory_eligible,
    record_pre_11_11_advisory_published,
    TARGET_CHANNEL_ID
)
from app.utils.logger import logger

# --- VARIANT 0: Direct Match to Channel Screenshot ---
VARIANT_0_EXACT = """<blockquote>⚠️ <b>باقي أقل من شهر على التخفيضات الكبرى لـ AliExpress في نوفمبر (11/11 و Black Friday)! 🔥</b></blockquote>

<blockquote>✅ <b>لهذا ننصح أي شخص يريد الاستفادة من هذه التخفيضات بشراء الدولار والأورو من الآن، لأن الأسعار سوف ترتفع في الأيام القادمة وتصل مستويات عالية في وقت التخفيضات.</b></blockquote>

💡 <i>جهز ميزانيتك وبطاقتك من الآن حتى لا تفوتك أضخم صفقات السنة!</i>
━━━━━━━━━━━━━━━━━
🪙 <b>بوت تخفيض العملات المباشر:</b> @Alilo07BOT
📢 <b>قناة الصفقات المعتمدة:</b> @DzAliexpress0"""

# --- VARIANT 1: Budget, Currency Rate Surge Advisory & Card Readiness ---
VARIANT_1_CURRENCY_STRATEGY = """<blockquote>🚨 <b>تنبيه هام واستعداد لمهرجان نوفمبر الأسطوري 11/11 و Black Friday 🛍️🔥</b></blockquote>

مع اقتراب أضخم فترة تخفيضات في السنة على AliExpress:

💵 <b>سوق الصرف (الدولار والأورو):</b> الطلب يتضاعف بشكل قياسي خلال أسابيع التخفيضات، مما يؤدي عادةً لارتفاع أسعار العملة الصعبة. ننصحكم بتوفير وشحن رصيدكم من الآن لتفادي أي زيادة!
💳 <b>البطاقات البنكية:</b> تأكدوا من جاهزية بطاقاتكم وتفعيلها لتكونوا في الموعد لاقتناص الكوبونات والصفقات الحصرية فور انطلاقها.

💡 <i>التسوق الذكي يبدأ بالتخطيط المبكر.. وفّر دراهمك واستعد لأقوى التخفيضات.</i>
━━━━━━━━━━━━━━━━━
🪙 <b>بوت تخفيض العملات المباشر:</b> @Alilo07BOT
📢 <b>قناة الصفقات المعتمدة:</b> @DzAliexpress0"""

# --- VARIANT 2: Coins Reservoir + Countdown to 11.11 ---
VARIANT_2_COINS_COUNTDOWN = """<blockquote>⏳ <b>العد التنازلي للتخفيضات الكبرى 11/11 و الجمعة السوداء Black Friday 🛒💥</b></blockquote>

باقي أسابيع قليلة على انطلاق أقوى حدث تسوق سنوي على AliExpress:

1️⃣ <b>وفّر الدولار والأورو من الآن:</b> تفادياً لارتفاع أسعار الصرف مع ذروة الطلب في نوفمبر.
2️⃣ <b>اجمع رصيد العملات (Coins) يومياً:</b> ادخل للتطبيق يومياً واجمع العملات، لأنها في 11.11 ستمنحك خصماً إضافياً يصل حتى <b>50% وأكثر</b> على عتاد القيمنق والهواتف!

📌 <i>ثبّتوا القناة وجهزوا ميزانيتكم، سنكون معكم بتغطية حصرية لأقوى الكوبونات والصفقات أولاً بأول!</i>
━━━━━━━━━━━━━━━━━
🪙 <b>بوت تخفيض العملات المباشر:</b> @Alilo07BOT
📢 <b>قناة الصفقات المعتمدة:</b> @DzAliexpress0"""

PRE_11_11_VARIANTS: List[Dict[str, Any]] = [
    {
        "id": "exact_advisory",
        "text": VARIANT_0_EXACT,
        "buttons": [
            [{"text": "🪙 فتح بوت تخفيض العملات", "url": "https://t.me/Alilo07BOT"}],
            [{"text": "📢 قناة الصفقات المعتمدة", "url": "https://t.me/DzAliexpress0"}]
        ]
    },
    {
        "id": "currency_strategy",
        "text": VARIANT_1_CURRENCY_STRATEGY,
        "buttons": [
            [{"text": "🪙 فتح بوت تخفيض العملات", "url": "https://t.me/Alilo07BOT"}],
            [{"text": "📢 قناة الصفقات المعتمدة", "url": "https://t.me/DzAliexpress0"}]
        ]
    },
    {
        "id": "coins_countdown",
        "text": VARIANT_2_COINS_COUNTDOWN,
        "buttons": [
            [{"text": "🪙 جمع وتخفيض العملات", "url": "https://t.me/Alilo07BOT"}],
            [{"text": "📢 قناة الصفقات المعتمدة", "url": "https://t.me/DzAliexpress0"}]
        ]
    }
]


async def check_and_auto_post_pre_11_11_advisory(
    bot_token: Optional[str] = None,
    force: bool = False
) -> Tuple[bool, str, Optional[int]]:
    """
    Evaluates Pre-11.11 season and randomized 3-4 days cooldown, publishing an advisory to @DzAliexpress0.
    Returns (success, message, message_id).
    """
    token = bot_token or getattr(settings, "TELEGRAM_BOT_TOKEN", None) or getattr(settings, "ADMIN_BOT_TOKEN", None) or os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("ADMIN_BOT_TOKEN")
    if not token:
        return False, "TELEGRAM_BOT_TOKEN not configured", None

    target = TARGET_CHANNEL_ID
    eligible, reason = await is_pre_11_11_advisory_eligible(force=force)
    if not eligible:
        return False, f"Skipping Pre-11.11 advisory: {reason}", None

    state = load_persistent_state()
    current_idx = state.get("pre_11_11_variant_idx", 0)
    variant = PRE_11_11_VARIANTS[current_idx % len(PRE_11_11_VARIANTS)]

    reply_markup = {"inline_keyboard": variant["buttons"]}
    api_url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": str(target),
        "text": variant["text"],
        "parse_mode": "HTML",
        "reply_markup": reply_markup,
        "disable_web_page_preview": True
    }

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.post(api_url, json=payload)
            data = resp.json()

            if resp.status_code == 200 and data.get("ok"):
                msg_id = data["result"]["message_id"]
                next_idx = (current_idx + 1) % len(PRE_11_11_VARIANTS)
                record_pre_11_11_advisory_published(variant_idx=next_idx)
                logger.info(f"[PRE-11.11 ADVISORY] Successfully posted variant '{variant['id']}' to {target} (Msg #{msg_id})")
                return True, f"Posted variant '{variant['id']}' (Msg #{msg_id})", msg_id
            else:
                err_desc = data.get("description", "Unknown Telegram API error")
                logger.error(f"[PRE-11.11 ADVISORY] Failed to post: {err_desc}")
                return False, f"Telegram API error: {err_desc}", None
    except Exception as e:
        logger.error(f"[PRE-11.11 ADVISORY] Exception during publishing: {e}")
        return False, f"Network/Publishing exception: {e}", None
