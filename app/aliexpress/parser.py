import re
from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict
from app.config.settings import settings

PRICE_PATTERNS = [
    re.compile(r'[\$💲]\s*([0-9]+(?:[\.,][0-9]{1,2})?)', re.IGNORECASE),
    re.compile(r'([0-9]+(?:[\.,][0-9]{1,2})?)\s*[\$💲]', re.IGNORECASE),
    re.compile(r'([0-9]+(?:[\.,][0-9]{1,2})?)\s*USD', re.IGNORECASE),
    re.compile(r'USD\s*([0-9]+(?:[\.,][0-9]{1,2})?)', re.IGNORECASE),
    re.compile(r'(?:ا+لسعر|ا+لسعــــر|سعر\s*القطعة|سعر\s*قطعة|سعر)\s*[:：\-\s]*[\$💲]?\s*([0-9]+(?:[\.,][0-9]{1,2})?)', re.IGNORECASE),
]

EUR_PRICE_PATTERNS = [
    re.compile(r'([0-9]+(?:[\.,][0-9]{1,2})?)\s*€', re.IGNORECASE),
    re.compile(r'€\s*([0-9]+(?:[\.,][0-9]{1,2})?)', re.IGNORECASE),
    re.compile(r'([0-9]+(?:[\.,][0-9]{1,2})?)\s*EUR', re.IGNORECASE),
]

COUPON_PATTERNS = [
    re.compile(r'(?:كوبون|كود|code|coupon|قسيمة)\s*(?:[-–]?\s*[$€]?[0-9]+(?:[\.,][0-9]+)?[^\S\r\n]*(?:/[^\S\r\n]*[$€]?[0-9]+(?:[\.,][0-9]+)?)?[^\S\r\n]*(?:€|eur|euro|euros|دولار|dollar|\$)?)?\s*[:：\-\s✅🔥👉✔️⏺🙏🎟️]*(?:استخدمه|استخدم|بكود|code)?\s*[:：\-\s✅🔥👉✔️⏺🙏🎟️]*([A-Za-z][A-Za-z0-9_-]{3,24})', re.IGNORECASE),
    re.compile(r'(?:كوبون|كود|code|coupon)\s*(?:[-–]?\s*[$€]?[0-9]+(?:\.[0-9]+)?(?:\s*(?:€|eur|euro|euros|دولار|dollar|\$))?)?[^\nA-Za-z0-9]*(?:استخدمه|استخدم|استعمله|استعمل)?[^\nA-Za-z0-9]*([A-Za-z][A-Za-z0-9_-]{3,24})', re.IGNORECASE),
    re.compile(r'(?:استخدم كود|استعمل كود|كود الخصم|كود التخفيض|كوبون خاص|code promo|code de reduction)\s*[^A-Za-z0-9]*([A-Za-z][A-Za-z0-9_-]{3,24})', re.IGNORECASE),
    re.compile(r'(?:code|كود)\s*[-–]?\s*[0-9]+[€$]?\s*[:：\-\s✅🔥👉✔️⏺🤐]+\s*([A-Za-z][A-Za-z0-9_-]{3,24})', re.IGNORECASE),
    re.compile(r'👊\s*(?:كوبون|كود|code)\s*[:：\-\s\d\$/€]*([A-Za-z][A-Za-z0-9_-]{3,24})', re.IGNORECASE),
]

