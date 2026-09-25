import re
from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict
from app.config.settings import settings

PRICE_PATTERNS = [
    re.compile(r'\$\s*([0-9]+(?:[\.,][0-9]{1,2})?)', re.IGNORECASE),
    re.compile(r'([0-9]+(?:[\.,][0-9]{1,2})?)\s*\$', re.IGNORECASE),
    re.compile(r'([0-9]+(?:[\.,][0-9]{1,2})?)\s*USD', re.IGNORECASE),
    re.compile(r'USD\s*([0-9]+(?:[\.,][0-9]{1,2})?)', re.IGNORECASE),
    re.compile(r'السعر\s*[:：]\s*([0-9]+(?:[\.,][0-9]{1,2})?)', re.IGNORECASE),
    re.compile(r'السعــــر\s*[:：]\s*([0-9]+(?:[\.,][0-9]{1,2})?)', re.IGNORECASE),
]

EUR_PRICE_PATTERNS = [
    re.compile(r'([0-9]+(?:[\.,][0-9]{1,2})?)\s*€', re.IGNORECASE),
    re.compile(r'€\s*([0-9]+(?:[\.,][0-9]{1,2})?)', re.IGNORECASE),
    re.compile(r'([0-9]+(?:[\.,][0-9]{1,2})?)\s*EUR', re.IGNORECASE),
]

COUPON_PATTERNS = [
    re.compile(r'(?:كوبـــ?ون|كود|code|coupon)\s*(?:[0-9]+(?:\.[0-9]+)?/[0-9]+(?:\.[0-9]+)?\$?)?\s*[:：\-]\s*([A-Za-z0-9_-]{3,25})', re.IGNORECASE),
    re.compile(r'🎟️?\s*(?:كوبـــ?ون|كود|code|coupon)\s*[:：\-]?\s*([A-Za-z0-9_-]{3,25})', re.IGNORECASE),
    re.compile(r'(?:استخدم كود|استعمل كود|قسيمة)\s*[:：\-]?\s*([A-Za-z0-9_-]{3,25})', re.IGNORECASE),
]

POINTS_PATTERNS = [
    re.compile(r'خصم\s*(?:النقاط|نقاط|العملات)', re.IGNORECASE),
    re.compile(r'نقاط\s*علي\s*إكسبريس', re.IGNORECASE),
    re.compile(r'coins\s*discount', re.IGNORECASE),
    re.compile(r'تخفيض\s*العملات', re.IGNORECASE),
    re.compile(r'تحتاج\s*الى\s*العملات', re.IGNORECASE),
    re.compile(r'سعر\s*تخفيض\s*العملات', re.IGNORECASE),
    re.compile(r'رابط\s*العملات', re.IGNORECASE),
]

COUNTRY_PATTERNS = [
    (re.compile(r'(?:دولة|البلد|بلد الحساب|تحويل الحساب الى)\s*(?:التطبيق\s*الى)?\s*كندا|🇨🇦', re.IGNORECASE), "كندا 🇨🇦"),
    (re.compile(r'(?:دولة|البلد|بلد الحساب|تحويل الحساب الى)\s*(?:التطبيق\s*الى)?\s*كوريا|🇰🇷', re.IGNORECASE), "كوريا 🇰🇷"),
    (re.compile(r'(?:دولة|البلد|بلد الحساب|تحويل الحساب الى)\s*(?:التطبيق\s*الى)?\s*فرنسا|🇫🇷', re.IGNORECASE), "فرنسا 🇫🇷"),
    (re.compile(r'(?:ديرو|دير|بلاد|دولة|البلد|بلد الحساب)\s*(?:بلاد\s*|دولة\s*)?الجزائر|🇩🇿', re.IGNORECASE), "الجزائر 🇩🇿"),
]

BLOCKED_STORE_KEYWORDS = [
    "temu", "تيمو", "amazon", "امازون", "أمازون", "shein", "شي ان", "noon", "نون"
]

NON_DEAL_INDICATORS = [
    "pinned a photo", "pinned a message", "تبادل إعلاني", "تبادل اعلاني",
    "اشترك في قناتنا", "قناتنا الاحتياطية", "مسابقة ربح", "قنواتنا", "تطبيق أفلام", "apk"
]

