"""
Strategic France Channel Cross-Promotion Module
Promotes the dedicated France / Europe deals channel (@francedealsdz) inside the Algerian channel (@DzAliexpress0).

User-Defined Guardrails:
1. Zero Marketing During Deal Rush: If deals are being posted heavily (>= 3 in last 4h or >= 5 in last 8h),
   marketing is STRICTLY ABORTED to keep the channel 100% focused on active bargains.
2. Low-Velocity & Quiet Hours Only: Triggers at random times during quiet night hours (22:00 - 02:30 Algiers time)
   or during daytime droughts (no deals posted for >= 6 hours).
3. Randomized Jitter: Cooldown is randomized between 48 and 96 hours (2 to 4 days) to appear completely organic.
4. Anti-Duplicate: Live channel cache is checked to ensure @francedealsdz hasn't been mentioned in recent posts.
"""
import os
import sys
import json
import random
import asyncio
from typing import Optional, Tuple, Dict, Any, List
import httpx

from app.config.settings import settings
from app.publisher.state_tracker import (
    load_persistent_state,
    is_france_cross_promo_eligible,
    record_france_cross_promo_published,
    TARGET_CHANNEL_ID
)
from app.utils.logger import logger, record_system_log
from app.utils.network import enforce_ipv4

enforce_ipv4()

TARGET_DZ_CHANNEL = os.getenv("TARGET_CHANNEL_ID", "@DzAliexpress0")
FRANCE_CHANNEL_HANDLE = os.getenv("FRANCE_TARGET_CHANNEL_ID", "@francedealsdz")
FRANCE_CHANNEL_URL = "https://t.me/francedealsdz"

# 4 High-Converting, Authentic Algerian Copywriting Variants
FRANCE_CROSS_VARIANTS: List[Dict[str, Any]] = [
    {
        "id": "family_diaspora",
        "title": "Family & Diaspora in France",
        "text": (
            "<blockquote>🇫🇷 <b>عندك فاميليا ولا صحابك عايشين في فرنسا؟</b></blockquote>\n\n"
            "بزاف من متابعينا يسقسونا على عروض وتخفيضات AliExpress الخاصة بفرنسا وأوروبا "
            "(كودات تخفيض حصرية، وتوصيل سريع في 3 إلى 5 أيام داخل أوروبا) 📦⚡\n\n"
            "خصصنالكم قناة رسمية ثانية غير لصفقات وتخفيضات فرنسا وأوروبا:\n"
            "👉 <b>@francedealsdz</b>\n\n"
            "بارطاجيوها مع لافامي لي راهم تما يستفادوا من التخفيضات والكوبونات القوية 🛍️🔥"
        ),
        "button_text": "🇫🇷 انضم لقناة صفقات فرنسا وأوروبا"
    },
    {
        "id": "caba_euro_orders",
        "title": "Caba & Euro Card Shoppers",
        "text": (
            "<blockquote>📦 <b>للناس لي تشري من فرنسا وتبعث كابة أو تسكن في أوروبا 🇪🇺</b></blockquote>\n\n"
            "كاين تخفيضات وكوبونات في AliExpress تخدم <b>فقط في فرنسا وأوروبا</b> (تخفيضات ما تمشيش في الجزائر).\n\n"
            "إذا كنت تشري ببطاقة بنكية أوروبية أو عندك شكون يجيبلك السلعة من فرنسا:\n"
            "تابـع قناتنا الثانية المخصصة لصفقات فرنسا 👇\n"
            "👉 <b>@francedealsdz</b>\n\n"
            "عروض حصرية، أكواد برومو فورية وتوصيل سريع جداً 🏃‍♂️💨"
        ),
        "button_text": "📦 تصفح صفقات فرنسا (@francedealsdz)"
    },
    {
        "id": "secret_euro_codes",
        "title": "Secret European Warehouses & Fast Shipping",
        "text": (
            "<blockquote>⚡ <b>معلومة للمتسوقين | تخفيضات AliExpress في فرنسا مختلفة تماماً!</b></blockquote>\n\n"
            "في فرنسا كاين عروض مستودعات أوروبية (Entrepôt France) السلعة توصل في 3 إلى 5 أيام وبدون جمارك، "
            "مع كوبونات خاصة (FR Codes) تخفض حتى 60€ و 80€ 💶🔥\n\n"
            "إذا عندك شخص مقيم في فرنسا أو رايح لتما، انصحه يتابع قناتنا الخاصة بفرنسا:\n"
            "👉 <b>@francedealsdz</b>\n\n"
            "صيدات يومية حصرية مخصصة فقط للأراضي الفرنسية والأوروبية 🇫🇷"
        ),
        "button_text": "💶 فتح قناة تخفيضات فرنسا"
    },
    {
        "id": "quiet_night_reminder",
        "title": "Late Night Diaspora Reminder",
        "text": (
            "<blockquote>🌙 <b>تذكير لخاوتنا في الغربة والمقيمين بفرنسا 🇫🇷🇩🇿</b></blockquote>\n\n"
            "بما أن التخفيضات والكوبونات تنطلق في أوروبا بأكواد خاصة بالجالية، "
            "خصصنالكم قناة خاصة تتبع صفقات وتخفيضات فرنسا لحظة بلحظة:\n"
            "👉 <b>@francedealsdz</b>\n\n"
            "فيها كل العروض القوية مع كودات التخفيض لي تخدم في فرنسا وأوروبا فقط 🛍️✨"
        ),
        "button_text": "✨ اضغط هنا للانضمام إلى @francedealsdz"
    }
]