SELLER_COUPON_PATTERNS = [
    re.compile(r'(?:حصل\s*|احجز\s*)?قسيمة\s*(?:البائع|المتجر|خاصة\s*بالمتجر|store\s*coupon|seller\s*coupon)\s*[:：\-\s✅🔥👉✔️🌷🙏\+]*[$]?\s*([0-9]+(?:[\.,][0-9]+)?(?:\s*(?:دولار|dollar|\$))?|[A-Za-z0-9_\-]{3,25})', re.IGNORECASE),
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
    "scyrox", "mad r", "vxe", "fantech", "keychron", "nuphy", "akko", "monsgeek",
    "wobkey", "rainy75", "crush80", "bridge75", "hi75", "hi8", "leobog", "epomaker",
    "royal kludge", "rk61", "redragon", "razer", "logitech", "steelseries", "corsair",
    "hyperx", "dareu", "thunderobot", "flydigi", "gamesir", "8bitdo", "gulikit",
    "easysmx", "mobapad", "iine", "dobe", "skull & co", "yunzii",
    # Sensor & Switch Tech
    "paw3395", "paw3950", "paw3311", "paw3370", "rapid trigger", "magnetic switch",
    "hall effect", "8k", "4k", "polling rate", "glass pad", "cordura",
    # Enthusiast brands
    "pulsar", "lamzu", "ninjutso", "sora", "maya", "thorn", "atlantis",
    "superlight", "g pro", "viper", "deathadder", "basilisk", "blackshark", "kraken",
    # GPU / PC parts & Specs
    "gpu", "graphics card", "video card", "vga", "apu", "amd", "bc 250", "bc-250", "bc250", "gddr6", "gddr5", "gddr",
    "256-bit", "256bit", "192bit", "128bit", "rtx", "gtx", "radeon", "rx", "ram", "ssd", "hdd", "nvme", "ddr4", "ddr5",
    "gaming chair", "cooling", "cooler", "fan", "fans", "motherboard", "processor", "ryzen", "intel core",
    "120hz", "144hz", "165hz", "240hz", "ips", "oled", "amoled",
    "thermalright", "deepcool", "id-cooling", "arctic", "noctua", "nzxt", "lian li",
    # Thermal & Cooling supplies
    "thermal paste", "thermal putty", "putty", "thermal pad", "thermalpad", "ptm7950", "heatsink", "aio",
    # Storage & Drives
    "hard drive", "hard disk", "m.2", "m2", "sata", "sata3", "flash drive", "pendrive", "pen drive",
    "thumb drive", "micro sd", "microsd", "sd card", "tf card", "memory card", "storage", "enclosure",
    # Cables, Power & Charging
    "cable", "cables", "cord", "wire", "usb", "usb-c", "usbc", "usb c", "type-c", "typec", "type c",
    "c to c", "hdmi", "displayport", "dp cable", "otg", "aux", "ethernet", "lan", "rj45", "lightning",
    "charger", "chargers", "charging", "gan charger", "gan", "fast charger", "fast charge", "fast charging",
    "power bank", "powerbank", "adapter", "adapters", "hub", "hubs", "dock", "docks", "docking station",
    "baseus", "ugreen", "anker", "pd 100w", "pd 65w", "100w", "65w",
    # Tools, Drivers & DIY
    "driver", "drivers", "screwdriver", "screwdrivers", "drill", "electric screwdriver", "rotary tool",
    "pen set", "grinder pen", "tool", "tools", "diy", "soldering", "soldering iron", "multimeter", "wrench",
    "plier", "pliers", "tungfull",
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
    # Accessories & Projectors
    "case", "cover", "screen protector", "tempered glass", "stylus", "pen",
    "webcam", "camera", "drone", "action cam", "action camera", "gopro", "tripod",
    "dji", "osmo", "gimbal", "stabilizer",
    "ring light", "led strip", "projector", "magcubic", "hy300",
    # Computers
    "mini pc", "laptop", "notebook", "chromebook", "macbook", "pc", "computer", "desktop",
    # Generic tech
    "wireless", "bluetooth", "rechargeable",
]