# ── Category Whitelist: ONLY gaming, watches, phones, tablets, tech accessories ──
ALLOWED_CATEGORY_KEYWORDS_EN = [
    # Gaming peripherals
    "mouse", "mice", "keyboard", "headset", "headphone", "earphone", "earbuds",
    "tws", "controller", "gamepad", "joystick", "gaming", "gamer", "game",
    "monitor", "mechanical", "rgb", "dpi", "mouse pad", "mousepad",
    # Gaming & PC Brands
    "attack shark", "ajazz", "machenike", "aula", "darmoshark", "vgn", "zaopin",
    "kysona", "fantech", "keychron", "royal kludge", "rk61", "epomaker", "akko",
    "redragon", "razer", "logitech", "steelseries", "corsair", "hyperx", "dareu",
    "thunderobot", "flydigi", "gamesir", "8bitdo", "gulikit", "easysmx", "mobapad",
    # GPU / PC parts & Specs
    "gpu", "graphics card", "rtx", "gtx", "radeon", "ram", "ssd", "nvme", "ddr4", "ddr5",
    "gaming chair", "cooling", "cooler", "fan", "motherboard", "processor", "ryzen", "intel core",
    "120hz", "144hz", "165hz", "240hz", "ips", "oled", "amoled",
    # Phones & Brands
    "phone", "smartphone", "mobile", "iphone", "samsung", "xiaomi", "redmi",
    "poco", "oneplus", "realme", "oppo", "vivo", "nothing phone", "pixel",
    "honor", "huawei", "infinix", "tecno", "zte", "nubia", "redmagic", "iqoo",
    "motorola", "moto", "black shark",
    # Tablets
    "tablet", "ipad", "tab", "pad", "xiaomi pad", "lenovo tab", "redmi pad",
    # Watches
    "watch", "smartwatch", "smart watch", "smart band", "band", "mi band",
    "amazfit", "garmin", "huawei watch", "apple watch", "fitness tracker", "colmi", "zeblaze",
    # Consoles & VR
    "console", "playstation", "ps5", "ps4", "xbox", "nintendo", "switch",
    "vr", "oculus", "meta quest", "steam deck", "rog ally", "legion go", "anbernic", "miyoo",
    # Audio
    "speaker", "soundbar", "microphone", "mic", "bluetooth", "anc", "hifi",
    # Accessories (phone/tablet/pc)
    "charger", "charging", "power bank", "case", "cover", "screen protector",
    "tempered glass", "stylus", "pen", "cable", "usb", "type-c", "hdmi",
    "adapter", "hub", "dock", "gan charger", "baseus", "ugreen", "anker",
    # Camera & media
    "webcam", "camera", "drone", "action cam", "gopro", "tripod",
    "ring light", "led strip", "projector",
    # Computers
    "mini pc", "laptop", "notebook", "chromebook", "macbook",
    # Generic tech
    "wireless", "bluetooth", "rechargeable",
]

ALLOWED_CATEGORY_KEYWORDS_AR = [
    "ماوس", "كيبورد", "لوحة مفاتيح", "سماعة", "سماعات", "يد تحكم", "يدة تحكم",
    "جيمنج", "قيمنق", "جيمينق", "جايمنج", "العاب", "ألعاب", "شاشة", "كرسي",
    "هاتف", "جوال", "موبايل", "تابلت", "لوحي", "ايباد", "آيباد",
    "ساعة", "ساعه", "ذكية", "سوار ذكي",
    "بلوتوث", "شاحن", "باور بانك", "كابل", "كفر", "جراب", "حامل",
    "سبيكر", "مايك", "كاميرا", "درون", "بروجكتر", "لابتوب",
    "لاسلكي", "وايرلس", "بي سي", "كارت شاشة", "كرت شاشة", "معالج", "رام",
    "هونر", "هواوي", "شاومي", "ريدمي", "بوكو", "سامسونج", "ايفون", "آيفون",
    "ريلمي", "انفينكس", "تكنو", "نوبيا", "لينوفو", "اسوس",
]


def is_allowed_category(title: str, text: str) -> Tuple[bool, Optional[str]]:
    """Check if the deal belongs to an allowed category (gaming, watches, phones, tablets, tech)."""
    combined = f"{title} {text}".lower()

    # Check English keywords
    for kw in ALLOWED_CATEGORY_KEYWORDS_EN:
        if kw in combined:
            return True, None

    # Check Arabic keywords
    for kw in ALLOWED_CATEGORY_KEYWORDS_AR:
        if kw in combined:
            return True, None

    # If coupon list (multiple coupons), allow it through — these are general discount codes
    if combined.count("كوبون") >= 2 or combined.count("code") >= 2 or combined.count("coupon") >= 2:
        return True, None

    return False, f"Category not allowed (not gaming/watch/phone/tablet): {title[:60]}"

