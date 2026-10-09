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

from app.config.settings import settings
from app.utils.logger import logger, record_system_log
from app.utils.network import enforce_ipv4
from app.publisher.state_tracker import (
    is_religious_reminder_eligible,
    record_religious_reminder_published
)

enforce_ipv4()

TARGET_CHANNEL_ID = getattr(settings, "TARGET_CHANNEL_ID", None) or os.getenv("TARGET_CHANNEL_ID", "@DzAliexpress0")
TELEGRAM_BOT_TOKEN = getattr(settings, "TELEGRAM_BOT_TOKEN", None) or os.getenv("TELEGRAM_BOT_TOKEN", "")
ADMIN_BOT_TOKEN = getattr(settings, "ADMIN_BOT_TOKEN", None) or os.getenv("ADMIN_BOT_TOKEN", "")

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
                [{"text": "🤲 أذكار الصباح والحفظ", "url": "https://sunnah.com"}]
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
                [{"text": "🤲 أذكار الصباح والحفظ", "url": "https://sunnah.com"}]
            ]
        }
    },
    {
        "text": """<b>﴿وَالصُّبْحِ إِذَا تَنَفَّسَ﴾ 🌅</b>

<b>الصلاة خيرٌ من النوم 🕌</b>

طوبى لمن استفتح يومه بصلاة الفجر وبذكر الله عز وجل ✨
ابسطوا أمانيكم في سجودكم، وتوكلوا على الحي القيوم الذي بيده مقاليد السماوات والأرض..

<b>صلاة الفجر يرحمكم الله، رزقنا الله وإياكم القبول والبركة وراحة بال 🤲</b>""",
        "keyboard": {
            "inline_keyboard": [
                [{"text": "🤲 أذكار الصباح والحفظ", "url": "https://sunnah.com"}]
            ]
        }
    }
]


# ── 4. Random Daily Dhikr & Spiritual Reminders (أذكار وأدعية مأثورة) ─────
RANDOM_DHIKR_VARIANTS = [
    {
        "text": """﷽
<b>﴿أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ﴾</b> 🤍🌿

قال رسول الله ﷺ:
<i>«كَلِمَتَانِ خَفِيفَتَانِ عَلَى اللِّسَانِ، ثَقِيلَتَانِ فِي الْمِيزَانِ، حَبِيبَتَانِ إِلَى الرَّحْمَنِ: سُبْحَانَ اللَّهِ وَبِحَمْدِهِ، سُبْحَانَ اللَّهِ الْعَظِيمِ»</i> ✨

<b>عطّروا ألسنتكم بذكر الله والصلاة على النبي ﷺ 🤲</b>""",
        "keyboard": {
            "inline_keyboard": [
                [{"text": "📖 حصن المسلم والأذكار", "url": "https://sunnah.com"}]
            ]
        }
    },
    {
        "text": """﷽
<b>﴿فَقُلْتُ اسْتَغْفِرُوا رَبَّكُمْ إِنَّهُ كَانَ غَفَّارًا ۝ يُرْسِلِ السَّمَاءَ عَلَيْكُم مِّدْرَارًا ۝ وَيُمْدِدْكُم بِأَمْوَالٍ وَبَنِينَ وَيَجْعَل لَّكُمْ جَنَّاتٍ وَيَجْعَل لَّكُمْ أَنْهَارًا﴾</b> 🤲🤍

<i>«أستغفر الله العظيم الذي لا إله إلا هو الحي القيوم وأتوب إليه»</i> ✨

استغفار يفرّج الهم، ويجلب الرزق، ويبعث السكينة في النفوس.. لا تغفلوا عنه في زحام يومكم 🌿""",
        "keyboard": {
            "inline_keyboard": [
                [{"text": "🤲 أدعية وتسابيح مأثورة", "url": "https://sunnah.com"}]
            ]
        }
    },
    {
        "text": """﷽
<b>﴿وَتَوَكَّلْ عَلَى الْحَيِّ الَّذِي لَا يَمُوتُ وَسَبِّحْ بِحَمْدِهِ﴾</b> 🤍✨

قال رسول الله ﷺ:
<i>«مَا مِنْ يَوْمٍ يُصْبِحُ الْعِبَادُ فِيهِ إِلاَّ مَلَكَانِ يَنْزِلاَنِ فَيَقُولُ أَحَدُهُمَا: اللَّهُمَّ أَعْطِ مُنْفِقًا خَلَفًا، وَيَقُولُ الآخَرُ: اللَّهُمَّ أَعْطِ مُمْسِكًا تَلَفًا»</i> 🌿

اللهم إنا نسألك رزقاً طيباً، وعملاً متقبلاً، وشفاءً لكل مريض، وفرجاً لكل صابر 🤲""",
        "keyboard": {
            "inline_keyboard": [
                [{"text": "🤍 أدعية جامعة وأذكار", "url": "https://sunnah.com"}]
            ]
        }
    },
    {
        "text": """<b>لا حَوْلَ وَلا قُوَّةَ إِلاَّ بِاللَّهِ العَلِيِّ العَظِيم 🤍🌿</b>

كنزٌ من كنوز الجنة، ومفتاح لكل بابٍ مغلق، وتفريجٌ لكل كربٍ وهم..
استعينوا بالله في كل أموركم، وتوكلوا عليه وحده، فما خاب من فوّض أمره إلى الله 🤲✨""",
        "keyboard": {
            "inline_keyboard": [
                [{"text": "📖 تلاوات وأدعية مأثورة", "url": "https://quran.com"}]
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
    reminder_type: 'jumuah' | 'jumuah_asr' | 'fajr' | 'daily_dhikr'
    """
    token = bot_token or getattr(settings, "TELEGRAM_BOT_TOKEN", None) or getattr(settings, "ADMIN_BOT_TOKEN", None) or TELEGRAM_BOT_TOKEN or ADMIN_BOT_TOKEN
    target_channel = getattr(settings, "TARGET_CHANNEL_ID", None) or TARGET_CHANNEL_ID
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
    elif reminder_type in ("daily_dhikr", "random_adhkar"):
        variant = random.choice(RANDOM_DHIKR_VARIANTS)
        text = variant["text"]
        markup = variant["keyboard"]
    else:
        return False, f"Unknown reminder type: {reminder_type}", None

    api_url = f"https://api.telegram.org/bot{token}"
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
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
    - Jumu'ah Morning: Fridays between 07:00 and 15:00 (or if forced on Friday).
    - Jumu'ah Asr: Fridays between 15:30 and 18:30 (Hour of response).
    - Fajr Prayer: Daily between 04:30 and 05:45 AM (Dawn).
    - Random Daily Dhikr: Daily on non-Fridays between 11:00 and 21:00.
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
        # Eligible between 07:00 and 15:00 Algeria time, or if forced
        in_jumuah_morning_window = (7.0 <= current_time_float <= 15.0)
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

    # 4. Random Daily Dhikr & Spiritual Reminders (On non-Fridays)
    if not is_friday:
        in_dhikr_window = (11.0 <= current_time_float <= 21.0)
        if in_dhikr_window or force:
            if is_religious_reminder_eligible("daily_dhikr", today_str) or force:
                success, err, msg_id = await post_religious_reminder("daily_dhikr", bot_token)
                results.append({
                    "type": "daily_dhikr",
                    "success": success,
                    "error": err,
                    "message_id": msg_id
                })

    return results