ALLOWED_CATEGORY_KEYWORDS_AR = [
    "ماوس", "كيبورد", "لوحة مفاتيح", "سماعة", "سماعات", "يد تحكم", "يدة تحكم", "يدة",
    "جيمنج", "قيمنق", "جيمينق", "جايمنج", "العاب", "ألعاب", "شاشة", "كرسي",
    "هاتف", "جوال", "موبايل", "تابلت", "لوحي", "ايباد", "آيباد",
    "ساعة", "ساعه", "ذكية", "سوار ذكي",
    "بلوتوث", "شاحن", "شواحن", "شحن سريع", "باور بانك", "باوربانك", "كابل", "كوابل", "كيبل", "كيابل", "سلك", "وصلة", "وصلات", "محول", "محولات", "كفر", "جراب", "حامل",
    "سبيكر", "مايك", "كاميرا", "درون", "بروجكتر", "بروجكتور", "بروجيكتور", "لابتوب",
    "لاسلكي", "وايرلس", "بي سي", "حاسوب", "كمبيوتر", "كارت شاشة", "كرت شاشة", "معالج", "رام", "رامات", "مذربورد", "لوحة ام",
    "قرص صلب", "هارد ديسك", "فلاش ديسك", "فلاشة", "بطاقة ذاكرة", "كارت ميموار", "تخزين", "اس اس دي", "ان في ام اي", "ساتا",
    "مفك", "مفكات", "طقم مفكات", "أداة", "اداة", "أدوات", "ادوات", "دريل", "صيانة", "لحام", "كاوية لحام",
    "معجون حراري", "بوتي حراري", "وسادة حرارية", "تبريد", "تبريد مائي", "مروحة", "مراوح", "مشتت",
    "هونر", "هواوي", "شاومي", "ريدمي", "بوكو", "سامسونج", "ايفون", "آيفون",
    "ريلمي", "انفينكس", "تكنو", "نوبيا", "لينوفو", "اسوس", "باد ماوس", "ماوس باد",
    "سويتش", "سويتشات", "عتاد", "صيدة", "يو اس بي", "تايب سي",
]


def is_allowed_category(title: str, text: str, channel_username: str = "") -> Tuple[bool, Optional[str]]:
    """Check if the deal belongs to an allowed category (gaming, tech, PC parts, cables, tools, phones, etc.)."""
    clean_ch = channel_username.lower().lstrip("@")
    monitored_tech_channels = {
        "pcgamingpart", "bnddeals", "zedstoreonline", "aniscoupons", "ecksdeal",
        "lodydeals", "megaprix", "megaphonna", "coupon4dz", "francecp", "alifrdrop",
        "couponsglobal"
    }
    # Curated channels are specialized tech/deal channels curated by the user
    if clean_ch in monitored_tech_channels:
        return True, None

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

    return False, f"Category not allowed (not tech/gaming/phone/tool): {title[:60]}"

def is_spam_or_non_deal(text: str) -> Tuple[bool, Optional[str]]:
    if not text or len(text.strip()) < 10:
        return True, "Message is too short or empty"

    lower_text = text.lower()

    for indicator in NON_DEAL_INDICATORS:
        if indicator in lower_text:
            return True, f"Non-deal announcement or promotional meta post: {indicator}"

    for store in BLOCKED_STORE_KEYWORDS:
        if store in lower_text:
            return True, f"Blocked store or platform detected: {store}"

    # Skip dead / ephemeral random coupons / lucky draw lottery posts
    # BUT allow coupon claim posts that contain actual AliExpress links (competitors post these as engagement)
    random_coupon_kws = ["كوبونات عشوائية", "سحب عشوائي", "يمد في كوبونات", "عشوائية", "عشوائيه"]
    has_random_coupon = any(k in lower_text for k in random_coupon_kws)
    has_ali_link = "aliexpress.com" in lower_text or "s.click.aliexpress" in lower_text
    has_claim_action = any(k in lower_text for k in ["احجز", "احجزها", "يوزع في كوبونات", "عودة الكوبونات", "رجعت الكوبونات"])
    if has_random_coupon and not has_ali_link and not has_claim_action:
        return True, "Dead / temporary random coupon draw post skipped"

    return False, None