def is_spam_or_non_deal(text: str) -> Tuple[bool, Optional[str]]:
    if not text or len(text.strip()) < 10:
        return True, "Message is too short or empty"

    lower_text = text.lower()

    for store in BLOCKED_STORE_KEYWORDS:
        if store in lower_text:
            return True, f"Blocked store or platform detected: {store}"

    for spam_kw in NON_DEAL_INDICATORS:
        if spam_kw in lower_text and not any(k in lower_text for k in ["s.click.aliexpress.com", "aliexpress.com/item"]):
            return True, f"Non-deal announcement: {spam_kw}"

    return False, None

def extract_coupon_list(text: str) -> List[Dict[str, str]]:
    """
    Extracts coupons ONLY from explicit coupon bulletin lists.
    Must contain explicit words like 'كوبون' or 'كود' on the line.
    """
    if not text:
        return []
    coupons = []
    lines = text.splitlines()
    for line in lines:
        line_clean = line.strip()
        if not line_clean or "http://" in line_clean or "https://" in line_clean:
            continue

        # Reject phone/hardware specs lines (camera, battery, display, cpu, ram)
        lower = line_clean.lower()
        if any(w in lower for w in ["camera", "battery", "amoled", "mah", "nits", "pdaf", "ois", "gen", "snapdragon", "adreno"]):
            continue

        # Must explicitly contain coupon / code / قسيمة
        if not any(k in line_clean for k in ["كوبون", "كوبـــون", "كود", "قسيمة", "code", "coupon"]):
            continue

        m = re.search(
            r'(?:🎟️?|🎫)?\s*(?:كوبـــ?ون|كود|code|قسيمة)?\s*([0-9]+(?:\.[0-9]+)?/[0-9]+(?:\.[0-9]+)?\$?|[0-9]+\$?(?:\s*/\s*[0-9]+\$?)?)\s*[:：\-]?\s*([A-Za-z0-9_-]{4,20})',
            line_clean,
            re.IGNORECASE
        )
        if m:
            tier = m.group(1).strip()
            code = m.group(2).strip()
            if not tier.endswith("$"):
                tier += "$"
            if code.lower() not in {"http", "https", "aliexpress", "item", "link", "t.me"}:
                coupons.append({"tier": tier, "code": code.upper()})
    return coupons

def extract_prices(text: str) -> Tuple[Optional[float], Optional[float]]:
    usd_val: Optional[float] = None
    eur_val: Optional[float] = None

    if not text:
        return None, None

    # Filter out lines that are coupon codes or discount tiers (e.g. 4/35$, 10/99$, قسيمة 20$)
    filtered_lines = []
    for line in text.splitlines():
        lc = line.strip().lower()
        if any(w in lc for w in ["كوبون", "كوبـــون", "كود", "قسيمة", "code", "coupon"]):
            continue
        if re.search(r'\d+\s*/\s*\d+', lc):
            continue
        filtered_lines.append(line)

    clean_text = "\n".join(filtered_lines)

    for pattern in EUR_PRICE_PATTERNS:
        m = pattern.search(clean_text)
        if m:
            try:
                eur_val = float(m.group(1).replace(",", "."))
                break
            except ValueError:
                pass

    for pattern in PRICE_PATTERNS:
        m = pattern.search(clean_text)
        if m:
            try:
                candidate = float(m.group(1).replace(",", "."))
                if 0.1 <= candidate <= 10000:
                    usd_val = candidate
                    break
            except ValueError:
                pass

    rate = settings.EUR_USD_RATE or 0.92
    if usd_val is not None and eur_val is None:
        eur_val = round(usd_val * rate, 2)
    elif eur_val is not None and usd_val is None:
        usd_val = round(eur_val / rate, 2)

    return usd_val, eur_val

def extract_coupon(text: str) -> Optional[str]:
    if not text:
        return None
    for pattern in COUPON_PATTERNS:
        m = pattern.search(text)
        if m:
            code = m.group(1).strip()
            if code.lower() not in {"http", "https", "aliexpress", "item", "link", "url", "temu"}:
                return code.upper()
    return None

def detect_points_discount(text: str) -> bool:
    if not text:
        return False
    for pattern in POINTS_PATTERNS:
        if pattern.search(text):
            return True
    return False

def extract_country_instruction(text: str) -> Optional[str]:
    if not text:
        return None
    for pattern, name in COUNTRY_PATTERNS:
        if pattern.search(text):
            return name
    return None

