"""
AliExpress Global Promotions & Promo Codes Tracker (Autonomous Event Knower)
Tracks official AliExpress sale festivals, Choice Day events, active coupons,
and validates deal freshness to prevent posting expired deals or outdated coupons.

Features:
1. Perpetual Recurring Event Generator (Choice Day 1st-8th, Brand Day 9th-13th, Mega festivals).
2. Autonomous Live Event Sniffer (Extracts event names, date ranges, and coupon tiers from Arabic, French, and English text).
3. Persistent Dynamic Event Database (storage/state/dynamic_events.json).
4. Auto-prioritizing Unified Calendar (Discovered > Baseline > Recurring).
"""
import os
import re
import json
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Any

from app.config.settings import settings
from app.utils.logger import logger


@dataclass
class PromoEvent:
    name: str
    name_ar: str
    start_date: datetime
    end_date: datetime
    banner_tag: str
    is_major: bool
    coupon_tiers: List[Dict[str, str]]
    name_fr: Optional[str] = None
    coupon_tiers_fr: Optional[List[Dict[str, str]]] = None
    banner_image_url: Optional[str] = None
    source: str = "baseline"  # "baseline", "recurring", "discovered"
    event_key: Optional[str] = None

    def get_event_key(self) -> str:
        if self.event_key:
            return self.event_key
        clean = re.sub(r'[^a-zA-Z0-9]', '_', self.name).strip('_')
        return f"{clean}_{self.start_date.strftime('%Y%m%d')}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "name_ar": self.name_ar,
            "name_fr": self.name_fr or self.name,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "banner_tag": self.banner_tag,
            "is_major": self.is_major,
            "coupon_tiers": self.coupon_tiers or [],
            "coupon_tiers_fr": self.coupon_tiers_fr or [],
            "banner_image_url": self.banner_image_url,
            "source": self.source,
            "event_key": self.get_event_key(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PromoEvent":
        start_date = datetime.fromisoformat(data["start_date"])
        if start_date.tzinfo is None:
            start_date = start_date.replace(tzinfo=timezone.utc)
        end_date = datetime.fromisoformat(data["end_date"])
        if end_date.tzinfo is None:
            end_date = end_date.replace(tzinfo=timezone.utc)
        return cls(
            name=data["name"],
            name_ar=data.get("name_ar", data["name"]),
            name_fr=data.get("name_fr", data["name"]),
            start_date=start_date,
            end_date=end_date,
            banner_tag=data.get("banner_tag", f"🎯 {data['name']}"),
            is_major=data.get("is_major", True),
            coupon_tiers=data.get("coupon_tiers", []),
            coupon_tiers_fr=data.get("coupon_tiers_fr", []),
            banner_image_url=data.get("banner_image_url"),
            source=data.get("source", "discovered"),
            event_key=data.get("event_key")
        )


# Comprehensive Multilingual Month Mapping
MONTH_MAP = {
    # French
    "janvier": 1, "janv": 1, "jan": 1, "février": 2, "fevrier": 2, "fevr": 2, "mars": 3, "mar": 3,
    "avril": 4, "avr": 4, "mai": 5, "juin": 6, "juillet": 7, "juil": 7, "jul": 7,
    "août": 8, "aout": 8, "septembre": 9, "sept": 9, "sep": 9, "octobre": 10, "oct": 10,
    "novembre": 11, "nov": 11, "décembre": 12, "decembre": 12, "dec": 12,
    # Arabic (Algerian, Maghreb, Middle Eastern)
    "جانفي": 1, "يناير": 1, "كانون الثاني": 1,
    "فيفري": 2, "فبراير": 2, "شباط": 2,
    "مارس": 3, "آذار": 3, "اذار": 3,
    "أفريل": 4, "افريل": 4, "ابريل": 4, "إبريل": 4, "نيسان": 4,
    "ماي": 5, "مايو": 5, "أيار": 5, "ايار": 5,
    "جوان": 6, "يونيو": 6, "حزيران": 6,
    "جويلية": 7, "يوليو": 7, "جولاي": 7, "تموز": 7,
    "أوت": 8, "اوت": 8, "أغسطس": 8, "اغسطس": 8, "آب": 8, "اب": 8,
    "سبتمبر": 9, "أيلول": 9, "ايلول": 9,
    "أكتوبر": 10, "اكتوبر": 10, "تشرين الأول": 10, "تشرين الاول": 10,
    "نوفمبر": 11, "تشرين الثاني": 11,
    "ديسمبر": 12, "كانون الأول": 12, "كانون الاول": 12,
    # English
    "january": 1, "february": 2, "feb": 2, "march": 3,
    "april": 4, "apr": 4, "may": 5, "june": 6, "jun": 6,
    "july": 7, "august": 8, "aug": 8, "september": 9,
    "october": 10, "november": 11, "december": 12,
}

ARABIC_MONTH_NAMES = {
    1: "جانفي", 2: "فيفري", 3: "مارس", 4: "أفريل", 5: "ماي", 6: "جوان",
    7: "جويلية", 8: "أوت", 9: "سبتمبر", 10: "أكتوبر", 11: "نوفمبر", 12: "ديسمبر"
}

FRENCH_MONTH_NAMES = {
    1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril", 5: "Mai", 6: "Juin",
    7: "Juillet", 8: "Août", 9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"
}

KNOWN_EVENT_PATTERNS = [
    {
        "key": "choice_day",
        "name": "Choice Day",
        "name_ar": "تخفيضات Choice Day الشهيرة 🎯",
        "name_fr": "AliExpress Choice Day 🎯",
        "banner_tag": "🎯 Choice Day Sale",
        "is_major": True,
        "keywords": ["choice day", "شويس داي", "party ready", "شويس داى", "choice"]
    },
    {
        "key": "brand_day",
        "name": "Brand Day Sale",
        "name_ar": "مهرجان Brand Day للعلامات التجارية 🏷️",
        "name_fr": "AliExpress Brand Day 🏷️",
        "banner_tag": "🏷️ Brand Day Sale",
        "is_major": True,
        "keywords": ["brand day", "براند داي", "mega brands", "brands day"]
    },
    {
        "key": "11_11",
        "name": "11.11 Global Shopping Festival",
        "name_ar": "مهرجان 11.11 الأكبر عالمياً 🛍️🔥",
        "name_fr": "Festival Mondial 11.11 AliExpress 🛍️🔥",
        "banner_tag": "🔥 أقوى تخفيضات السنة 11.11",
        "is_major": True,
        "keywords": ["11.11", "double 11", "عالمي 11.11", "تخفيضات 11.11", "مهرجان 11.11", "singles day"]
    },
    {
        "key": "black_friday",
        "name": "Black Friday & Cyber Monday",
        "name_ar": "تخفيضات الجمعة السوداء Black Friday 🖤",
        "name_fr": "Black Friday & Cyber Monday AliExpress 🖤",
        "banner_tag": "🖤 Black Friday السنوي",
        "is_major": True,
        "keywords": ["black friday", "cyber monday", "الجمعة السوداء", "الجمعة البيضاء", "بلاك فرايدي", "cyber week"]
    },
    {
        "key": "anniversary",
        "name": "AliExpress Anniversary Sale",
        "name_ar": "تخفيضات ذكرى تأسيس علي إكسبرس 🎂",
        "name_fr": "Anniversaire AliExpress 🎂",
        "banner_tag": "🎂 Anniversary Sale",
        "is_major": True,
        "keywords": ["anniversary", "تأسيس", "ذكرى تأسيس", "anniversaire"]
    },
    {
        "key": "summer_sale",
        "name": "Mega Summer Sale",
        "name_ar": "تخفيضات الصيف الكبرى Summer Sale ☀️",
        "name_fr": "Soldes d'Été AliExpress ☀️",
        "banner_tag": "☀️ Mega Summer Sale",
        "is_major": True,
        "keywords": ["summer sale", "soldes d'été", "تخفيضات الصيف", "summer offers"]
    },
    {
        "key": "winter_offers",
        "name": "Winter Offers Sale",
        "name_ar": "عروض الشتاء Winter Offers ❄️",
        "name_fr": "Offres d'Hiver Winter Offers ❄️",
        "banner_tag": "❄️ Winter Offers",
        "is_major": True,
        "keywords": ["winter offers", "winter sale", "عروض الشتاء", "offres d'hiver"]
    },
    {
        "key": "back_to_school",
        "name": "Back To School / 828 Sale",
        "name_ar": "تخفيضات العودة للمدارس 828 📚",
        "name_fr": "Rentrée Scolaire 828 📚",
        "banner_tag": "📚 828 Mega Sale",
        "is_major": True,
        "keywords": ["back to school", "828 sale", "8.28", "العودة للمدارس", "rentrée"]
    },
]

# Baseline Sales Calendar (Ground Truth)
PROMO_CALENDAR: List[PromoEvent] = [
    PromoEvent(
        name="Party Ready Sale / Choice Day",
        name_ar="تخفيضات Party Ready Sale & Choice Day لشهر أكتوبر 🔥",
        name_fr="Soldes Party Ready Sale & Choice Day Octobre 🇫🇷",
        start_date=datetime(2026, 10, 1, 7, 0, 0, tzinfo=timezone.utc),
        end_date=datetime(2026, 10, 8, 6, 59, 59, tzinfo=timezone.utc),
        banner_tag="🎯 Party Ready Sale (1 - 7 أكتوبر)",
        is_major=True,
        coupon_tiers=[
            {"tier": "2/15$", "code": "OTPRD02"},
            {"tier": "4/30$", "code": "OTPRD04"},
            {"tier": "8/65$", "code": "OTPRD08"},
            {"tier": "15/119$", "code": "OTPRD15"},
            {"tier": "29/229$", "code": "OTPRD28"},
            {"tier": "42/339$", "code": "OTPRD42"},
            {"tier": "55/449$", "code": "OTPRD55"},
        ],
        coupon_tiers_fr=[
            {"tier": "-2€ dès 18€", "code": "FRPRD02"},
            {"tier": "-6€ dès 45€", "code": "FRPRD06"},
            {"tier": "-12€ dès 89€", "code": "FRPRD12"},
            {"tier": "-20€ dès 159€", "code": "FRPRD20"},
            {"tier": "-30€ dès 239€", "code": "FRPRD30"},
            {"tier": "-45€ dès 355€", "code": "FRPRD45"},
            {"tier": "-60€ dès 475€", "code": "FRPRD60"},
        ],
        banner_image_url=None,
        source="baseline"
    ),
    PromoEvent(
        name="Brand Day Sale",
        name_ar="مهرجان Brand Day لشهر أكتوبر 🏷️",
        name_fr="Festival Brand Day Octobre 🏷️",
        start_date=datetime(2026, 10, 9, 7, 0, 0, tzinfo=timezone.utc),
        end_date=datetime(2026, 10, 13, 6, 59, 59, tzinfo=timezone.utc),
        banner_tag="🏷️ Brand Day (9 - 12 أكتوبر)",
        is_major=True,
        coupon_tiers=[],
        source="baseline"
    ),
    PromoEvent(
        name="Winter Offers",
        name_ar="تخفيضات عروض الشتاء Winter Offers ❄️",
        name_fr="Offres d'Hiver Winter Offers ❄️",
        start_date=datetime(2026, 10, 14, 7, 0, 0, tzinfo=timezone.utc),
        end_date=datetime(2026, 10, 18, 6, 59, 59, tzinfo=timezone.utc),
        banner_tag="❄️ Winter Offers (14 - 17 أكتوبر)",
        is_major=True,
        coupon_tiers=[],
        source="baseline"
    ),
    PromoEvent(
        name="11.11 Global Shopping Festival Warm-Up",
        name_ar="التحضير لمهرجان 11.11 العالمي 💥",
        name_fr="Échauffement Festival Mondial 11.11 💥",
        start_date=datetime(2026, 11, 1, 7, 0, 0, tzinfo=timezone.utc),
        end_date=datetime(2026, 11, 11, 6, 59, 59, tzinfo=timezone.utc),
        banner_tag="⏳ تحضيرات مهرجان 11.11",
        is_major=True,
        coupon_tiers=[],
        source="baseline"
    ),
    PromoEvent(
        name="11.11 Global Shopping Festival Main Sale",
        name_ar="مهرجان 11.11 الأكبر عالمياً 🛍️",
        name_fr="Festival Mondial 11.11 AliExpress 🛍️",
        start_date=datetime(2026, 11, 11, 7, 0, 0, tzinfo=timezone.utc),
        end_date=datetime(2026, 11, 19, 6, 59, 59, tzinfo=timezone.utc),
        banner_tag="🔥 أقوى تخفيضات السنة 11.11",
        is_major=True,
        coupon_tiers=[],
        source="baseline"
    ),
    PromoEvent(
        name="Black Friday & Cyber Monday",
        name_ar="تخفيضات الجمعة البيضاء Black Friday 🖤",
        name_fr="Black Friday & Cyber Monday AliExpress 🖤",
        start_date=datetime(2026, 11, 24, 7, 0, 0, tzinfo=timezone.utc),
        end_date=datetime(2026, 12, 1, 6, 59, 59, tzinfo=timezone.utc),
        banner_tag="🖤 Black Friday السنوي",
        is_major=True,
        coupon_tiers=[],
        source="baseline"
    ),
]

EXPIRED_DATE_PATTERNS = [
    re.compile(r'(?:ينتهي|صالح\s+حتى|نهاية\s+العرض|إلى\s+غاية|الى\s+غاية)\s*(?:يوم)?\s*([0-9]{1,2})\s*(?:سبتمبر|sept|september|أوت|اوت|august|جويلية|july)', re.IGNORECASE),
    re.compile(r'(?:20|19|18|17|16|15|14|13|12|11|10)\s*(?:سبتمبر|september|sept)\b', re.IGNORECASE),
    re.compile(r'\b(?:20|19|18|17|16|15|14|13|12|11|10)/09(?:/202[0-6])?\b', re.IGNORECASE),
    re.compile(r'brand\s*day\s*september', re.IGNORECASE),
    re.compile(r'تخفيضات\s*(?:منتصف|شهر)?\s*سبتمبر', re.IGNORECASE),
]


def parse_promo_dates(text: str, default_year: Optional[int] = None) -> Optional[Tuple[datetime, datetime]]:
    """
    Multilingual Date Extractor for Arabic, French, and English announcements.
    Detects ranges like:
    - 'من 1 إلى 7 أكتوبر 2026'
    - 'du 1er au 7 octobre 2026'
    - 'from Oct 1 to Oct 7'
    - '11 - 18 نوفمبر'
    - 'du 24 novembre au 1er décembre'
    - '01/10 au 07/10'
    Returns (start_date, end_date) in UTC or None.
    """
    if not text:
        return None

    clean_text = re.sub(r'[\u0640]', '', text)
    ref_year = default_year or datetime.now(timezone.utc).year

    # Pattern M1: Month Day to Month Day: e.g. 'Oct 1 to Oct 7', 'from Oct 1 to Oct 7 2026', 'Nov 11 - 18'
    p_m1 = re.search(
        r'(?:from\s+)?([^\W0-9_]+)\s+([0-9]{1,2})(?:er|st|nd|rd|th)?\s*(?:to|-|until|au|à)\s*(?:([^\W0-9_]+)\s+)?([0-9]{1,2})(?:er|st|nd|rd|th)?(?:\s*([0-9]{4}))?',
        clean_text,
        re.IGNORECASE
    )
    if p_m1:
        m1_str = p_m1.group(1).lower().strip()
        s_day = int(p_m1.group(2))
        m2_str = p_m1.group(3).lower().strip() if p_m1.group(3) else m1_str
        e_day = int(p_m1.group(4))
        yr = int(p_m1.group(5)) if p_m1.group(5) else ref_year
        if m1_str in MONTH_MAP and m2_str in MONTH_MAP and 1 <= s_day <= 31 and 1 <= e_day <= 31:
            m1_num = MONTH_MAP[m1_str]
            m2_num = MONTH_MAP[m2_str]
            try:
                start_dt = datetime(yr, m1_num, s_day, 7, 0, 0, tzinfo=timezone.utc)
                end_yr = yr if m2_num >= m1_num else yr + 1
                end_dt = datetime(end_yr, m2_num, e_day, 6, 59, 59, tzinfo=timezone.utc) + timedelta(days=1)
                if end_dt > start_dt:
                    return start_dt, end_dt
            except ValueError:
                pass

    # Pattern 1: Same month range: [start_day] to [end_day] [month] [optional year]
    # e.g. 'من 1 إلى 7 أكتوبر', 'du 1er au 7 octobre', 'from 1 to 7 October', '1-7 Nov'
    p1 = re.search(
        r'(?:من|du|from)?\s*([0-9]{1,2})(?:er|st|nd|rd|th)?\s*(?:إلى|الى|حتى|au|à|to|-)\s*([0-9]{1,2})(?:er|st|nd|rd|th)?\s*([^\W0-9_]+)(?:\s*([0-9]{4}))?',
        clean_text,
        re.IGNORECASE
    )
    if p1:
        s_day = int(p1.group(1))
        e_day = int(p1.group(2))
        m_str = p1.group(3).lower().strip()
        yr = int(p1.group(4)) if p1.group(4) else ref_year
        if m_str in MONTH_MAP and 1 <= s_day <= 31 and 1 <= e_day <= 31:
            m_num = MONTH_MAP[m_str]
            try:
                start_dt = datetime(yr, m_num, s_day, 7, 0, 0, tzinfo=timezone.utc)
                # AliExpress campaigns closing on e_day usually run until the morning after
                end_dt = datetime(yr, m_num, e_day, 6, 59, 59, tzinfo=timezone.utc) + timedelta(days=1)
                if end_dt > start_dt:
                    return start_dt, end_dt
            except ValueError:
                pass

    # Pattern 2: Across two different months
    # e.g. 'من 24 نوفمبر إلى 1 ديسمبر 2026', 'du 24 nov au 1er dec', 'Nov 24 to Dec 1'
    p2 = re.search(
        r'(?:من|du|from)?\s*([0-9]{1,2})(?:er|st|nd|rd|th)?\s*([^\W0-9_]+)\s*(?:إلى|الى|حتى|au|à|to|-)\s*([0-9]{1,2})(?:er|st|nd|rd|th)?\s*([^\W0-9_]+)(?:\s*([0-9]{4}))?',
        clean_text,
        re.IGNORECASE
    )
    if p2:
        s_day = int(p2.group(1))
        m1_str = p2.group(2).lower().strip()
        e_day = int(p2.group(3))
        m2_str = p2.group(4).lower().strip()
        yr = int(p2.group(5)) if p2.group(5) else ref_year
        if m1_str in MONTH_MAP and m2_str in MONTH_MAP:
            m1_num = MONTH_MAP[m1_str]
            m2_num = MONTH_MAP[m2_str]
            try:
                start_dt = datetime(yr, m1_num, s_day, 7, 0, 0, tzinfo=timezone.utc)
                end_yr = yr if m2_num >= m1_num else yr + 1
                end_dt = datetime(end_yr, m2_num, e_day, 6, 59, 59, tzinfo=timezone.utc) + timedelta(days=1)
                if end_dt > start_dt:
                    return start_dt, end_dt
            except ValueError:
                pass

    # Pattern 3: Slash / Dot numerical format: '01/10 au 07/10', '01/10 إلى 07/10', '01/10/2026 - 07/10/2026'
    p3 = re.search(
        r'([0-9]{1,2})[/\.]([0-9]{1,2})(?:[/\.]([0-9]{4}))?\s*(?:إلى|الى|حتى|au|à|to|-)\s*([0-9]{1,2})[/\.]([0-9]{1,2})(?:[/\.]([0-9]{4}))?',
        clean_text
    )
    if p3:
        s_day = int(p3.group(1))
        s_m = int(p3.group(2))
        yr = int(p3.group(3)) if p3.group(3) else ref_year
        e_day = int(p3.group(4))
        e_m = int(p3.group(5))
        try:
            start_dt = datetime(yr, s_m, s_day, 7, 0, 0, tzinfo=timezone.utc)
            end_yr = yr if e_m >= s_m else yr + 1
            end_dt = datetime(end_yr, e_m, e_day, 6, 59, 59, tzinfo=timezone.utc) + timedelta(days=1)
            if end_dt > start_dt:
                return start_dt, end_dt
        except ValueError:
            pass

    return None


def extract_coupon_tiers_from_text(text: str) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    """
    Extracts promotional coupon codes and spend thresholds from announcement text.
    Separates into (dz_tiers, fr_tiers).
    Handles:
    - Algeria / Global: 'كوبون 2/15$ : OTPRD02', 'CDDZ03: 3/29$', 'BDQT04 (4/35$)'
    - France: 'Code -2€ dès 18€ : FRPRD02', 'FRPRD06 (-6€ dès 45€)', '2/18€ : CDFR02'
    """
    dz_tiers: List[Dict[str, str]] = []
    fr_tiers: List[Dict[str, str]] = []
    seen_codes = set()

    clean_text = re.sub(r'[\u0640]', '', text)

    # 1. First run the existing Arabic/Global extractor for standard formats
    from app.aliexpress.parser import extract_coupon_list
    std_coupons = extract_coupon_list(clean_text)
    for c in std_coupons:
        code = c.get("code", "").upper().strip()
        tier = c.get("tier", "").strip()
        if code and code not in seen_codes:
            seen_codes.add(code)
            if code.startswith("FR") or "FR" in code[:4]:
                fr_tiers.append({"tier": tier, "code": code})
            else:
                dz_tiers.append({"tier": tier, "code": code})

    # 2. Extract French / Euro formats (-2€ dès 18€, 2/18€)
    fr_patterns = [
        # "-2€ dès 18€ : FRPRD02" or "Code -2€ dès 18€ : FRPRD02"
        re.compile(r'(?:code|coupon)?\s*(-?[0-9]+[€$]?(?:\s*(?:dès|des|off)\s*[0-9]+[€$]?)?)\s*[:=\-]\s*(?:<code>)?([A-Za-z0-9_]{4,15})(?:</code>)?', re.IGNORECASE),
        # "FRPRD02 (-2€ dès 18€)" or "FRPRD02 : -2€ dès 18€"
        re.compile(r'(?:<code>)?([A-Za-z0-9_]{4,15})(?:</code>)?\s*[:=\-\(]\s*(-?[0-9]+[€$]?(?:\s*(?:dès|des|off)\s*[0-9]+[€$]?)?)\)?', re.IGNORECASE),
        # "2/18€ : FRPRD02"
        re.compile(r'([0-9]+/[0-9]+[€$]?)\s*[:=\-]\s*(?:<code>)?([A-Za-z0-9_]{4,15})(?:</code>)?', re.IGNORECASE),
    ]

    for p in fr_patterns:
        for m in p.finditer(clean_text):
            if len(m.groups()) == 2:
                g1, g2 = m.group(1).strip(), m.group(2).strip().upper()
                # Determine which is code and which is tier
                if any(char.isdigit() for char in g1) and ("€" in g1 or "$" in g1 or "dès" in g1.lower() or "/" in g1):
                    tier, code = g1, g2
                else:
                    code, tier = g1, g2

                if code and code not in seen_codes and len(code) >= 4:
                    if code.lower() not in {"http", "https", "aliexpress", "item", "link", "t.me", "code", "promo"}:
                        seen_codes.add(code)
                        is_fr = "€" in tier or "dès" in tier.lower() or code.startswith("FR") or "FR" in code[:4]
                        item = {"tier": tier, "code": code}
                        if is_fr:
                            fr_tiers.append(item)
                        else:
                            dz_tiers.append(item)

    return dz_tiers, fr_tiers


def generate_recurring_promos(ref_date: Optional[datetime] = None, months_ahead: int = 4) -> List[PromoEvent]:
    """
    Perpetual AliExpress Sales Calendar Generator.
    Guarantees the bot autonomously knows all recurring events indefinitely:
    - Choice Day: 1st of every month at 07:00 UTC through 8th at 06:59:59 UTC (7 full days)
    - Brand Day: 9th of every month at 07:00 UTC through 13th at 06:59:59 UTC (4 days)
    - Annual Mega Sales:
      * March (Month 3): Anniversary Sale (17 - 28 March)
      * June (Month 6): Summer Mega Sale (12 - 19 June)
      * August (Month 8): 828 Mega Sale (18 - 28 August)
      * November (Month 11): 11.11 Warm-Up (1 - 11 Nov), 11.11 Main Sale (11 - 19 Nov), Black Friday (20 Nov - 1 Dec)
      * December (Month 12): Year-End Mega Clearance (15 - 23 Dec)
    """
    if ref_date is None:
        ref_date = datetime.now(timezone.utc)

    events: List[PromoEvent] = []

    # Default baseline tier templates
    default_dz_choice = [
        {"tier": "2/15$", "code": "OTPRD02"},
        {"tier": "4/30$", "code": "OTPRD04"},
        {"tier": "8/65$", "code": "OTPRD08"},
        {"tier": "15/119$", "code": "OTPRD15"},
        {"tier": "29/229$", "code": "OTPRD28"},
        {"tier": "42/339$", "code": "OTPRD42"},
        {"tier": "55/449$", "code": "OTPRD55"}
    ]
    default_fr_choice = [
        {"tier": "-2€ dès 18€", "code": "FRPRD02"},
        {"tier": "-6€ dès 45€", "code": "FRPRD06"},
        {"tier": "-12€ dès 89€", "code": "FRPRD12"},
        {"tier": "-20€ dès 159€", "code": "FRPRD20"},
        {"tier": "-30€ dès 239€", "code": "FRPRD30"},
        {"tier": "-45€ dès 355€", "code": "FRPRD45"},
        {"tier": "-60€ dès 475€", "code": "FRPRD60"}
    ]

    for offset in range(months_ahead + 1):
        m_idx = (ref_date.month - 1 + offset)
        yr = ref_date.year + (m_idx // 12)
        m = (m_idx % 12) + 1

        ar_m = ARABIC_MONTH_NAMES.get(m, str(m))
        fr_m = FRENCH_MONTH_NAMES.get(m, str(m))

        # 1. CHOICE DAY (1st to 8th)
        c_start = datetime(yr, m, 1, 7, 0, 0, tzinfo=timezone.utc)
        c_end = datetime(yr, m, 8, 6, 59, 59, tzinfo=timezone.utc)
        events.append(PromoEvent(
            name=f"Choice Day {fr_m} {yr}",
            name_ar=f"تخفيضات Choice Day لشهر {ar_m} 🎯🔥",
            name_fr=f"Codes Promo Choice Day {fr_m} 🇫🇷🎯",
            start_date=c_start,
            end_date=c_end,
            banner_tag=f"🎯 Choice Day (1 - 7 {ar_m})",
            is_major=True,
            coupon_tiers=list(default_dz_choice),
            coupon_tiers_fr=list(default_fr_choice),
            source="recurring"
        ))

        # 2. BRAND DAY (9th to 13th)
        b_start = datetime(yr, m, 9, 7, 0, 0, tzinfo=timezone.utc)
        b_end = datetime(yr, m, 13, 6, 59, 59, tzinfo=timezone.utc)
        events.append(PromoEvent(
            name=f"Brand Day {fr_m} {yr}",
            name_ar=f"مهرجان Brand Day لشهر {ar_m} 🏷️",
            name_fr=f"AliExpress Brand Day {fr_m} 🏷️",
            start_date=b_start,
            end_date=b_end,
            banner_tag=f"🏷️ Brand Day (9 - 12 {ar_m})",
            is_major=True,
            coupon_tiers=[],
            coupon_tiers_fr=[],
            source="recurring"
        ))

        # 3. Annual Mega Events
        if m == 3:  # Anniversary Sale
            events.append(PromoEvent(
                name=f"AliExpress Anniversary Sale {yr}",
                name_ar=f"تخفيضات ذكرى تأسيس علي إكسبرس {yr} 🎂🎉",
                name_fr=f"Anniversaire AliExpress {yr} 🎂🎉",
                start_date=datetime(yr, 3, 17, 7, 0, 0, tzinfo=timezone.utc),
                end_date=datetime(yr, 3, 28, 6, 59, 59, tzinfo=timezone.utc),
                banner_tag=f"🎂 تخفيضات ذكرى التأسيس (17 - 27 مارس)",
                is_major=True,
                coupon_tiers=list(default_dz_choice),
                coupon_tiers_fr=list(default_fr_choice),
                source="recurring"
            ))
        elif m == 6:  # Summer Sale
            events.append(PromoEvent(
                name=f"Mega Summer Sale {yr}",
                name_ar=f"تخفيضات الصيف الكبرى Summer Sale {yr} ☀️",
                name_fr=f"Soldes d'Été AliExpress {yr} ☀️",
                start_date=datetime(yr, 6, 12, 7, 0, 0, tzinfo=timezone.utc),
                end_date=datetime(yr, 6, 19, 6, 59, 59, tzinfo=timezone.utc),
                banner_tag=f"☀️ Mega Summer Sale (12 - 18 جوان)",
                is_major=True,
                coupon_tiers=list(default_dz_choice),
                coupon_tiers_fr=list(default_fr_choice),
                source="recurring"
            ))
        elif m == 8:  # 828 Mega Sale
            events.append(PromoEvent(
                name=f"828 Mega Sale {yr}",
                name_ar=f"تخفيضات 828 الكبرى للعودة للمدارس {yr} 📚",
                name_fr=f"Soldes 828 & Rentrée {yr} 📚",
                start_date=datetime(yr, 8, 18, 7, 0, 0, tzinfo=timezone.utc),
                end_date=datetime(yr, 8, 28, 6, 59, 59, tzinfo=timezone.utc),
                banner_tag=f"📚 828 Mega Sale (18 - 27 أوت)",
                is_major=True,
                coupon_tiers=list(default_dz_choice),
                coupon_tiers_fr=list(default_fr_choice),
                source="recurring"
            ))
        elif m == 11:  # 11.11 & Black Friday
            events.append(PromoEvent(
                name=f"11.11 Global Shopping Festival Warm-Up {yr}",
                name_ar=f"التحضير لمهرجان 11.11 العالمي {yr} 💥",
                name_fr=f"Échauffement 11.11 Mondial {yr} 💥",
                start_date=datetime(yr, 11, 1, 7, 0, 0, tzinfo=timezone.utc),
                end_date=datetime(yr, 11, 11, 6, 59, 59, tzinfo=timezone.utc),
                banner_tag=f"⏳ تحضيرات مهرجان 11.11",
                is_major=True,
                coupon_tiers=list(default_dz_choice),
                coupon_tiers_fr=list(default_fr_choice),
                source="recurring"
            ))
            events.append(PromoEvent(
                name=f"11.11 Global Shopping Festival Main Sale {yr}",
                name_ar=f"مهرجان 11.11 الأكبر عالمياً {yr} 🛍️🔥",
                name_fr=f"Festival Mondial 11.11 AliExpress {yr} 🛍️🔥",
                start_date=datetime(yr, 11, 11, 7, 0, 0, tzinfo=timezone.utc),
                end_date=datetime(yr, 11, 19, 6, 59, 59, tzinfo=timezone.utc),
                banner_tag=f"🔥 أقوى تخفيضات السنة 11.11",
                is_major=True,
                coupon_tiers=list(default_dz_choice),
                coupon_tiers_fr=list(default_fr_choice),
                source="recurring"
            ))
            events.append(PromoEvent(
                name=f"Black Friday & Cyber Monday {yr}",
                name_ar=f"تخفيضات الجمعة السوداء Black Friday {yr} 🖤",
                name_fr=f"Black Friday & Cyber Monday AliExpress {yr} 🖤",
                start_date=datetime(yr, 11, 20, 7, 0, 0, tzinfo=timezone.utc),
                end_date=datetime(yr, 12, 1, 6, 59, 59, tzinfo=timezone.utc),
                banner_tag=f"🖤 Black Friday السنوي",
                is_major=True,
                coupon_tiers=list(default_dz_choice),
                coupon_tiers_fr=list(default_fr_choice),
                source="recurring"
            ))
        elif m == 12:  # Year-End Clearance
            events.append(PromoEvent(
                name=f"Year-End Mega Clearance {yr}",
                name_ar=f"تخفيضات نهاية السنة الكبرى {yr} ❄️🎊",
                name_fr=f"Méga Ventes de Fin d'Année {yr} ❄️🎊",
                start_date=datetime(yr, 12, 15, 7, 0, 0, tzinfo=timezone.utc),
                end_date=datetime(yr, 12, 23, 6, 59, 59, tzinfo=timezone.utc),
                banner_tag=f"❄️ تخفيضات نهاية السنة",
                is_major=True,
                coupon_tiers=list(default_dz_choice),
                coupon_tiers_fr=list(default_fr_choice),
                source="recurring"
            ))

    return events


def sniff_event_from_text(
    text: str,
    media_url: Optional[str] = None,
    campaign_url: Optional[str] = None
) -> Optional[PromoEvent]:
    """
    Autonomous Event Sniffer:
    Inspects incoming message text to discover official promotional festivals,
    sale events, active coupons, and date periods.
    Returns a PromoEvent instance if an authentic event is discovered, or None.
    """
    if not text or len(text.strip()) < 15:
        return None

    clean_text = re.sub(r'[\u0640]', '', text)
    lower_text = clean_text.lower()

    # 1. Check for known event keywords
    matched_pattern = None
    for pat in KNOWN_EVENT_PATTERNS:
        if any(kw in lower_text for kw in pat["keywords"]):
            matched_pattern = pat
            break

    # Extract any coupon tiers
    dz_tiers, fr_tiers = extract_coupon_tiers_from_text(clean_text)
    has_coupons = (len(dz_tiers) + len(fr_tiers)) >= 2

    # Parse date range
    date_range = parse_promo_dates(clean_text)

    # General sale indicator
    has_sale_keywords = any(kw in lower_text for kw in [
        "تخفيضات", "عروض", "كوبونات", "كودات", "حجز الكوبونات",
        "codes promo", "bon plan", "bons plans", "mega sale", "festival"
    ])

    # Qualification criteria:
    # A) Matched a known festival keyword + (dates OR coupons)
    # B) Has explicit date range + sale keywords
    # C) Has 3+ coupon tiers (a full coupon bulletin announcement)
    if not (
        (matched_pattern and (date_range or has_coupons)) or
        (date_range and has_sale_keywords) or
        (len(dz_tiers) + len(fr_tiers) >= 3)
    ):
        return None

    now = datetime.now(timezone.utc)

    # Determine dates
    if date_range:
        start_date, end_date = date_range
    elif matched_pattern and matched_pattern["key"] == "choice_day":
        # If Choice Day is mentioned without explicit dates:
        # If current date is within Choice Day window (1st-8th) or before 8th, use current month
        # Else use 1st-8th of next month
        if now.day <= 8:
            start_date = datetime(now.year, now.month, 1, 7, 0, 0, tzinfo=timezone.utc)
            end_date = datetime(now.year, now.month, 8, 6, 59, 59, tzinfo=timezone.utc)
        else:
            m_next = (now.month % 12) + 1
            yr_next = now.year if m_next > 1 else now.year + 1
            start_date = datetime(yr_next, m_next, 1, 7, 0, 0, tzinfo=timezone.utc)
            end_date = datetime(yr_next, m_next, 8, 6, 59, 59, tzinfo=timezone.utc)
    elif matched_pattern and matched_pattern["key"] == "brand_day":
        start_date = datetime(now.year, now.month, 9, 7, 0, 0, tzinfo=timezone.utc)
        end_date = datetime(now.year, now.month, 13, 6, 59, 59, tzinfo=timezone.utc)
    else:
        # Default 7-day window from today if completely unspecified
        start_date = now.replace(minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=7)

    # Determine event naming
    month_ar = ARABIC_MONTH_NAMES.get(start_date.month, "")
    month_fr = FRENCH_MONTH_NAMES.get(start_date.month, "")

    if matched_pattern:
        name = f"{matched_pattern['name']} {month_fr} {start_date.year}".strip()
        name_ar = f"{matched_pattern['name_ar']} ({month_ar} {start_date.year})".strip()
        name_fr = f"{matched_pattern['name_fr']} {month_fr} {start_date.year}".strip()
        banner_tag = f"{matched_pattern['banner_tag']} ({start_date.day} - {end_date.day - 1} {month_ar})"
        is_major = matched_pattern["is_major"]
    else:
        name = f"AliExpress Special Promo {month_fr} {start_date.year}"
        name_ar = f"تخفيضات علي إكسبرس الاستثنائية ({month_ar} {start_date.year}) 🔥"
        name_fr = f"Promotions Spéciales AliExpress {month_fr} {start_date.year} 🇫🇷"
        banner_tag = f"🎯 تخفيضات علي إكسبرس ({start_date.day} - {end_date.day - 1} {month_ar})"
        is_major = True

    return PromoEvent(
        name=name,
        name_ar=name_ar,
        name_fr=name_fr,
        start_date=start_date,
        end_date=end_date,
        banner_tag=banner_tag,
        is_major=is_major,
        coupon_tiers=dz_tiers,
        coupon_tiers_fr=fr_tiers,
        banner_image_url=media_url,
        source="discovered"
    )


DYNAMIC_EVENTS_FILE = Path(settings.BASE_DIR) / "storage" / "state" / "dynamic_events.json"


def load_dynamic_events() -> List[PromoEvent]:
    """Loads dynamically discovered promotional events from JSON state."""
    if not DYNAMIC_EVENTS_FILE.exists():
        return []
    try:
        with open(DYNAMIC_EVENTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return [PromoEvent.from_dict(d) for d in data if isinstance(d, dict)]
    except Exception as e:
        logger.warning(f"Error loading dynamic events state: {e}")
    return []


def save_dynamic_events(events: List[PromoEvent]):
    """Persists dynamically discovered promotional events to disk atomically."""
    DYNAMIC_EVENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        tmp_file = DYNAMIC_EVENTS_FILE.with_suffix(".tmp")
        data = [ev.to_dict() for ev in events]
        with open(tmp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        if DYNAMIC_EVENTS_FILE.exists():
            os.replace(tmp_file, DYNAMIC_EVENTS_FILE)
        else:
            os.rename(tmp_file, DYNAMIC_EVENTS_FILE)
    except Exception as e:
        logger.error(f"Error saving dynamic events state: {e}")


class PromoTracker:
    def __init__(self):
        self.baseline_calendar: List[PromoEvent] = list(PROMO_CALENDAR)
        self.dynamic_events: List[PromoEvent] = load_dynamic_events()

    @property
    def calendar(self) -> List[PromoEvent]:
        """Provides full backward-compatibility for code iterating over promo_tracker.calendar."""
        return self.get_all_promos()

    def get_all_promos(self, now: Optional[datetime] = None) -> List[PromoEvent]:
        """
        Returns the unified, deduplicated list of all promo events:
        Discovered > Baseline > Recurring.
        """
        if now is None:
            now = datetime.now(timezone.utc)

        # 1. Recurring base
        recurring = generate_recurring_promos(ref_date=now, months_ahead=4)

        # 2. Baseline entries
        baseline = list(self.baseline_calendar)

        # 3. Dynamic discovered entries (re-load from disk to stay up to date)
        self.dynamic_events = load_dynamic_events()
        dynamic = list(self.dynamic_events)

        merged: Dict[str, PromoEvent] = {}

        # Add recurring base first
        for ev in recurring:
            merged[ev.get_event_key()] = ev

        # Add / override with baseline
        for ev in baseline:
            matching_key = None
            for k, existing in merged.items():
                if abs((ev.start_date - existing.start_date).total_seconds()) < 48 * 3600:
                    matching_key = k
                    break
            if matching_key:
                # Merge: enrich with any existing recurring tiers if baseline has none
                if not ev.coupon_tiers and merged[matching_key].coupon_tiers:
                    ev.coupon_tiers = merged[matching_key].coupon_tiers
                if not ev.coupon_tiers_fr and merged[matching_key].coupon_tiers_fr:
                    ev.coupon_tiers_fr = merged[matching_key].coupon_tiers_fr
                merged[matching_key] = ev
            else:
                merged[ev.get_event_key()] = ev

        # Add / enrich with dynamic discovered events (highest precedence)
        for ev in dynamic:
            matching_key = None
            for k, existing in merged.items():
                if abs((ev.start_date - existing.start_date).total_seconds()) < 48 * 3600:
                    matching_key = k
                    break
            if matching_key:
                existing = merged[matching_key]
                # Merge coupons: dynamic takes priority, keeping existing unique codes
                combined_dz = {c["code"]: c for c in (existing.coupon_tiers or []) + (ev.coupon_tiers or [])}
                combined_fr = {c["code"]: c for c in (existing.coupon_tiers_fr or []) + (ev.coupon_tiers_fr or [])}
                existing.coupon_tiers = list(combined_dz.values())
                existing.coupon_tiers_fr = list(combined_fr.values())
                if ev.banner_image_url:
                    existing.banner_image_url = ev.banner_image_url
                if ev.source == "discovered":
                    existing.source = "discovered"
            else:
                merged[ev.get_event_key()] = ev

        return sorted(merged.values(), key=lambda x: x.start_date)

    def get_active_promo(self, now: Optional[datetime] = None) -> Optional[PromoEvent]:
        """Returns the currently active official AliExpress promo event, if any."""
        if now is None:
            now = datetime.now(timezone.utc)
        promos = self.get_all_promos(now)
        active = [ev for ev in promos if ev.start_date <= now <= ev.end_date]
        if not active:
            return None
        # Prioritize major events and events with coupon tiers
        active.sort(key=lambda x: (x.is_major, len(x.coupon_tiers) + len(x.coupon_tiers_fr or [])), reverse=True)
        return active[0]

    def get_next_promo(self, now: Optional[datetime] = None) -> Optional[Tuple[PromoEvent, int]]:
        """Returns the upcoming promo event and days remaining until it starts."""
        if now is None:
            now = datetime.now(timezone.utc)
        promos = self.get_all_promos(now)
        for ev in promos:
            if ev.start_date > now:
                days_left = (ev.start_date - now).days
                return ev, days_left
        return None

    def validate_deal_freshness(self, text: str, msg_datetime: Optional[datetime] = None, max_hours: Optional[int] = None) -> Tuple[bool, Optional[str]]:
        """
        Validates that a deal is fresh and not an expired promo from past campaigns:
        1. Checks message age (within last 24 hours normally, or 72 hours during active promos).
        2. Detects expired date mentions (e.g. Sept 20 coupons or past dates).
        3. Detects expired campaign names.
        """
        now = datetime.now(timezone.utc)

        # 1. Message age check (within 24 hours normally, up to 72 hours during active promos)
        if max_hours is None:
            active_promo = self.get_active_promo(now)
            max_hours = 72 if active_promo else 24

        if msg_datetime is not None:
            age = now - msg_datetime
            if age > timedelta(hours=max_hours):
                return False, f"Message is too old ({age.total_seconds() / 3600:.1f} hours ago, max {max_hours}h)"

        # 2. Expired date mentions in text
        for pat in EXPIRED_DATE_PATTERNS:
            m = pat.search(text)
            if m:
                return False, f"Mention of expired campaign/date detected: '{m.group(0)}'"

        # 3. If coupons are mentioned, ensure we are not in an empty period passing off old codes
        active_promo = self.get_active_promo(now)
        if not active_promo:
            if "brand day" in text.lower() and "sept" in text.lower():
                return False, "Expired September Brand Day promo"

        return True, None

    def get_promo_header(self, now: Optional[datetime] = None) -> Optional[str]:
        """Returns promo banner to include in telegram posts if a major event is active or imminent."""
        if now is None:
            now = datetime.now(timezone.utc)

        active = self.get_active_promo(now)
        if active:
            return active.banner_tag

        next_event = self.get_next_promo(now)
        if next_event:
            event, days_left = next_event
            if days_left <= 3 and event.is_major:
                return f"⏳ استعدوا: {event.banner_tag} ينطلق بعد {days_left} أيام!"

        return None

    def sniff_and_register_event(
        self,
        text: str,
        media_url: Optional[str] = None,
        campaign_url: Optional[str] = None
    ) -> Optional[PromoEvent]:
        """
        Sniffs message text for promo event announcements and registers discovered
        events into the persistent dynamic events database.
        """
        discovered = sniff_event_from_text(text, media_url=media_url, campaign_url=campaign_url)
        if not discovered:
            return None

        # Check if already present in dynamic_events
        matched_existing = None
        for ev in self.dynamic_events:
            if abs((ev.start_date - discovered.start_date).total_seconds()) < 48 * 3600:
                matched_existing = ev
                break

        if matched_existing:
            # Enrich existing dynamic event with new coupons if any
            new_dz = {c["code"]: c for c in (matched_existing.coupon_tiers or []) + (discovered.coupon_tiers or [])}
            new_fr = {c["code"]: c for c in (matched_existing.coupon_tiers_fr or []) + (discovered.coupon_tiers_fr or [])}
            matched_existing.coupon_tiers = list(new_dz.values())
            matched_existing.coupon_tiers_fr = list(new_fr.values())
            if discovered.banner_image_url and not matched_existing.banner_image_url:
                matched_existing.banner_image_url = discovered.banner_image_url
            logger.info(f"[EVENT KNOWER] Enriched discovered event: {matched_existing.name} (Coupons DZ: {len(matched_existing.coupon_tiers)}, FR: {len(matched_existing.coupon_tiers_fr or [])})")
            save_dynamic_events(self.dynamic_events)
            return matched_existing
        else:
            self.dynamic_events.append(discovered)
            save_dynamic_events(self.dynamic_events)
            logger.info(f"[EVENT KNOWER] Discovered and registered new event: {discovered.name} from {discovered.start_date} to {discovered.end_date} (DZ: {len(discovered.coupon_tiers)}, FR: {len(discovered.coupon_tiers_fr or [])})")
            return discovered

    async def scrape_aliexpress_promo_banner(self, campaign_url: Optional[str] = None) -> Optional[str]:
        """
        Scrapes or retrieves the official AliExpress promo banner image:
        1. Resolves shortlink / campaign URL and fetches page metadata (og:image, twitter:image).
        2. Filters strictly for AliExpress CDN domains (alicdn.com, aliexpress-media.com).
        3. Falls back to official AliExpress CDN calendar banners (e.g. Choice Day).
        """
        if campaign_url:
            try:
                import httpx
                from bs4 import BeautifulSoup
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
                    "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
                }
                async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
                    resp = await client.get(campaign_url, headers=headers)
                    if resp.status_code == 200:
                        soup = BeautifulSoup(resp.text, "html.parser")
                        og = soup.find("meta", property="og:image") or soup.find("meta", attrs={"name": "og:image"})
                        if og and og.get("content"):
                            cand = og["content"].strip()
                            if any(d in cand for d in ["alicdn.com", "aliexpress-media.com"]):
                                return cand

                        tw = soup.find("meta", attrs={"name": "twitter:image"})
                        if tw and tw.get("content"):
                            cand = tw["content"].strip()
                            if any(d in cand for d in ["alicdn.com", "aliexpress-media.com"]):
                                return cand

                        for img in soup.find_all("img"):
                            src = img.get("src") or img.get("data-src") or ""
                            if any(d in src for d in ["alicdn.com", "aliexpress-media.com"]) and ("kf/" in src or "banner" in src.lower()):
                                if not src.startswith("http"):
                                    src = f"https:{src}"
                                return src
            except Exception:
                pass

        active = self.get_active_promo()
        if active and active.banner_image_url:
            return active.banner_image_url

        next_event = self.get_next_promo()
        if next_event and next_event[0].banner_image_url:
            return next_event[0].banner_image_url

        return None


promo_tracker = PromoTracker()