def extract_coupon_list(text: str) -> List[Dict[str, str]]:
    """
    Extracts coupons from explicit coupon bulletin lists.
    Strips Arabic tatweels and handles:
    - Tier then Code: 'كوبون 2/15$ : OTPRD02', '🎟️ 2/15$ : OTPRD02', 'خصم 2/15$ بكود OTPRD02'
    - Code then Tier: 'OTPRD02 : 2/15$', 'كود OTPRD02 (2/15$)'
    - Multi-line or single-line formats.
    """
    if not text:
        return []

    # Strip Arabic tatweels (\u0640)
    norm = re.sub(r'[\u0640]', '', text)

    # 1. Tier then Code
    p1 = re.compile(
        r'(?P<kw>🎟️?|🎫|•|\-|\*)?[^\S\r\n]*(?P<kw2>كوبون|كود|code|قسيمة|خصم)?[^\S\r\n]*(?P<tier>[$]?[0-9]+(?:\.[0-9]+)?[^\S\r\n]*/[^\S\r\n]*[$]?[0-9]+(?:\.[0-9]+)?[$]?)[^\S\r\n]*(?:بكود|code|:|=|：|\-)?[^\S\r\n]*\r?\n?[^\S\r\n]*(?P<code>[A-Za-z0-9_-]{4,25})',
        re.IGNORECASE
    )

    # 2. Code then Tier
    p2 = re.compile(
        r'(?P<kw>🎟️?|🎫|•|\-|\*)?[^\S\r\n]*(?P<kw2>كوبون|كود|code|قسيمة)?[^\S\r\n]*(?P<code>[A-Za-z][A-Za-z0-9_-]{3,24})[^\S\r\n]*(?:[:=：\-]|خصم|بخصم|\()?[^\S\r\n]*\r?\n?[^\S\r\n]*(?P<tier>[$]?[0-9]+(?:\.[0-9]+)?[^\S\r\n]*/[^\S\r\n]*[$]?[0-9]+(?:\.[0-9]+)?[$]?)\)?',
        re.IGNORECASE
    )

    coupons = []
    seen_codes = set()
    blacklist = {'http', 'https', 'aliexpress', 'item', 'link', 't.me', 'camera', 'battery', 'android', 'snapdragon', 'display', 'screen'}

    def add_coupon(tier_str, code_str, has_kw):
        c = code_str.strip().upper()
        if c.lower() in blacklist or any(b in c.lower() for b in ['http', 't.me', 'click']):
            return
        if not re.search(r'[A-Za-z]', c):
            return
        # If tier has no dollar sign (e.g. 8/256), ensure explicit coupon context exists
        if '$' not in tier_str and not has_kw:
            return
        t = re.sub(r'\s+', '', tier_str.strip())
        if not t.startswith('$') and not t.endswith('$'):
            t = f"{t}$"
        if c not in seen_codes:
            seen_codes.add(c)
            coupons.append({"tier": t, "code": c})

    for m in p1.finditer(norm):
        has_kw = bool((m.group('kw') and m.group('kw') in '🎟️🎫') or m.group('kw2'))
        add_coupon(m.group('tier'), m.group('code'), has_kw)

    for m in p2.finditer(norm):
        has_kw = bool((m.group('kw') and m.group('kw') in '🎟️🎫') or m.group('kw2'))
        add_coupon(m.group('tier'), m.group('code'), has_kw)

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
    norm = re.sub(r'[\u0640]', '', text)
    for pattern in COUPON_PATTERNS:
        m = pattern.search(norm)
        if m:
            code = m.group(1).strip()
            if code.lower() not in {"http", "https", "aliexpress", "item", "link", "url", "temu"}:
                return code.upper()
    return None

def extract_seller_coupon(text: str) -> Optional[str]:
    if not text:
        return None
    norm = re.sub(r'[\u0640]', '', text)

    # 1. Combined amount and code: e.g. "حصل قسيمة البائع $80: T0F4TZ" or "قسيمة المتجر $35: TJD5MT" or "قسيمة البائع $2: SEP908KKLL / JULYHHKKLL88"
    p_combined = re.search(
        r'(?:حصل\s*|احجز\s*)?قسيمة\s*(?:البائع|المتجر|خاصة\s*بالمتجر)\s*[:：\-\s✅🔥👉✔️🌷🙏\+]*[$]?\s*([0-9]+(?:\.[0-9]+)?)\s*[$]?\s*[:：\-\s]+\s*([A-Za-z0-9_\-\s/]{3,35})',
        norm,
        re.IGNORECASE
    )
    if p_combined:
        amount = p_combined.group(1).strip()
        code = p_combined.group(2).strip()
        code = code.split('\n')[0].strip()
        code = re.sub(r'[🎟️🎫👊🔗📌].*$', '', code).strip()
        # Remove any trailing Arabic commentary (e.g. احجزها, سارع قبل النفاذ)
        code = re.sub(r'[\u0600-\u06FF].*$', '', code).strip()
        try:
            if amount and float(amount) < 1.0:
                return None
        except ValueError:
            pass
        if code and code.lower() not in {"http", "https", "aliexpress", "link", "url", "temu"}:
            return f"{amount}$ (كود: {code})"

    # 2. Standard SELLER_COUPON_PATTERNS (amount or code)
    for pattern in SELLER_COUPON_PATTERNS:
        m = pattern.search(norm)
        if m:
            code = m.group(1).strip()
            # If purely numerical or dollar amount, ensure it is at least $1.00
            num_clean = re.sub(r'[^\d\.]', '', code)
            try:
                if num_clean and float(num_clean) < 1.0:
                    continue  # Ignore trivial sub-dollar coupons like 0.9$
            except ValueError:
                pass
            return code
    return None


