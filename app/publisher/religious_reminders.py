"""
Religious & Spiritual Reminders Publisher for @DzAliexpress0
Publishes authentic, beautiful Islamic reminders to subscribers:
1. Jumu'ah (Friday Morning): Sending blessings upon the Prophet ﷺ (user's requested verse 33:56) & Surah Al-Kahf.
2. Jumu'ah Asr (Friday Afternoon): Hour of Response (ساعة الاستجابة) & Du'a for Muslims and Palestine.
3. Fajr Salah Reminder: Daily dawn call to prayer (04:30 - 05:45 AM Algerian Time) with rotating Hadith & Quranic verses.

All timestamps are evaluated against Algeria Local Time (Africa/Algiers, UTC+1).
Tracked persistently by date so each reminder is posted exactly once per occurrence.
"""
import os
import random
from datetime import datetime, timezone, timedelta
from typing import Optional, Tuple, Dict, Any, List
import httpx

from app.utils.logger import logger, record_system_log
from app.publisher.state_tracker import (
    is_religious_reminder_eligible,
    record_religious_reminder_published
)

TARGET_CHANNEL_ID = os.getenv("TARGET_CHANNEL_ID", "@DzAliexpress0")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8900887118:AAELbFHyV2joUO-4EJ0fPSoZurkQNuENbfY")
ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN", "8708965924:AAH7SoSX7VV3Nx_yI_J39VzWjlsc-XPgXAQ")

DZ_TIMEZONE = timezone(timedelta(hours=1))  # Algeria time is UTC+1 all year round


# ── 1. Friday Morning Reminder (الصلاة على النبي ﷺ وسنن الجمعة) ────
JUMUAH_MORNING_TEXT = """﷽
<b>﴿إِنَّ اللَّهَ وَمَلَائِكَتَهُ يُصَلُّونَ عَلَى النَّبِيِّ يَا أَيُّهَا الَّذِينَ آمَنُوا صَلُّوا عَلَيْهِ وَسَلِّمُوا تَسْلِيمًا﴾</b> 🤍🕌

اللهم صلِّ وسلّم وبارك على سيدنا وحبيبنا ونبينا محمد وعلى آله وصحبه أجمعين ﷺ ✨

🌿 <b>سُنن وفضائل يوم الجمعة المباركة:</b>
▫️ <b>الإكثار من الصلاة والسلام على رسول الله ﷺ</b>
▫️ <b>قراءة سورة الكهف</b> (نورٌ يضيء ما بين الجمعتين) 📖
▫️ <b>الغسل والتطيب والسواك</b> ولبس أحسن الثياب 🧴
▫️ <b>التبكير لصلاة الجمعة</b> والإنصات للخطبة 🕌
▫️ <b>تحري ساعة الإجابة</b> والإلحاح في الدعاء 🤲

<i>«اللهم في يوم الجمعة، نسألك فرجاً لكل صابر، وشفاءً لكل مريض، ورحمةً لكل ميت، واستجابةً لكل دعاء.. وانصر إخواننا المستضعفين في فلسطين وغزة وسائر بلاد المسلمين يا رب العالمين»</i> 🤲🇵🇸

<b>جمعة مباركة وطيبة عليكم جميعاً تقبل الله منا ومنكم صالح الأعمال 🤍</b>"""

JUMUAH_MORNING_KEYBOARD = {
    "inline_keyboard": [
        [
            {"text": "📖 تلاوة وقراءة سورة الكهف", "url": "https://quran.com/18"}
        ],
        [
            {"text": "📢 قناة الصفقات @DzAliexpress0", "url": "https://t.me/DzAliexpress0"}
        ]
    ]
}


# ── 2. Friday Asr Reminder (ساعة الاستجابة والدعاء) ─────────────────
JUMUAH_ASR_TEXT = """﷽
<b>﴿فَاذْكُرُونِي أَذْكُرْكُمْ وَاشْكُرُوا لِي وَلَا تَكْفُرُونِ﴾</b> 🤲🤍

🌿 <b>تذكير | ساعة الاستجابة في يوم الجمعة المباركة ✨</b>

قال رسول الله ﷺ:
<i>«يَوْمُ الْجُمُعَةِ اثْنَتَا عَشْرَةَ سَاعَةً، لاَ يُوجَدُ فِيهَا عَبْدٌ مُسْلِمٌ يَسْأَلُ اللَّهَ شَيْئًا إِلاَّ آتَاهُ إِيَّاهُ، فَالْتَمِسُوهَا آخِرَ سَاعَةٍ بَعْدَ الْعَصْرِ»</i> 🕌

اغتنموا هذه الدقائق المباركة بالدعاء والاستغفار والصلاة على الحبيب المصطفى ﷺ:
<b>اللهم صلِّ وسلّم وبارك على نبينا محمد ﷺ 🤍</b>

لا تنسوا والديكم وأحبابكم ومرضاكم وإخواننا المستضعفين في فلسطين وغزة وسائر بلاد المسلمين من صالح دعائكم في هذه الساعة المباركة 🤲🇵🇸"""

