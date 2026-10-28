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
JUMUAH_MORNING_TEXT = """<blockquote><b>بِسْمِ اللَّـهِ الرَّحْمَـٰنِ الرَّحِيمِ</b>

﴿ إِنَّ اللَّهَ وَمَلَائِكَتَهُ يُصَلُّونَ عَلَى النَّبِيِّ يَا أَيُّهَا الَّذِينَ آمَنُوا صَلُّوا عَلَيْهِ وَسَلِّمُوا تَسْلِيمًا ﴾</blockquote> 🤍🕌

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
JUMUAH_ASR_TEXT = """<blockquote><b>بِسْمِ اللَّـهِ الرَّحْمَـٰنِ الرَّحِيمِ</b>

﴿ فَاذْكُرُونِي أَذْكُرْكُمْ وَاشْكُرُوا لِي وَلَا تَكْفُرُونِ ﴾</blockquote> 🤲🤍

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

<blockquote><b>بِسْمِ اللَّـهِ الرَّحْمَـٰنِ الرَّحِيمِ</b>

﴿ أَقِمِ الصَّلَاةَ لِدُلُوكِ الشَّمْسِ إِلَىٰ غَسَقِ اللَّيْلِ وَقُرْآنَ الْفَجْرِ ۖ إِنَّ قُرْآنَ الْفَجْرِ كَانَ مَشْهُودًا ﴾</blockquote>

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
        "text": """<blockquote><b>بِسْمِ اللَّـهِ الرَّحْمَـٰنِ الرَّحِيمِ</b>

﴿ أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ ﴾</blockquote> 🤍🌿

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
        "text": """<blockquote><b>بِسْمِ اللَّـهِ الرَّحْمَـٰنِ الرَّحِيمِ</b>

﴿ فَقُلْتُ اسْتَغْفِرُوا رَبَّكُمْ إِنَّهُ كَانَ غَفَّارًا • يُرْسِلِ السَّمَاءَ عَلَيْكُم مِّدْرَارًا • وَيُمْدِدْكُم بِأَمْوَالٍ وَبَنِينَ وَيَجْعَل لَّكُمْ جَنَّاتٍ وَيَجْعَل لَّكُمْ أَنْهَارًا ﴾</blockquote> 🤲🤍

«<b>أستغفر الله العظيم الذي لا إله إلا هو الحي القيوم وأتوب إليه</b>» ✨

استغفار يفرّج الهم، ويجلب الرزق، ويبعث السكينة في النفوس.. لا تغفلوا عنه في زحام يومكم 🌿""",
        "keyboard": {
            "inline_keyboard": [
                [{"text": "🤲 أدعية وتسابيح مأثورة", "url": "https://sunnah.com"}]
            ]
        }
    },
    {
        "text": """<blockquote><b>بِسْمِ اللَّـهِ الرَّحْمَـٰنِ الرَّحِيمِ</b>

﴿ وَتَوَكَّلْ عَلَى الْحَيِّ الَّذِي لَا يَمُوتُ وَسَبِّحْ بِحَمْدِهِ ﴾</blockquote> 🤍✨

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



# ── 5. Major Islamic Events (أعياد ومناسبات إسلامية كبرى) ──────────────────
EID_FITR_TEXT = """<blockquote><b>بِسْمِ اللَّـهِ الرَّحْمَـٰنِ الرَّحِيمِ</b>

﴿ وَلِتُكَبِّرُوا اللَّهَ عَلَىٰ مَا هَدَاكُمْ وَلَعَلَّكُمْ تَشْكُرُونَ ﴾</blockquote> 🌙✨

<b>عيد فطر مبارك وسعيد عليكم وعلى عائلاتكم الكريمة 🤍🎉</b>

تقبل الله منا ومنكم الصيام والقيام وصالح الأعمال والدعوات..
أعاده الله علينا وعليكم وعلى الأمة الإسلامية جمعاء بالخير واليُمن والبركات، وفرّج كرب إخواننا المستضعفين في فلسطين وسائر بلاد المسلمين يا رب العالمين 🤲🇩🇿🇵🇸

<b>كل عام وأنتم بخير وصحة وعافية ✨</b>"""

EID_ADHA_TEXT = """<blockquote><b>بِسْمِ اللَّـهِ الرَّحْمَـٰنِ الرَّحِيمِ</b>

﴿ فَصَلِّ لِرَبِّكَ وَانْحَرْ ﴾</blockquote> 🐑✨

<b>عيد أضحى مبارك وسعيد تقبل الله طاعاتكم وصالح أعمالكم 🤍🎉</b>

نسأل الله تعالى أن يتقبل منا ومنكم ومن حجاج بيت الله الحرام، وأن يعيده علينا وعليكم بالخير والبركة واليُمن والسلام..
ولا تنسوا إخوانكم في فلسطين وغزة من صالح دعائكم في هذه الأيام الفضيلة 🤲🇵🇸

<b>صحّ عيدكم وكل عام وأنتم بخير 🇩🇿✨</b>"""