def detect_points_discount(text: str) -> bool:
    if not text:
        return False
    for pattern in POINTS_PATTERNS:
        if pattern.search(text):
            return True
    return False

def extract_country_instruction(text: str, url: str = "", title: str = "") -> str:
    """
    Intelligently detects which country setting is needed for maximum discount.
    1. Reads explicit mentions or flags in text or url (Canada 🇨🇦, Korea 🇰🇷, Algeria 🇩🇿, France 🇫🇷, Spain 🇪🇸, Ukraine 🇺🇦, Australia 🇦🇺).
    2. Defaults to Canada 🇨🇦 for coins and tech deals (standard 50-70%+ coin discounts).
    """
    combined = f"{text or ''} {url or ''}".lower()

    # 1. Canada detection
    if any(k in combined for k in ["كندا", "🇨🇦", "canada", "cad", "shiptocountry=ca", "country=ca"]):
        return "كندا 🇨🇦"

    # 2. Korea detection (only when explicitly specified in source post or URL)
    if any(k in combined for k in ["كوريا", "🇰🇷", "korea", "krw", "shiptocountry=kr", "country=kr"]):
        return "كوريا 🇰🇷"

    # 3. Algeria detection (rare cases: local shipping / DZ coin promo)
    if any(k in combined for k in ["الجزائر", "🇩🇿", "algeria", "shiptocountry=dz", "country=dz", "ديرو الجزائر", "بلاد الجزائر", "حساب جزائري"]):
        return "الجزائر 🇩🇿"

    # 4. France detection
    if any(k in combined for k in [
        "فرنسا", "🇫🇷", "france", "shiptocountry=fr", "country=fr",
        "european", "version européenne", "version europeenne", "livraison france",
        "francecp", "alifrdrop"
    ]) or re.search(r'\bfr(?:prd|ld|cd)?[0-9]{1,4}\b', combined):
        return "فرنسا 🇫🇷"

    # 5. Spain detection
    if any(k in combined for k in ["إسبانيا", "اسبانيا", "🇪🇸", "spain", "shiptocountry=es"]):
        return "إسبانيا 🇪🇸"

    # 5.5 Ukraine detection (frequent for low smartphone prices)
    if any(k in combined for k in ["أوكرانيا", "اوكرانيا", "🇺🇦", "ukraine", "shiptocountry=ua"]):
        return "أوكرانيا 🇺🇦"

    # 5.6 Australia detection
    if any(k in combined for k in ["استراليا", "أستراليا", "🇦🇺", "australia", "shiptocountry=au"]):
        return "أستراليا 🇦🇺"

    # Default to Canada 🇨🇦 for all coins / general tech deals
    return "كندا 🇨🇦"

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

    # 0. Look for explicit star bullet title line (ZedStore & top Algerian channels standard: ⭐️ [Title])
    for i, line in enumerate(lines):
        if any(s in line for s in ["⭐️", "⭐", "🌟"]):
            cand = re.sub(r'^[⭐️⭐🌟\s\-:]+', '', line).strip()
            if (not cand or len(cand) < 3) and i + 1 < len(lines):
                cand = lines[i + 1].strip()
                if i + 2 < len(lines) and not any(k in lines[i + 2] for k in ['$', '€', 'السعر', 'احجز', 'كوبون', 'رابط', '🔗', '💵']):
                    cand += ' ' + lines[i + 2].strip()
            cand = re.sub(r'[\$€💵].*$', '', cand).strip()
            cand = re.sub(r'https?://\S+', '', cand).strip()
            if not is_noisy(cand) and len(cand) >= 3:
                return cand[:100]

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