JUMUAH_ASR_KEYBOARD = {
    "inline_keyboard": [
        [
            {"text": "🤲 أدعية مأثورة واستغفار", "url": "https://sunnah.com"}
        ],
        [
            {"text": "📢 قناة الصفقات @DzAliexpress0", "url": "https://t.me/DzAliexpress0"}
        ]
    ]
}


# ── 3. Daily Fajr Prayer Reminders (صلاة الفجر) ─────────────────────
FAJR_VARIANTS = [
    {
        "text": """<b>الصلاة خيرٌ من النوم 🕌✨</b>

<b>﴿أَقِمِ الصَّلَاةَ لِدُلُوكِ الشَّمْسِ إِلَىٰ غَسَقِ اللَّيْلِ وَقُرْآنَ الْفَجْرِ ۖ إِنَّ قُرْآنَ الْفَجْرِ كَانَ مَشْهُودًا﴾</b>

هنيئاً لمن استيقظ تلبيةً لنداء ربه، ونفض عن عينيه لذة النوم ليفوز برضا الرحمن وبداية يومٍ مشرق في ذمة الله ورعايته 🤍

<b>صلاة الفجر أثابكم الله ونوّر قلوبكم وبيوتكم ودروبكم 🤲</b>""",
        "keyboard": {
            "inline_keyboard": [
                [{"text": "🤲 أذكار الصباح والحفظ", "url": "https://sunnah.com"}],
                [{"text": "📢 قناة الصفقات @DzAliexpress0", "url": "https://t.me/DzAliexpress0"}]
            ]
        }
    },
    {
        "text": """<b>الصلاة خيرٌ من النوم 🤍🕌</b>

قال رسول الله ﷺ:
<i>«مَنْ صَلَّى الصُّبْحَ فَهُوَ فِي ذِمَّةِ اللَّهِ»</i> ✨

وقال ﷺ:
<i>«رَكْعَتَا الْفَجْرِ خَيْرٌ مِنَ الدُّنْيَا وَمَا فِيهَا»</i> 🌿

قوموا إلى صلاتكم يرحمكم الله، واستفتحوا يومكم بالبركة والنور والسكينة والسجود بين يدي الله عز وجل..

<b>صلاة الفجر أثابكم الله، تقبل الله منا ومنكم صالح الأعمال والدعوات 🤲</b>""",
        "keyboard": {
            "inline_keyboard": [
                [{"text": "🤲 أذكار الصباح والحفظ", "url": "https://sunnah.com"}],
                [{"text": "📢 قناة الصفقات @DzAliexpress0", "url": "https://t.me/DzAliexpress0"}]
            ]
        }
    },
    {
        "text": """<b>﴿وَالصُّبْحِ إِذَا تَنَفَّسَ﴾ 🌅</b>

<b>الصلاة خيرٌ من النوم 🕌</b>

طوبى لمن استفتح يومه بصلاة الفجر وبذكر الله عز وجل ✨
ابسطوا أمانيكم في سجودكم، وتوكلوا على الحي القيوم الذي بيده مقاليد السماوات والأرض..

<b>صلاة الفجر يرحمكم الله، رزقنا الله وإياكم القبول والبركة وراحة البال 🤲</b>""",
        "keyboard": {
            "inline_keyboard": [
                [{"text": "🤲 أذكار الصباح والحفظ", "url": "https://sunnah.com"}],
                [{"text": "📢 قناة الصفقات @DzAliexpress0", "url": "https://t.me/DzAliexpress0"}]
            ]
        }
    }
]