RAMADAN_TEXT = """<blockquote><b>بِسْمِ اللَّـهِ الرَّحْمَـٰنِ الرَّحِيمِ</b>

﴿ شَهْرُ رَمَضَانَ الَّذِي أُنزِلَ فِيهِ الْقُرْآنُ هُدًى لِّلنَّاسِ وَبَيِّنَاتٍ مِّنَ الْهُدَىٰ وَالْفُرْقَانِ ﴾</blockquote> 🌙✨

<b>مبارك عليكم شهر رمضان الفضيل 🤍🕌</b>

نسأل الله العلي القدير أن يوفقنا وإياكم لصيامه وقيامه إيماناً واحتساباً، وأن يجعلنا وإياكم ووالدينا من عتقائه من النار..
رمضان مبارك وطيب على الأمة الإسلامية جمعاء 🤲✨"""

MAWLID_TEXT = """<blockquote><b>بِسْمِ اللَّـهِ الرَّحْمَـٰنِ الرَّحِيمِ</b>

﴿ وَمَا أَرْسَلْنَاكَ إِلَّا رَحْمَةً لِّلْعَالَمِينَ ﴾</blockquote> 🤍✨

<b>ذكرى المولد النبوي الشريف ﷺ 🕌</b>

عطّروا قلوبكم وألسنتكم بالصلاة والسلام على سيد الخلق وخاتم الأنبياء والمرسلين، نبينا وحبيبنا محمد ﷺ:
<b>اللهم صلِّ وسلّم وبارك على سيدنا محمد وعلى آله وصحبه أجمعين ﷺ 🌿</b>"""

ASHURA_TEXT = """<blockquote><b>بِسْمِ اللَّـهِ الرَّحْمَـٰنِ الرَّحِيمِ</b></blockquote> 🤍✨

🌿 <b>تذكير | فضل صيام يوم عاشوراء 🕌</b>

قال رسول الله ﷺ:
<i>«صِيَامُ يَوْمِ عَاشُورَاءَ أَحْتَسِبُ عَلَى اللَّهِ أَنْ يُكَفِّرَ السَّنَةَ الَّتِي قَبْلَهُ»</i> ✨

تقبل الله منا ومنكم صالح الأعمال والدعوات، وغفر لنا ولكم ووفقنا لكل خير 🤲"""

async def post_religious_reminder(
    reminder_type: str,
    bot_token: Optional[str] = None
) -> Tuple[bool, Optional[str], Optional[int]]:
    """
    Publishes a specified religious reminder to @DzAliexpress0.
    reminder_type: 'jumuah' | 'jumuah_asr' | 'eid_fitr' | 'eid_adha' | 'ramadan_start' | 'mawlid' | 'ashura' | 'fajr' | 'daily_dhikr'
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
    elif reminder_type == "eid_fitr":
        text = EID_FITR_TEXT
        markup = None
    elif reminder_type == "eid_adha":
        text = EID_ADHA_TEXT
        markup = None
    elif reminder_type == "ramadan_start":
        text = RAMADAN_TEXT
        markup = None
    elif reminder_type == "mawlid":
        text = MAWLID_TEXT
        markup = None
    elif reminder_type == "ashura":
        text = ASHURA_TEXT
        markup = None
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
    Evaluates current Algerian time and publishes religious reminders if eligible.
    STRICT POLICY:
    - Jumu'ah (Fridays): Morning blessings & Asr hour of response.
    - Major Islamic Events: Eid al-Fitr, Eid al-Adha, Ramadan start, Mawlid an-Nabi, Ashura.
    - Daily weekday reminders (Fajr, Daily Dhikr) are COMPLETELY DISABLED from automated posting
      to keep the channel focused exclusively on deals.
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
        if in_jumuah_asr_window or force:
            if is_religious_reminder_eligible("jumuah_asr", today_str) or force:
                success, err, msg_id = await post_religious_reminder("jumuah_asr", bot_token)
                results.append({
                    "type": "jumuah_asr",
                    "success": success,
                    "error": err,
                    "message_id": msg_id
                })

    # 3. Major Islamic Events (Exact calendar dates)
    MAJOR_ISLAMIC_DATES = {
        # Ramadan start
        "2026-02-18": "ramadan_start",
        "2027-02-08": "ramadan_start",
        # Eid al-Fitr
        "2026-03-20": "eid_fitr",
        "2027-03-10": "eid_fitr",
        # Eid al-Adha
        "2026-05-27": "eid_adha",
        "2027-05-17": "eid_adha",
        # Ashura
        "2026-06-26": "ashura",
        "2027-06-16": "ashura",
        # Mawlid an-Nabi
        "2026-08-25": "mawlid",
        "2027-08-15": "mawlid",
    }
    if today_str in MAJOR_ISLAMIC_DATES:
        ev_type = MAJOR_ISLAMIC_DATES[today_str]
        in_event_window = (8.0 <= current_time_float <= 20.0)
        if in_event_window or force:
            if is_religious_reminder_eligible(ev_type, today_str) or force:
                success, err, msg_id = await post_religious_reminder(ev_type, bot_token)
                results.append({
                    "type": ev_type,
                    "success": success,
                    "error": err,
                    "message_id": msg_id
                })

    return results