def is_france_deal(text: str, url: str = "", country_info: Optional[str] = None) -> bool:
    """
    Detects if a deal or coupon is specifically intended for France/Europe and NOT Algeria.
    Prevents French offers from ever leaking into Algerian channel @DzAliexpress0.
    """
    if country_info and any(k in str(country_info).lower() for k in ["فرنسا", "france", "fr"]):
        return True
    combined = f"{text or ''} {url or ''}".lower()
    france_keywords = [
        "فرنسا", "🇫🇷", "france", "shiptocountry=fr", "country=fr",
        "توصيل لفرنسا", "توصيل فرنسا", "livraison france", "vers la france",
        "pour la france", "france seulement", "خاص بفرنسا", "فرنسا فقط",
        "فقط لفرنسا", "كودات فرنسا", "كوبونات فرنسا", "codes promo france",
        "@francedealsdz", "francedealsdz", "livraison : france",
        "livraison en france", "livré en france", "livraison gratuite en france",
        "bon plan france", "prix constaté"
    ]
    if any(k in combined for k in france_keywords):
        return True
    if re.search(r'\bfr\d{2,3}\b', combined):
        return True
    return False

def detect_deal_type(raw_text: str, url: str = "") -> str:
    """
    Intelligently determines whether a deal is a 'bundle', 'coin', or standard 'item' deal.
    - Bundle deals: Choice Bundle / 3 items / sourceType=562.
    - Coin deals: explicitly mentions coins/points AND is a small gadget/peripheral.
    - Standard item deals: phones, tablets, or coupon-only deals (canonical item page).
    """
    text_lower = (raw_text or "").lower()
    url_lower = (url or "").lower()

    bundle_keywords = [
        "bundle", "bundledraw", "bundledeals", "bundle deals", "bundledeals2",
        "300000512", "sourcetype=562", "sourcetype=620", "channel=bundle",
        "/bundledeals", "choice bundle", "حزم", "حزمة", "3 بـ", "3 ب ", "3بـ", "3ب",
        "3 منتجات", "3 items", "3 حبات", "ثلاث حبات", "ثلاث منتجات", "3 عروض",
        "باندل", "بندل", "حزم التوفير", "حزمة التوفير", "3 قطع", "3 سلع",
        "ثلاث سلع", "ثلاث قطع", "عرض 3", "عروض 3", "3 أجهزة", "3 اجهزة",
        "3 حبات بـ", "3 حبات ب", "3items", "3pcs", "سعر ثلاث قطع", "سعر 3 قطع",
        "سعر 3 حبات", "سعر ثلاث حبات", "رابط الباندل", "رابط البندل"
    ]
    if any(k in text_lower for k in bundle_keywords) or any(k in url_lower for k in bundle_keywords):
        return "bundle"

    if re.search(r'\b3\s*ب(?:ـ|\s|[0-9]|$)', text_lower):
        return "bundle"
    if re.search(r'bundle\s*deal', text_lower):
        return "bundle"
    if re.search(r'3\s*(?:items|منتجات|حبات|قطع|سلع)', text_lower):
        return "bundle"
    if re.search(r'300000512|sourcetype=(?:562|620)|bundledeals', url_lower):
        return "bundle"

    # Coin deals: only if text explicitly mentions coins / points discount
    coin_keywords = [
        "عملات", "نقاط", "coins", "تخفيض العملات", "رابط العملات", "خصم العملات", "سعر العملات"
    ]
    if any(k in text_lower for k in coin_keywords):
        if any(w in text_lower for w in ["phone", "redmi", "poco", "xiaomi", "realme", "oneplus", "oppo", "هاتف", "تابلت", "ipad", "pad"]):
            return "item"
        return "coin"

    return "coin"