async def post_religious_reminder(
    reminder_type: str,
    bot_token: Optional[str] = None
) -> Tuple[bool, Optional[str], Optional[int]]:
    """
    Publishes a specified religious reminder to @DzAliexpress0.
    reminder_type: 'jumuah' | 'jumuah_asr' | 'fajr'
    """
    token = bot_token or ADMIN_BOT_TOKEN or TELEGRAM_BOT_TOKEN
    target_channel = TARGET_CHANNEL_ID
    if not token or not target_channel:
        return False, "Telegram Bot Token or Target Channel not configured", None

    if reminder_type == "jumuah":
        text = JUMUAH_MORNING_TEXT
        markup = JUMUAH_MORNING_KEYBOARD
    elif reminder_type == "jumuah_asr":
        text = JUMUAH_ASR_TEXT
        markup = JUMUAH_ASR_KEYBOARD
    elif reminder_type == "fajr":
        variant = random.choice(FAJR_VARIANTS)
        text = variant["text"]
        markup = variant["keyboard"]
    else:
        return False, f"Unknown reminder type: {reminder_type}", None

    api_url = f"https://api.telegram.org/bot{token}"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"{api_url}/sendMessage",
                json={
                    "chat_id": target_channel,
                    "text": text,
                    "parse_mode": "HTML",
                    "reply_markup": markup,
                    "disable_web_page_preview": True
                }
            )
            data = resp.json()
            if resp.status_code == 200 and data.get("ok"):
                msg_id = data.get("result", {}).get("message_id")
                # Record in state tracker
                now_dz = datetime.now(DZ_TIMEZONE)
                today_str = now_dz.strftime("%Y-%m-%d")
                record_religious_reminder_published(reminder_type, today_str)

                await record_system_log(
                    "INFO",
                    "publisher",
                    f"Published religious reminder ({reminder_type}) to {target_channel} (msg #{msg_id})"
                )
                logger.info(f"Published religious reminder '{reminder_type}' to {target_channel} (msg #{msg_id})")
                return True, None, msg_id
            else:
                err = data.get("description", f"HTTP {resp.status_code}")
                logger.error(f"Failed to publish religious reminder '{reminder_type}': {err}")
                return False, err, None
    except Exception as e:
        logger.exception(f"Exception publishing religious reminder: {e}")
        return False, str(e), None


async def check_and_auto_post_religious_reminders(
    force: bool = False,
    bot_token: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Evaluates current Algerian time and publishes religious reminders if eligible:
    - Jumu'ah Morning: Fridays between 07:00 and 14:00 (or if forced on Friday).
    - Jumu'ah Asr: Fridays between 15:30 and 18:30 (Hour of response).
    - Fajr Prayer: Daily between 04:30 and 05:45 AM (Dawn).
    """
    now_dz = datetime.now(DZ_TIMEZONE)
    today_str = now_dz.strftime("%Y-%m-%d")
    is_friday = (now_dz.weekday() == 4)
    hour = now_dz.hour
    minute = now_dz.minute
    current_time_float = hour + (minute / 60.0)

    results = []

    # 1. Friday Morning Reminder (الصلاة على النبي ﷺ وسنن الجمعة)
    if is_friday:
        # Eligible between 07:00 and 14:30 Algeria time, or if forced
        in_jumuah_morning_window = (7.0 <= current_time_float <= 14.5)
        if in_jumuah_morning_window or force:
            if is_religious_reminder_eligible("jumuah", today_str) or force:
                success, err, msg_id = await post_religious_reminder("jumuah", bot_token)
                results.append({
                    "type": "jumuah",
                    "success": success,
                    "error": err,
                    "message_id": msg_id
                })

        # 2. Friday Asr Reminder (ساعة الاستجابة)
        in_jumuah_asr_window = (15.5 <= current_time_float <= 18.5)
        if in_jumuah_asr_window:
            if is_religious_reminder_eligible("jumuah_asr", today_str):
                success, err, msg_id = await post_religious_reminder("jumuah_asr", bot_token)
                results.append({
                    "type": "jumuah_asr",
                    "success": success,
                    "error": err,
                    "message_id": msg_id
                })

    # 3. Daily Fajr Salah Reminder (صلاة الفجر)
    # Fajr in Algeria is around 04:45 - 05:30 (window 04:30 to 05:45)
    in_fajr_window = (4.5 <= current_time_float <= 5.75)
    if in_fajr_window:
        if is_religious_reminder_eligible("fajr", today_str):
            success, err, msg_id = await post_religious_reminder("fajr", bot_token)
            results.append({
                "type": "fajr",
                "success": success,
                "error": err,
                "message_id": msg_id
            })

    return results