def extract_clean_title(text: str) -> Optional[str]:
    if not text:
        return None

    noise = [
        "عروض", "brand day", "choice day", "winter offers", "party ready",
        "لافار", "لافاار", "الحق", "الححق", "سعر ممتاز", "سعر خيالي",
        "جدول تخفيضات", "باطل", "اقل سعر", "أقل سعر", "ممتاز",
        "متوفرة للجمع", "طريقة حجز", "حجز الكوبونات", "تفعيل الاشعارات",
        "هاتف جديد", "أحدث", "جميع الألوان", "عاود رجع", "تخفيض الآن",
        "مواصفات", "قسيمة البائع", "كوبون", "قسيمة", "قناة", "اشترك",
        "بكمية قليلة", "ألحق", "الحق", "تاع بريكولاج", "بريكولاج", "افار", "آفار",
        "ديرو بلاد", "بلاد الجزائر", "ديرو بلاد الجزائر", "اختر بلد", "أختر بلد",
        "يلحقك", "معاها", "يأتي مع", "معها", "ملحقات", "الهدايا", "محتويات", "العلبة",
        "بوشات", "كيتمان", "قلم كتابة", "انكسابل", "هدية", "شاحن مع كابل",
        "طريقة الشراء", "طريقة الطلب", "رابط الشراء", "للشراء", "للطلب",
        "جدول", "اكواد", "أكواد", "تخفيضات", "عروض الخريف", "تفعيل"
    ]

    # Normalize tatweel and remove multiple exclamation/fire emojis
    cleaned_text = re.sub(r'[\u0640]', '', text)
    lines = [l.strip() for l in cleaned_text.splitlines() if l.strip()]
    if not lines:
        return None

    def is_noisy(cand_str: str) -> bool:
        if not cand_str or len(cand_str) < 4:
            return True
        norm = cand_str.lower()
        norm_collapsed = re.sub(r'(.)\1{2,}', r'\1', norm)
        for n in noise:
            if n in norm or n in norm_collapsed:
                return True
        # Reject bundle listings with multiple slashes (e.g. بوشات / كابل / شاحن / ماوس)
        if cand_str.count('/') >= 2 or cand_str.count('+') >= 3:
            return True
        # Reject candidate titles starting with description verbs
        if any(norm.startswith(v) for v in ["يلحقك", "تأتي", "تحتوي", "يأتي", "معاها", "طريقة", "كيفية", "شرح"]):
            return True
        return False

    # 1. Look for explicit title prefix line
    for i, line in enumerate(lines):
        m = re.search(r'(?:تخفيض\s+لـ?|تخفيض\s+الآن\s+لـ?|عرض\s+خاص\s+لـ?|تخفيض\s+على)\s*[:：\-]?\s*(.*)', line)
        if m:
            cand = m.group(1).strip()
            # If empty or colon or very short, check the next line
            if (not cand or len(cand) < 3) and i + 1 < len(lines):
                cand = lines[i + 1].strip()
            cand = re.sub(r'[\$€].*$', '', cand).strip()
            cand = re.sub(r'https?://\S+', '', cand).strip()
            cand = re.sub(r'^[❗️🔖📌🔥🚨⚡💥✨📦🛒🎁📢✅💎💰🔻ـ\s\-:]+', '', cand).strip()
            if not is_noisy(cand) and len(cand) >= 4:
                return cand[:100]

    # 2. Look for lines with English/Arabic product name
    for line in lines:
        c = re.sub(r'^[❗️🔖📌🔥🚨⚡💥✨📦🛒🎁📢✅💎💰🔻ـ\s\-:⭐️🌷⏺📎]+', '', line).strip()
        c = re.sub(r'[\$€].*$', '', c).strip()
        c = re.sub(r'https?://\S+', '', c).strip()
        norm = c.lower()
        # Reject standalone coupon code lines (e.g. FSQT02, BDQT30)
        if re.match(r'^[A-Z0-9_-]{4,20}$', c):
            continue
        # Ignore noisy lines
        if (
            len(c) >= 5
            and not is_noisy(c)
            and not any(k in norm for k in ["السعر", "رابط", "كوبون", "قناتنا", "البوت", "t.me", "youtu", "https", "http", "شحن", "تخفيض", "سعر", "البلد", "بلاد", "ديرو", "الجزائر"])
        ):
            return c[:100]

    return None


def detect_deal_type(raw_text: str, url: str = "") -> str:
    """
    Intelligently determines whether a deal is a 'bundle' deal or a 'coin' deal.
    90%+ of channel offers are coin deals.
    Bundle deals are identified by keywords like 'bundle', 'حزمة', 'حزم', '3 بـ',
    '3 منتجات', 'choice bundle', or bundle URL patterns.
    """
    text_lower = (raw_text or "").lower()
    url_lower = (url or "").lower()

    bundle_keywords = [
        "bundle", "bundledraw", "bundledeals", "bundle deals",
        "حزم", "حزمة", "3 بـ", "3 منتجات", "3 items", "3 حبات",
        "sourcetype=562"
    ]
    if any(k in text_lower for k in bundle_keywords) or any(k in url_lower for k in bundle_keywords):
        return "bundle"

    return "coin"