def detect_restock_deal(text: str) -> bool:
    """
    Detects if an incoming Telegram deal post is an urgent Restock / Return announcement.
    Matches Algerian deal channel patterns like:
    - عودة العرض, عودة التوفر, عودة توفر, رجع العرض, رجع توفر, عاد للتوفر, توفر من جديد
    - حبات قلال, حبات قليلة, حبات قلا, بقاو حبات, كمية محدودة جدا, عدد قليل
    - الححححق عودة, الحقوو عودة, سارع قبل النفاذ, قبل ما يخلاص
    """
    if not text:
        return False
    t = text.lower()

    # 1. Direct explicit phrases
    phrases = [
        "عودة العرض", "عودة التوفر", "عودة توفر", "رجع العرض", "رجع توفر",
        "توفر من جديد", "توفر مجددا", "عاد للتوفر", "رجع للتوفر", "رجعت توفرت",
        "عاود توفر", "عاود رجع", "حبات قلال", "حبات قليلة", "حبات قلا",
        "بقايا حبات", "بقاو حبات", "كمية محدودة جدا", "كمية قليلة جدا", "عدد قليل",
        "سارع قبل النفاذ", "سارعوا قبل نفاذ الكمية", "قبل ما يخلاص", "قبل نفاذ المخزون",
        "الحق عودة", "الحححق عودة", "الحقوو عودة", "الحقوا عودة", "الحقق عودة"
    ]
    if any(p in t for p in phrases):
        return True

    # 2. Co-occurrence: (الحق / سارع / اجري) + (توفر / رجع / عودة / حبات / مخزون)
    has_urgency = any(u in t for u in ["الحق", "الحححق", "الحقو", "الحقوا", "سارع", "سارعوا", "اجري", "لحق روحك"])
    has_stock = any(s in t for s in ["توفر", "رجع", "رجعت", "عودة", "حبات", "مخزون", "ستوك", "stock"])
    if has_urgency and has_stock:
        return True

    # 3. French Restock Phrases
    french_restock_phrases = [
        "restock", "re-stock", "retour en stock", "de retour en stock",
        "de nouveau disponible", "nouveau en stock", "remise en stock",
        "stock limité", "quantité limitée", "quantités limitées",
        "quelques pièces", "dernières pièces", "derniers stocks",
        "dépêchez-vous", "faites vite", "avant rupture"
    ]
    if any(p in t for p in french_restock_phrases):
        return True

    # 4. Regex matches
    if re.search(r'حبات\s*(?:قلال|قليلة|قلا|معدودة)', t):
        return True
    if re.search(r'عود[ةه]\s*(?:ال(?:عرض|توفر)|توفر|سلع)', t):
        return True
    if re.search(r'رجعت?\s*(?:توفر|توفرت|العرض)', t):
        return True

    return False


def detect_price_drop_deal(text: str) -> bool:
    """
    Detects if an incoming Telegram deal post mentions a price drop / price cut.
    Works for both French and Algerian / Arabic deal channel styles.
    """
    if not text:
        return False
    t = text.lower()
    price_drop_keywords = [
        # French
        "baisse de prix", "prix en baisse", "nouveau prix", "prix réduit", "prix cassé",
        "prix en chute", "chute de prix", "encore moins cher", "prix encore plus bas",
        "baisse supplémentaire", "prix en promo", "chute du prix", "baisse de tarif",
        # Arabic / Algerian
        "انخفاض السعر", "هبوط السعر", "نزل السعر", "طاح السعر", "طيحة فالسعر",
        "سعر جديد منخفض", "سعر جديد أقل", "تخفيض إضافي", "تخفيض جديد", "زاد هبط",
        "أرخص من قبل", "ارخص من قبل", "نقص السعر"
    ]
    return any(k in t for k in price_drop_keywords)