async def check_and_post_france_cross_promo(force: bool = False) -> Tuple[bool, str]:
    """
    Evaluates rules and conditionally posts a France channel cross-promotion to @DzAliexpress0.
    Returns (success, message).
    """
    eligible, reason = await is_france_cross_promo_eligible(force=force)
    if not eligible:
        return False, f"Skipped: {reason}"

    bot_token = settings.TELEGRAM_BOT_TOKEN
    if not bot_token:
        return False, "TELEGRAM_BOT_TOKEN not configured"

    # Load persistent state to determine variant rotation
    state = load_persistent_state()
    prev_idx = state.get("france_cross_promo_variant_idx", 0)
    variant_idx = (prev_idx + 1) % len(FRANCE_CROSS_VARIANTS)
    variant = FRANCE_CROSS_VARIANTS[variant_idx]

    reply_markup = {
        "inline_keyboard": [
            [
                {"text": variant["button_text"], "url": FRANCE_CHANNEL_URL}
            ]
        ]
    }

    api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": TARGET_DZ_CHANNEL,
        "text": variant["text"],
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
        "reply_markup": reply_markup
    }

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.post(api_url, json=payload)
            res_data = resp.json()
            if resp.status_code == 200 and res_data.get("ok"):
                msg_id = res_data.get("result", {}).get("message_id")
                record_france_cross_promo_published(variant_idx=variant_idx)
                log_msg = f"Published France cross-promo variant '{variant['id']}' to {TARGET_DZ_CHANNEL} (Msg #{msg_id})"
                logger.info(log_msg)
                try:
                    await record_system_log("INFO", "FRANCE_CROSS_PROMO", log_msg)
                except Exception:
                    pass
                return True, log_msg
            else:
                err_desc = res_data.get("description", resp.text)
                logger.warning(f"Failed to post France cross-promo to {TARGET_DZ_CHANNEL}: {err_desc}")
                return False, f"Telegram API error: {err_desc}"
    except Exception as e:
        logger.error(f"Network error sending France cross-promo: {e}")
        return False, f"Exception: {e}"


if __name__ == "__main__":
    force_run = "--force" in sys.argv or "-f" in sys.argv
    success, msg = asyncio.run(check_and_post_france_cross_promo(force=force_run))
    print(f"Result: success={success} | {msg}")