def detect_channel_announcement(text: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Detects non-deal informational bulletins or service notices from monitored channels:
    - China national holidays / Golden Week / Spring festival shipping delays.
    - Coupon return / refresh announcements (الحق عودة الكوبونات احجزها).
    - Customs & parcel alerts (الجمارك / الطرود).
    Returns (is_announcement, formatted_text, tag).
    """
    if not text:
        return False, None, None
    t = text.lower()

    # 0. Coupon Return / Refresh Announcements (checked FIRST because they contain AliExpress links)
    coupon_return_kws = [
        "عودة الكوبونات", "رجعت الكوبونات", "كوبونات جديدة", "كوبونات عشوائية",
        "يوزع في كوبونات", "يوزع كوبونات", "توزيع كوبونات", "احجز الكوبونات",
        "احجز كوبونات", "كوبونات مجانية"
    ]
    coupon_action_kws = ["احجز", "احجزها", "سارع", "الحق", "اجري"]
    has_coupon_return = any(k in t for k in coupon_return_kws)
    has_action = any(k in t for k in coupon_action_kws)
    has_ali_link_ann = "aliexpress.com" in t or "s.click.aliexpress" in t
    if has_coupon_return and (has_action or has_ali_link_ann):
        ali_link_match = re.search(r'https?://s\.click\.aliexpress\.com/e/[A-Za-z0-9_-]+', text)
        ali_link = ali_link_match.group(0) if ali_link_match else "https://www.aliexpress.com"
        formatted = (
            "🎟️ <b>الحقوووا عودة الكوبونات.. احجزوها قبل ما تخلاص! 🏃‍♂️🔥</b>\n\n"
            "AliExpress رجعت توزع في <b>كوبونات خصم عشوائية</b> 🎁\n"
            "احجزوها الآن مباشرة قبل نفاذها:\n\n"
            f"🔗 <b>رابط حجز الكوبونات ⤵️</b>\n{ali_link}\n\n"
            "📌 <b>ملاحظة:</b> حوّل دولة التطبيق إلى نفس عنوان الشحن 🇩🇿\n\n"
            "📢 @DzAliexpress0"
        )
        return True, formatted, "coupon_return_refresh"

    # Skip remaining checks if text contains actual product affiliate links (deal posts, not announcements)
    if any(k in t for k in ["s.click.aliexpress.com", "/item/", "bundledeals", "coin-index"]):
        return False, None, None

    # 1. China Holiday / Shipping Delays (e.g. October Golden Week or Spring Festival)
    china_holiday_kws = ["عطلة في الصين", "عطلة الصين", "العيد الوطني في الصين", "العيد الوطني الصيني", "رأس السنة الصينية"]
    shipping_delay_kws = ["تتأخر في الشحن", "تأخر في الشحن", "تأخر الشحن", "تأخير في الشحن", "تأخير الشحن", "توقف الشحن"]

    if any(k in t for k in china_holiday_kws) or (any(k in t for k in shipping_delay_kws) and ("صين" in t or "china" in t)):
        m_date = re.search(r'حتى\s*(?:يوم\s*)?([0-9]+\s*[^\s\n\.,]+)', text)
        date_str = m_date.group(0) if m_date else "خلال هذه الفترة"
        formatted = (
            "⚠️ <b>تنويه هـام لمتابعينا الكرام 🇨🇳📦</b>\n\n"
            "نحيطكم علماً بأنه توجد حالياً <b>عطلة رسمية في الصين</b> "
            f"({date_str}).\n\n"
            "📌 <b>ملاحظة هامة:</b>\n"
            "▫️ بعض المتاجر والبائعين في AliExpress قد يتأخرون قليلاً في تجهيز وشحن الطلبيات خلال هذه الفترة.\n"
            "▫️ العروض والأسعار المنشورة مستمرة كالمعتاد بدون أي توقف، ولكن الشحن سينطلق فور انتهاء فترة العطلة إن شاء الله ✈️\n\n"
            "تسوق ممتع وبالتوفيق للجميع 🤍🛒"
        )
        return True, formatted, "china_holiday_shipping_delay"

    # 2. Algerian Customs / Postal notices
    customs_kws = ["جمارك", "الجمارك", "طرود الجمارك", "مركز الفرز", "بريد الجزائر"]
    if any(k in t for k in customs_kws) and any(w in t for w in ["تنبيه", "تنويه", "إشعار", "توقف", "حجز", "قانون"]):
        clean = re.sub(r'@[A-Za-z0-9_]+', '', text)
        clean = re.sub(r'https?://t\.me/[A-Za-z0-9_]+', '', clean).strip()
        formatted = (
            "📢 <b>إشعار هـام لمتابعينا 📦🇩🇿</b>\n\n"
            f"{clean}\n\n"
            "📌 <i>نوافيكم دائماً بكل جديد ومستجدات الشحن والتسوق من AliExpress أولاً بأول ✨</i>"
        )
        return True, formatted, "customs_postal_notice"

    return False, None, None


