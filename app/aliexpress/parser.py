import re
from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict, Any
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
    re.compile(
        r'(?:code\s*promo|code\s*de\s*r[ée]duction|code\s*r[ée]duction|bon\s*de\s*r[ée]duction|(?:ال)?كوبون(?:\s*الخصم|\s*التخفيض)?|(?:ال)?كود(?:\s*الخصم|\s*التخفيض)?|(?:ال)?قسيمة|coupon|code|promo)\s*'
        r'(?:[-–]?\s*[$€]?[0-9]+(?:[\.,][0-9]+)?[^\S\r\n]*(?:/[^\S\r\n]*[$€]?[0-9]+(?:[\.,][0-9]+)?)?[^\S\r\n]*(?:€|eur|euro|euros|دولار|dollar|\$)?)?'
        r'[\s:：\-=ـ_•*~|()✅🔥👉✔️⏺🙏🎟️🎫💵💰🎁📌⚡💥🤐\r\n]*'
        r'(?:استخدمه|استخدم|استعمله|استعمل|انسخه|بكود|code|avec\s*le\s*code|utilisez\s*le\s*code)?'
        r'[\s:：\-=ـ_•*~|()✅🔥👉✔️⏺🙏🎟️🎫💵💰🎁📌⚡💥🤐\r\n]*'
        r'(?:<code>|\*\*|`)*'
        r'([A-Za-z0-9_-]{3,24})',
        re.IGNORECASE
    ),
    re.compile(
        r'(?:استخدم\s+كود|استعمل\s+كود|كود\s+الخصم|كود\s+التخفيض|كود\s+الشراء|كوبون\s+الخصم|كوبون\s+التخفيض|كوبون\s+خاص|(?:ال)?كود\s*[:：]|(?:ال)?كوبون\s*[:：]|code\s*promo|code\s*de\s*r[ée]duction|code\s*r[ée]duction|bon\s*de\s*r[ée]duction|utilisez\s*(?:le\s*)?code|avec\s*(?:le\s*)?code)\s*[:：\-=ـ_•*~|\s]*(?:<code>|\*\*|`)*([A-Za-z0-9_-]{3,24})',
        re.IGNORECASE
    ),
    re.compile(
        r'[🏷️🎟️🎫👊]\s*(?:كوبون|كود|code|coupon|promo)?\s*[:：\-\s\d\$/€\r\n]*(?:<code>|\*\*|`)*([A-Za-z0-9_-]{3,24})',
        re.IGNORECASE
    ),
    re.compile(
        r'(?:كود|كوبون|قسيمة|code|coupon|promo|خصم|تخفيض)[^\n]{0,60}?(?:<code>|`)([A-Za-z0-9_-]{3,24})(?:</code>|`)',
        re.IGNORECASE
    ),
]

SELLER_COUPON_PATTERNS = [
    re.compile(r'(?:حصل\s*|احجز\s*)?(?:(?:ال)?قسيمة|(?:ال)?كوبون|(?:ال)?كود)\s*(?:البائع|المتجر|خاصة\s*بالمتجر|store\s*coupon|seller\s*coupon|vendeur)[\s:：\-=ـ_•*~|()✅🔥👉✔️🌷🙏\+💵💰🎁\r\n]*[$€]?\s*([0-9]+(?:[\.,][0-9]+)?(?:\s*(?:دولار|dollar|€|eur|\$))?|[A-Za-z0-9_\-]{3,25})', re.IGNORECASE),
    re.compile(r'🌷\s*(?:(?:ال)?قسيمـ?ة\s*(?:البـ?ائع|المتجر)?|(?:كوبون|كود)\s*(?:المتجر|البائع)|coupon\s*vendeur|store\s*coupon)\s*[:：]?\s*(?:<code>|\*\*|`)*([0-9]+(?:[\.,][0-9]+)?\$?|[A-Za-z0-9_\-]{3,25})', re.IGNORECASE),
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
    (re.compile(r'(?:دولة|البلد|بلد الحساب|ضع البلد|خلي البلد|تحويل الحساب الى)\s*(?:التطبيق\s*الى)?\s*السعودية|🇸🇦', re.IGNORECASE), "السعودية 🇸🇦"),
    (re.compile(r'(?:دولة|البلد|بلد الحساب|ضع البلد|خلي البلد|تحويل الحساب الى)\s*(?:التطبيق\s*الى)?\s*(?:الإمارات|الامارات)|🇦🇪', re.IGNORECASE), "الإمارات 🇦🇪"),
    (re.compile(r'(?:دولة|البلد|بلد الحساب|ضع البلد|خلي البلد|تحويل الحساب الى)\s*(?:التطبيق\s*الى)?\s*قطر|🇶🇦', re.IGNORECASE), "قطر 🇶🇦"),
    (re.compile(r'(?:دولة|البلد|بلد الحساب|ضع البلد|خلي البلد|تحويل الحساب الى)\s*(?:التطبيق\s*الى)?\s*الكويت|🇰🇼', re.IGNORECASE), "الكويت 🇰🇼"),
    (re.compile(r'(?:دولة|البلد|بلد الحساب|ضع البلد|خلي البلد|تحويل الحساب الى)\s*(?:التطبيق\s*الى)?\s*البحرين|🇧🇭', re.IGNORECASE), "البحرين 🇧🇭"),
    (re.compile(r'(?:دولة|البلد|بلد الحساب|ضع البلد|خلي البلد|تحويل الحساب الى)\s*(?:التطبيق\s*الى)?\s*(?:عمان|عُمان)|🇴🇲', re.IGNORECASE), "عمان 🇴🇲"),
    (re.compile(r'(?:دولة|البلد|بلد الحساب|ضع البلد|خلي البلد|تحويل الحساب الى)\s*(?:التطبيق\s*الى)?\s*كندا|🇨🇦', re.IGNORECASE), "كندا 🇨🇦"),
    (re.compile(r'(?:دولة|البلد|بلد الحساب|ضع البلد|خلي البلد|تحويل الحساب الى)\s*(?:التطبيق\s*الى)?\s*كوريا|🇰🇷', re.IGNORECASE), "كوريا 🇰🇷"),
    (re.compile(r'(?:دولة|البلد|بلد الحساب|ضع البلد|خلي البلد|تحويل الحساب الى)\s*(?:التطبيق\s*الى)?\s*فرنسا|🇫🇷', re.IGNORECASE), "فرنسا 🇫🇷"),
    (re.compile(r'(?:ديرو|دير|بلاد|دولة|البلد|بلد الحساب|ضع البلد|خلي البلد)\s*(?:بلاد\s*|دولة\s*)?الجزائر|🇩🇿', re.IGNORECASE), "الجزائر 🇩🇿"),
    (re.compile(r'(?:دولة|البلد|بلد الحساب|ضع البلد|خلي البلد|تحويل الحساب الى)\s*(?:التطبيق\s*الى)?\s*(?:إسبانيا|اسبانيا)|🇪🇸', re.IGNORECASE), "إسبانيا 🇪🇸"),
    (re.compile(r'(?:دولة|البلد|بلد الحساب|ضع البلد|خلي البلد|تحويل الحساب الى)\s*(?:التطبيق\s*الى)?\s*(?:أوكرانيا|اوكرانيا)|🇺🇦', re.IGNORECASE), "أوكرانيا 🇺🇦"),
    (re.compile(r'(?:دولة|البلد|بلد الحساب|ضع البلد|خلي البلد|تحويل الحساب الى)\s*(?:التطبيق\s*الى)?\s*(?:أستراليا|استراليا)|🇦🇺', re.IGNORECASE), "أستراليا 🇦🇺"),
    (re.compile(r'(?:دولة|البلد|بلد الحساب|ضع البلد|خلي البلد|تحويل الحساب الى)\s*(?:التطبيق\s*الى)?\s*(?:بريطانيا|المملكة المتحدة)|🇬🇧', re.IGNORECASE), "المملكة المتحدة 🇬🇧"),
    (re.compile(r'(?:دولة|البلد|بلد الحساب|ضع البلد|خلي البلد|تحويل الحساب الى)\s*(?:التطبيق\s*الى)?\s*(?:البرازيل|برازيل)|🇧🇷', re.IGNORECASE), "البرازيل 🇧🇷"),
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
    "tws", "controller", "controllers", "gamepad", "gamepads", "joystick", "joysticks", "gaming", "gamer", "game",
    "monitor", "mechanical", "rgb", "dpi", "mouse pad", "mousepad",
    "iem", "iems", "in-ear", "in ear", "earphones", "headphones", "headsets",
    # IEM & Audio Brands
    "kz", "edx", "edx pro", "edx pro x", "castor", "zsn", "zs10", "cca", "tangzu",
    "wan'er", "waner", "moondrop", "chu", "space travel", "7hz", "zero", "salnotes",
    "qkz", "truthear", "gate", "hola", "simgot", "ew200", "kbear",
    # Gaming & PC Brands
    "attack shark", "ajazz", "machenike", "mchose", "mchose ax5", "mchose a5", "mchose g3", "mchose k99",
    "incott", "atk", "waizowl", "aula", "darmoshark", "vgn", "zaopin",
    "scyrox", "mad r", "vxe", "fantech", "keychron", "nuphy", "akko", "monsgeek",
    "wobkey", "rainy75", "crush80", "bridge75", "hi75", "hi8", "leobog", "epomaker",
    "royal kludge", "rk61", "redragon", "razer", "logitech", "steelseries", "corsair",
    "hyperx", "dareu", "thunderobot", "flydigi", "gamesir", "8bitdo", "gulikit",
    "easysmx", "mobapad", "iine", "dobe", "skull & co", "yunzii",
    # Sensor & Switch Tech
    "paw3395", "paw3950", "paw3311", "paw3370", "rapid trigger", "magnetic switch",
    "hall effect", "magnetic keyboard", "mechanical keyboard", "magnetic", "8k", "4k", "polling rate", "glass pad", "cordura",
    # Enthusiast brands
    "pulsar", "lamzu", "ninjutso", "sora", "maya", "thorn", "atlantis",
    "superlight", "g pro", "viper", "deathadder", "basilisk", "blackshark", "kraken",
    # GPU / CPU / PC parts & Specs
    "gpu", "graphics card", "video card", "vga", "apu", "cpu", "cpus", "processor", "processors",
    "amd", "intel", "ryzen", "intel core", "core i3", "core i5", "core i7", "core i9", "i3", "i5", "i7", "i9",
    "am4", "am5", "lga1700", "lga1200", "b450", "b550", "b650", "b760", "h610", "a520", "z790", "x670",
    "bc 250", "bc-250", "bc250", "gddr6", "gddr5", "gddr",
    "256-bit", "256bit", "192bit", "128bit", "rtx", "gtx", "radeon", "rx", "ram", "ssd", "hdd", "nvme", "ddr4", "ddr5",
    "gaming chair", "cooling", "cooler", "fan", "fans", "motherboard", "motherboards", "mainboard",
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
    "webcam", "web camera", "1080p", "60fps", "8mp", "2k", "4k", "autofocus",
    "camera", "drone", "action cam", "action camera", "gopro", "tripod",
    "dji", "osmo", "gimbal", "stabilizer",
    "ring light", "led strip", "projector", "magcubic", "hy300",
    # Computers
    "mini pc", "laptop", "notebook", "chromebook", "macbook", "pc", "computer", "desktop",
    # Generic tech & Smart Home Gadgets
    "wireless", "bluetooth", "rechargeable", "scale", "smart scale", "electronic scale",
]

ALLOWED_CATEGORY_KEYWORDS_AR = [
    "ميزان", "ميزان ذكي", "ميزان الكتروني", "ميزان إلكتروني",
    "ماوس", "كيبورد", "لوحة مفاتيح", "سماعة", "سماعات", "سماعات اذن", "سماعات أذن", "سماعة اذن", "سماعة أذن",
    "سماعات داخل الاذن", "سماعات داخل الأذن", "سماعة داخل الاذن", "سماعة داخل الأذن", "سماعة سلكية", "سماعات سلكية", "سماعة رأس", "سماعات رأس", "ايربودز", "إيربودز",
    "يد تحكم", "يد تحكم فخمة", "يدة تحكم", "ايادي تحكم", "أيادي تحكم", "يدات تحكم", "كنترولر", "كنترولرز", "جيمباد", "قيمباد", "ذراع تحكم", "يدة",
    "كيبورد مغناطيسي", "كيبورد ميكانيكي", "لوحة مفاتيح مغناطيسية", "لوحة مفاتيح ميكانيكية", "مغناطيسي", "ميكانيكي", "مغناطيسية", "ميكانيكية", "رابيد تريجر", "هول افكت", "هول إفكت",
    "جيمنج", "قيمنق", "جيمينق", "جايمنج", "العاب", "ألعاب", "شاشة", "كرسي",
    "هاتف", "جوال", "موبايل", "تابلت", "لوحي", "ايباد", "آيباد",
    "ساعة", "ساعه", "ذكية", "سوار ذكي",
    "بلوتوث", "شاحن", "شواحن", "شحن سريع", "باور بانك", "باوربانك", "كابل", "كوابل", "كيبل", "كيابل", "سلك", "وصلة", "وصلات", "محول", "محولات", "كفر", "جراب", "حامل",
    "سبيكر", "مايك", "ميكروفون", "مايكروفون", "كاميرا", "درون", "بروجكتر", "بروجكتور", "بروجيكتور", "لابتوب",
    "لاسلكي", "وايرلس", "بي سي", "حاسوب", "كمبيوتر", "كارت شاشة", "كرت شاشة", "معالج", "معالجات", "رام", "رامات", "مذربورد", "لوحة ام", "لوحة أم",
    "قرص صلب", "هارد ديسك", "فلاش ديسك", "فلاشة", "بطاقة ذاكرة", "كارت ميموار", "تخزين", "اس اس دي", "ان في ام اي", "ساتا",
    "مفك", "مفكات", "طقم مفكات", "أداة", "اداة", "أدوات", "ادوات", "دريل", "صيانة", "لحام", "كاوية لحام",
    "معجون حراري", "بوتي حراري", "وسادة حرارية", "تبريد", "تبريد مائي", "مروحة", "مراوح", "مشتت",
    "هونر", "هواوي", "شاومي", "ريدمي", "بوكو", "سامسونج", "ايفون", "آيفون",
    "ريلمي", "انفينكس", "تكنو", "نوبيا", "لينوفو", "اسوس", "باد ماوس", "ماوس باد",
    "لوجيتك", "لوجيتيك", "اجاز", "أجاز", "امشوز", "ام شوز", "مشوز", "ماتشوز",
    "كاميرا ويب", "ويب كام", "ويبكام", "كاميرا حاسوب", "كاميرا كمبيوتر",
    "كيزيد", "كي زي", "كي زيد", "موندروب", "تانغزو",
    "سويتش", "سويتشات", "عتاد", "صفقة", "يو اس بي", "تايب سي",
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

    # Reject competitor affiliate-exclusive deals
    is_aff, aff_reason = is_affiliate_exclusive_deal(text)
    if is_aff:
        return True, f"Competitor affiliate-exclusive deal rejected: {aff_reason}"

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

    tier_pattern = r'[$]?[0-9]+(?:\.[0-9]+)?[$]?[^\S\r\n]*(?:/|-)[^\S\r\n]*[$]?[0-9]+(?:\.[0-9]+)?[$]?'

    # 1. Tier then Code
    p1 = re.compile(
        r'(?:[^\w\s]|•|-|\*)?[^\S\r\n]*(?:كوبون|كود|code|قسيمة|خصم)?[^\S\r\n]*(?P<tier>' + tier_pattern + r')[^\S\r\n]*(?:بكود|code|:|=|：|-)?' + r'[^\S\r\n]*\r?\n?[^\S\r\n]*(?P<code>[A-Za-z0-9_-]{4,25})',
        re.IGNORECASE
    )

    # 2. Code then Tier
    p2 = re.compile(
        r'(?:[^\w\s]|•|-|\*)?[^\S\r\n]*(?:كوبون|كود|code|قسيمة)?[^\S\r\n]*(?P<code>[A-Za-z][A-Za-z0-9_-]{3,24})[^\S\r\n]*(?:[:=：\-]|خصم|بخصم|\()?[^\S\r\n]*\r?\n?[^\S\r\n]*(?P<tier>' + tier_pattern + r')\)?',
        re.IGNORECASE
    )

    coupons = []
    seen_codes = set()
    blacklist = {'http', 'https', 'aliexpress', 'item', 'link', 't.me', 'camera', 'battery', 'android', 'snapdragon', 'display', 'screen'}

    def add_coupon(tier_str, code_str, has_kw):
        c = code_str.strip().upper()
        if c.lower() in blacklist or any(b in c.lower() for b in ['http', 't.me', 'click']):
            return
        if not re.search(r'[A-Za-z]', c) or is_competitor_branded_code(c):
            return
        # If tier has no dollar sign (e.g. 8/256), ensure explicit coupon context exists
        if '$' not in tier_str and not has_kw:
            return
        t = re.sub(r'\s+', '', tier_str.strip())
        m_tier = re.match(r'[$]?([0-9]+(?:\.[0-9]+)?)[$]?[^\S\r\n]*(?:/|-)[^\S\r\n]*[$]?([0-9]+(?:\.[0-9]+)?)[$]?', t)
        if m_tier:
            val1, val2 = float(m_tier.group(1)), float(m_tier.group(2))
            disc = min(val1, val2)
            spend = max(val1, val2)
            disc_str = f"{int(disc)}" if disc.is_integer() else f"{disc}"
            spend_str = f"{int(spend)}" if spend.is_integer() else f"{spend}"
            t = f"{disc_str}/{spend_str}$"
        else:
            if not t.startswith('$') and not t.endswith('$'):
                t = f"{t}$"
        if c not in seen_codes:
            seen_codes.add(c)
            coupons.append({"tier": t, "code": c})

    for m in p1.finditer(norm):
        has_kw = bool(m.group(0) and any(sym in m.group(0) for sym in ['🎟️', '🎫', 'كوبون', 'كود', 'قسيمة', 'خصم']))
        add_coupon(m.group('tier'), m.group('code'), has_kw)

    for m in p2.finditer(norm):
        has_kw = bool(m.group(0) and any(sym in m.group(0) for sym in ['🎟️', '🎫', 'كوبون', 'كود', 'قسيمة', 'خصم']))
        add_coupon(m.group('tier'), m.group('code'), has_kw)

    return coupons

def detect_coupon_event_type(text: str, promo_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Intelligently analyzes whether a coupon bulletin post from competitor channels
    (e.g. ECKSDEAL, lodydeals, zedstoreonline, aniscoupons) is:
    1. A Special / Restricted Event (e.g. Brand Day, category/brand sales):
       - Coupons ONLY apply to products on a dedicated landing page.
       - Signals: 'بعض المنتجات فقط', 'الموجودة في هذه الصفحة', 'صفحة العرض', 'المنتجات المؤهلة', 'Brand Day'.
       - Shoppers must be directed to the eligible landing page.
    2. A General / Site-Wide Event (e.g. Choice Day, 11.11, Anniversary Sale):
       - Coupons apply across the entire site.
       - Shoppers reserve/lock coupons by applying them to a dummy phone / high-value item ('حجز الكوبونات').
    """
    if not text:
        return {
            "is_restricted": False,
            "is_sitewide_booking": False,
            "landing_url": None,
            "reason": "empty_text"
        }

    norm = re.sub(r'[\u0640]', '', text).lower()
    promo_lower = (promo_name or "").lower()

    # Restricted keywords (coupons work ONLY on specific landing page items)
    restricted_keywords = [
        "بعض المنتجات فقط", "في بعض المنتجات فقط", "الموجودة في هذه الصفحة",
        "الموجوده في هذه الصفحه", "في هذه الصفحة", "في هذه الصفحه",
        "صفحة العرض", "صفحه العرض", "صفحة التخفيضات", "صفحة التخفيض",
        "صفحة المنتجات", "صفحة الكوبونات", "المنتجات المؤهلة", "منتجات مؤهلة",
        "المنتجات المؤهله", "منتجات مؤهله", "خاصة بمنتجات هذه الصفحة",
        "خاصة بهذه الصفحة", "في هذه الصفحة فقط", "على هذه الصفحة فقط",
        "منتجات مختارة", "سلع مختارة", "منتجات محددة", "سلع محددة",
        "brand day", "براند داي", "brands day", "mega brands",
        "sur cette page", "produits éligibles", "sélection de produits",
        "eligible items only", "landing page only", "selected products"
    ]

    is_restricted = any(kw in norm for kw in restricted_keywords) or ("brand" in promo_lower)

    # Booking keywords (general sitewide promo with dummy product coupon locking)
    booking_keywords = [
        "حجز الكوبونات", "احجز الكوبونات", "تثبيت الكوبونات", "حجز وتثبيت",
        "حجز وتثبيت الكوبونات", "طبقوا الآن كامل الكوبونات", "طبقوا كامل الكوبونات",
        "طبقوها على هذا المنتج", "طبقوا على هذا المنتج", "تبقالكم في الحساب",
        "تبقى في الحساب", "تثبيت في الحساب", "حفظ الكوبونات", "طريقة الحجز"
    ]
    is_sitewide_booking = any(kw in norm for kw in booking_keywords)

    # If restricted indicators are present, it overrides generic booking wording
    if is_restricted:
        is_sitewide_booking = False

    # Extract landing page URL if restricted
    landing_url = None
    # 1. Search for link immediately following landing page notice
    m_near = re.search(
        r'(?:هذه الصفحة|صفحة العرض|المنتجات المؤهلة|رابط العرض|رابط المنتجات|رابط الكوبونات)[^\n]*[\s:：\-=ـ_•*~|()✅🔥👉✔️🌷🙏\+]*\r?\n[^\S\r\n]*(https?://[^\s]+)',
        text,
        re.IGNORECASE
    )
    if m_near:
        landing_url = m_near.group(1).strip()
    else:
        # 2. Search for any AliExpress link in text
        all_links = re.findall(r'https?://[^\s]+', text)
        ali_links = [u for u in all_links if "aliexpress" in u.lower() or "s.click" in u.lower()]
        if ali_links:
            landing_url = ali_links[0].strip()

    return {
        "is_restricted": is_restricted,
        "is_sitewide_booking": is_sitewide_booking,
        "landing_url": landing_url,
        "reason": "restricted_keywords_found" if is_restricted else ("booking_keywords_found" if is_sitewide_booking else "standard")
    }

def extract_prices(text: str) -> Tuple[Optional[float], Optional[float]]:
    usd_val: Optional[float] = None
    eur_val: Optional[float] = None

    if not text:
        return None, None

    # Step 1: Strip BiDi controls, zero-width chars, BOM, and normalize Unicode whitespace
    text = re.sub(r'[\u200e\u200f\u200b\u200c\u200d\u202a-\u202e\u2066-\u2069\ufeff]', '', text)
    text = re.sub(r'[\u00a0\u1680\u2000-\u200a\u202f\u205f\u3000]', ' ', text)
    text = re.sub(r'[\u0640]', '', text)  # tatweel

    # Step 2: Normalize Eastern Arabic-Indic numerals (٠-٩) and Persian numerals (۰-۹) to ASCII (0-9)
    arabic_digits = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789")
    text = text.translate(arabic_digits)

    # Step 3: Normalize Arabic decimal separators (٫, ،) between digits to dot
    text = re.sub(r'(?<=\d)[٫،](?=\d)', '.', text)

    eur_rate = float(getattr(settings, "EUR_USD_RATE", 0.92) or 0.92)

    def _parse_candidate_price(raw_num_str: str, full_context_str: str) -> Tuple[Optional[float], Optional[float]]:
        try:
            val = float(raw_num_str.replace(",", "."))
        except (ValueError, TypeError):
            return None, None

        if not (0.01 <= val <= 100000):
            return None, None

        context_lower = full_context_str.lower()

        # DZD / Algerian dinars
        if any(cur in context_lower for cur in ["دج", "د.ج", "da", "dzd"]) or ("دينار" in context_lower):
            usdt_rate = 250.0
            u = round(val / usdt_rate, 2)
            e = round(u * eur_rate, 2)
            return u, e

        if "€" in full_context_str or "eur" in context_lower or "euro" in context_lower:
            u = round(val / eur_rate, 2)
            return u, val

        # Default USD
        return val, round(val * eur_rate, 2)

    # Priority 1: High-confidence discounted / coin / post-coupon / final prices
    discounted_price_patterns = [
        # Coins / Points discounts: 'السعر بعد العملات : 0.60$' or 'السعر في خانة العملات : 0.60$' or 'بالنقاط 0.60$'
        re.compile(
            r'(?:السعر\s*(?:في|بـ?|مع|بعد|بتخفيض)?\s*(?:خانة\s*)?(?:العملات|نقاط|النقاط)|سعر\s*(?:في|بـ?|مع|بعد|بتخفيض)?\s*(?:خانة\s*)?(?:العملات|نقاط|النقاط)|(?:بعد|مع|بتخفيض|في\s*خانة|بخانة)\s*(?:العملات|النقاط|نقاط))'
            r'[\s:：\-–=ـ•*~|]*[\$💲€]?\s*([0-9]+(?:[\.,][0-9]{1,2})?)\s*([\$💲€]|usd|eur|euro|euros|دولار|دج|د\.ج|da|dzd)?',
            re.IGNORECASE
        ),
        # Post-coupon / Post-code: 'القطعة بعد الكوبون : 4.19$' or 'السعر بعد الكود : 12.50$' or 'السعر بعد التخفيض : 1.28$'
        re.compile(
            r'(?:القطعة\s*بعد\s*(?:الكوبون|الكود|التخفيض|الخصم)|السعر\s*بعد\s*(?:الكوبون|الكود|التخفيض|الخصم)|سعر\s*بعد\s*(?:الكوبون|الكود|التخفيض|الخصم)|بعد\s*(?:الكوبون|الكود|التخفيض|الخصم)|القطعة\s*بـ?كود|السعر\s*بـ?كود)'
            r'[\s:：\-–=ـ•*~|]*[\$💲€]?\s*([0-9]+(?:[\.,][0-9]{1,2})?)\s*([\$💲€]|usd|eur|euro|euros|دولار|دج|د\.ج|da|dzd)?',
            re.IGNORECASE
        ),
        # Final / Price drop / Dropped to / Now: 'والآن 0.60$' or 'الآن 0.60$' or 'طاح لـ 0.60$' or 'وصل لـ 0.60$' or 'غير بـ 0.60$' or 'فقط بـ 0.60$' or 'أصبح بسعر 0.60$'
        re.compile(
            r'(?:السعر\s*النهائي|السعر\s*الصافي|السعر\s*الإجمالي|السعر\s*الاجمالي|السعر\s*الجديد|السعر\s*الحالي|(?:و\s*)?(?:الآن|الان|حاليا|حالياً)(?:\s*بسعر|\s*بـ?|\s*صار|\s*أصبح|\s*اصبح)?|(?:و\s*)?(?:أصبح|أصبحت|اصبح|اصبحت|صار|صارت)(?:\s*بسعر|\s*بـ?)?|طاح\s*لـ?|وصل\s*لـ?|هبط\s*لـ?|غير\s*بـ?|فقط\s*بـ?|يوصل\s*لـ?)'
            r'[\s:：\-–=ـ•*~|]*[\$💲€]?\s*([0-9]+(?:[\.,][0-9]{1,2})?)\s*([\$💲€]|usd|eur|euro|euros|دولار|دج|د\.ج|da|dzd)?',
            re.IGNORECASE
        ),
        # French final / discount prices: 'Prix final : 15.50€' or 'Prix après réduction : 15.50€' or 'À seulement 15.50€'
        re.compile(
            r'(?:prix\s*final|prix\s*apr[èe]s\s*(?:r[ée]duction|code|coupon)|prix\s*avec\s*code|prix\s*r[ée]duit|[àa]\s*seulement|seulement)'
            r'[\s:：\-–=ـ•*~|]*[\$💲€]?\s*([0-9]+(?:[\.,][0-9]{1,2})?)\s*([\$💲€]|usd|eur|euro|euros|دج|da|dzd)?',
            re.IGNORECASE
        ),
    ]

    for p in discounted_price_patterns:
        m = p.search(text)
        if m:
            u, e = _parse_candidate_price(m.group(1), m.group(0))
            if u is not None:
                return u, e

    # Priority 2: Standard Explicit Price Mentions (ignoring original/old price keywords)
    explicit_price_patterns = [
        # Per piece / unit: 'سعر القطعة : 4.4$' or 'سعر الحبة : 3.5$' or 'القطعة بـ 0.60$' or 'الحبة بـ 0.60$'
        re.compile(
            r'(?:سعر\s*القطعة|سعر\s*قطعة|سعر\s*الحبة|سعر\s*حبة|القطعة\s*بـ?|الحبة\s*بـ?)'
            r'[\s:：\-–=ـ•*~|]*[\$💲€]?\s*([0-9]+(?:[\.,][0-9]{1,2})?)\s*([\$💲€]|usd|eur|euro|euros|دولار|دج|د\.ج|da|dzd)?',
            re.IGNORECASE
        ),
        # Multi-pack price: 'سعر 3 قطع: 28.85$' or 'سعر ثلاث قطع 13.2$' or 'سعر 3 حبات: 24$'
        re.compile(
            r'(?<!\S)(?:سعر|prix\s*(?:de)?)\s*(?:[0-9]+|ثلاث|أربع|اربع|خمس|ست|سبع|ثمان|تسع|عشر|قطعتين|حبتين)\s+(?:قطع|حبات|منتجات|حبة|قطعة)'
            r'[\s:：\-–=ـ•*~|]*[\$💲€]?\s*([0-9]+(?:[\.,][0-9]{1,2})?)\s*([\$💲€]|usd|eur|euro|euros|دولار|دج|د\.ج|da|dzd)?',
            re.IGNORECASE
        ),
        # Standard 'السعر : 0.60$' or 'سعر: 0.60$' or 'Prix : 15€' or 'Price: 15$' or 'بسعر 0.60$'
        re.compile(
            r'(?<!كان\s)(?<!كان\sب)(?<!كان\sبـ)(?<!كانت\s)(?<!كانت\sب)(?<!كانت\sبـ)(?<!بدل\s)(?<!بدل\sب)(?<!بدل\sبـ)(?<!عوض\s)(?<!من\s)'
            r'(?:ا+لسعر|ا+لسعــــر|\bسعر|\bprix|\bprice|\bبسعر)'
            r'(?!\s*(?:القديم|السابق|قبل|الأصلي|الاصلي|العادي|بدون))'
            r'[\s:：\-–=ـ•*~|]*[\$💲€]?\s*([0-9]+(?:[\.,][0-9]{1,2})?)\s*([\$💲€]|usd|eur|euro|euros|دولار|دج|د\.ج|da|dzd)?',
            re.IGNORECASE
        ),
        # 'بـ 0.60$' or 'ب 0.60$' when at start of line or following whitespace/emoji (not after كان/كانت/بدل/عوض)
        re.compile(
            r'(?:^|[\s\r\n🔥💥⚡💰💵])'
            r'(?<!كان\s)(?<!كانت\s)(?<!بدل\s)(?<!عوض\s)'
            r'بـ?\s*[\$💲€]?\s*([0-9]+(?:[\.,][0-9]{1,2})?)\s*([\$💲€]|usd|eur|euro|euros|دولار|دج|د\.ج|da|dzd)',
            re.IGNORECASE
        ),
    ]

    for p in explicit_price_patterns:
        m = p.search(text)
        if m:
            u, e = _parse_candidate_price(m.group(1), m.group(0))
            if u is not None:
                return u, e

    # Priority 3: Line-by-line filtering of obvious tiers/codes, followed by currency pattern match
    filtered_lines = []
    for line in text.splitlines():
        lc = line.strip().lower()
        if not lc:
            continue
        # Skip pure old price lines
        if any(w in lc for w in ["السعر القديم", "السعر السابق", "سعر سابق", "سعر قديم", "كان بسعر", "بدل من", "بدل ", "السعر الأصلي", "السعر الاصلي", "prix d'origine", "ancien prix"]):
            continue
        # Skip coupon tier lines like 'كوبون 2/15$ : OTPRD02' or 'code 5/30$' unless the line also has an explicit price indicator
        if re.search(r'\d+\s*/\s*\d+', lc) and not any(p in lc for p in ["السعر", "سعر", "القطعة", "الحبة", "prix", "price"]):
            continue
        # Skip store discount promo tier lines like 'تخفيض 1$ على 6 منتجات'
        if re.search(r'^\s*(?:تخفيض|خصم|وفر|توفير)\s*[\$💲€]?[0-9]+(?:\.[0-9]+)?[\$💲€]?\s*(?:على|لكل|pour|sur)', lc):
            continue
        filtered_lines.append(line)

    clean_text = "\n".join(filtered_lines)

    # Search for explicit currency tagged prices in cleaned text
    currency_patterns = [
        re.compile(r'([0-9]+(?:[\.,][0-9]{1,2})?)\s*(?:دج|د\.ج|da|dzd)\b', re.IGNORECASE),
        re.compile(r'([0-9]+(?:[\.,][0-9]{1,2})?)\s*€', re.IGNORECASE),
        re.compile(r'€\s*([0-9]+(?:[\.,][0-9]{1,2})?)', re.IGNORECASE),
        re.compile(r'([0-9]+(?:[\.,][0-9]{1,2})?)\s*(?:EUR|euro|euros)\b', re.IGNORECASE),
        re.compile(r'[\$💲]\s*([0-9]+(?:[\.,][0-9]{1,2})?)', re.IGNORECASE),
        re.compile(r'([0-9]+(?:[\.,][0-9]{1,2})?)\s*[\$💲]', re.IGNORECASE),
        re.compile(r'([0-9]+(?:[\.,][0-9]{1,2})?)\s*(?:USD|دولار)\b', re.IGNORECASE),
        re.compile(r'(?:USD|دولار)\s*([0-9]+(?:[\.,][0-9]{1,2})?)', re.IGNORECASE),
    ]

    for pattern in currency_patterns:
        m = pattern.search(clean_text)
        if m:
            u, e = _parse_candidate_price(m.group(1), m.group(0))
            if u is not None:
                return u, e

    # Priority 4: Fallback for lone decimal price entered by user (e.g. "https://... 0.60" or "0.60")
    lone_m = re.search(r'(?:^|[\s\r\n])([0-9]{1,4}[\.,][0-9]{1,2})(?:[\s\r\n]|$)', clean_text)
    if lone_m:
        u, e = _parse_candidate_price(lone_m.group(1), lone_m.group(0))
        if u is not None:
            return u, e

    return None, None


def is_competitor_branded_code(code: str) -> bool:
    """Checks if a coupon code contains a competitor channel's brand/name (e.g. ANIS, BND, ZED, LODY, ECKS)."""
    if not code:
        return False
    cl = code.lower().strip()
    for brand in ["anis", "bnd", "zed", "lody", "ecks", "megaprix", "megaphonna", "pcgaming", "cp4dz", "francecp", "alifrdrop", "anishays", "couponsglobal"]:
        if cl.startswith(brand) or f"_{brand}" in cl or f"-{brand}" in cl:
            return True
        if brand in ["anis", "megaprix", "megaphonna", "ecks", "pcgaming"] and brand in cl:
            return True
    return False


BLACKLIST_COUPONS = {
    "http", "https", "aliexpress", "item", "items", "link", "url", "temu", "html", "bot", "bots",
    "coin", "coins", "scoins", "scoins_bot", "coinbot", "couponsbot",
    "t.me", "dzgamingcoinbot", "channel", "click", "s.click",
    "dzaliexpress0", "francedealsdz", "france", "canada", "algerie", "livraison",
    "promo", "promos", "reduction", "reductions", "remise", "code", "codes", "coupon", "coupons",
    "seller", "store", "vendeur", "boutique", "magasin", "shop", "online",
    "choice", "plus", "super", "deal", "deals", "price", "prix", "order",
    "camera", "battery", "android", "snapdragon", "display", "screen",
    "global", "version", "edition", "original", "usbc", "typec",
    "realme", "vivo", "iqoo", "redmi", "xiaomi", "poco", "samsung", "infinix",
    "oppo", "honor", "huawei", "apple", "iphone", "ipad", "oneplus", "lenovo",
    "motorola", "blackview", "cubot", "oukitel", "doogee", "tecno", "itel", "nubia", "zte",
    "note", "pad", "tab", "watch", "band", "buds", "air", "phone", "z11s", "c71",
    "ram", "rom", "used", "new", "pro", "max", "lite", "mini", "neo", "ultra",
    "8gb", "16gb", "32gb", "64gb", "128gb", "256gb", "512gb", "1tb", "2tb", "4gb", "6gb", "2gb",
    "com", "net", "org", "co", "io", "app", "xyz", "tech", "site", "live", "info", "link", "dev", "ai",
    "haylou", "faro", "smart", "voice", "calling", "health", "screen",
    "zeblaze", "colmi", "amazfit", "qcy", "soundpeats", "edifier",
    "mchose", "machenike", "ajazz", "aula", "epomaker", "keychron", "dareu",
    "redragon", "gamesir", "flydigi", "gulikit", "8bitdo", "macbook", "airpods",
    "galaxy", "pixel", "blackshark", "moondrop", "tangzu", "chu", "fantech", "attack",
    "shark", "bmax", "teclast", "alldocube", "chuwi", "kfa2", "colorful",
    "gainward", "soyo", "maxsun", "huananzhi", "jisu", "jisulife", "anker",
    "baseus", "ugreen", "essager", "toocki", "kuulaa", "orico", "blitzwolf",
    "tronsmart", "zealot", "wireless", "bluetooth", "earphone", "earphones",
    "headphone", "headphones", "headset", "speaker", "mouse", "keyboard",
    "controller", "gamepad", "cable", "charger", "powerbank", "adapter"
}


def clean_coupon_token(raw: str, title: Optional[str] = None) -> Optional[str]:
    """Validates and cleans a potential coupon token string."""
    if not raw:
        return None
    raw_str = raw.strip()

    # Reject URL slug hashes and tokens starting or ending with underscores or hyphens (e.g. _c3lJDYXB)
    if raw_str.startswith(('_', '-')) or raw_str.endswith(('_', '-')):
        return None

    c = re.sub(r'^[<>/`*#()\[\]{}:;,\.=\-+ـ_]+|[<>/`*#()\[\]{}:;,\.=\-+ـ_]+$', '', raw_str).strip()
    c = c.replace("<code>", "").replace("</code>", "")
    c = c.upper()

    if len(c) < 3 or len(c) > 25:
        return None
    if c.startswith(('_', '-')) or c.endswith(('_', '-')):
        return None
    if not re.search(r'[A-Za-z]', c):
        return None
    c_lower = c.lower()

    # Reject bots, coin bots, Telegram handles and channels (e.g. SCOINS_BOT, Coins_bot, etc.)
    if any(k in c_lower for k in ["bot", "coin", "tele", "gram", "channel", "group", "chat", "admin", "join"]):
        return None
    if "@" in raw_str or "/" in raw_str or "\\" in raw_str or ":" in raw_str:
        return None

    # Reject web domains, TLDs, and URL fragments
    if c_lower in {
        "com", "net", "org", "co", "io", "app", "xyz", "online", "store", "shop",
        "tech", "site", "live", "info", "link", "pro", "me", "club", "vip", "dev",
        "ai", "gov", "edu", "url", "uri", "http", "https", "www", "html", "php", "aspx", "api"
    }:
        return None

    if c_lower in BLACKLIST_COUPONS:
        return None
    if re.search(r'^\d+(?:gb|tb|mb|g|ram|rom|t)$', c_lower):
        return None
    if any(b in c_lower for b in ["http", "t.me", "click", "item/", ".com", ".net", "aliexpress"]):
        return None
    if c_lower.startswith("item"):
        return None
    if is_competitor_branded_code(c):
        return None

    # Title check: A coupon code can NEVER simply be an English word from the product title
    if title:
        title_words = {w.lower().strip() for w in re.findall(r'[A-Za-z0-9_-]+', title) if len(w) >= 3}
        if c_lower in title_words:
            return None

    return c


def extract_multi_coupons(raw_text: str, title: Optional[str] = None) -> Dict[str, Any]:
    """
    Comprehensive multi-coupon and description extractor for Telegram deal posts.
    Extracts ALL promo codes, spend/discount tiers, and labels from various formats:
      - 'كوبون: CODE1', 'كوبون آخر: CODE2', 'كود المتجر: CODE3'
      - '🎟️ 6/49$ : WOAE06', '🎟️ 12/89$ : WOAE12'
      - 'كود: CODE1 / CODE2'
      - 'Code promo: CODE1'
      - 'قسيمة: CODE1'
    Filters out blacklist noise and competitor-branded codes.
    Returns:
      {
        "coupons": List[str],             # All unique valid coupon codes
        "coupon_details": List[Dict],      # [{"code": str, "tier": str, "label": str}]
        "coupon_code": Optional[str],     # First code (for backward compatibility)
        "description": str                # Cleaned description stripping URLs, bots, affiliate links
      }
    """
    if not raw_text:
        return {
            "coupons": [],
            "coupon_details": [],
            "coupon_code": None,
            "description": ""
        }

    norm = re.sub(r'[\u0640]', '', raw_text)

    coupons: List[str] = []
    coupon_details: List[Dict[str, str]] = []
    seen_codes = set()

    def add_coupon(code_str: str, label: str = "كوبون", tier: str = ""):
        c = clean_coupon_token(code_str, title=title)
        if not c:
            return
        clean_tier = ""
        if tier:
            t = re.sub(r'\s+', '', tier.strip())
            if not t.startswith('$') and not t.endswith('$') and not t.startswith('€') and not t.endswith('€'):
                t = f"{t}$"
            clean_tier = t

        clean_label = label.strip() if label else "كوبون"
        clean_label = re.sub(r'^[🏷️🎟️🎫•\-\*:\s]+|[🏷️🎟️🎫•\-\*:\s]+$', '', clean_label).strip()
        if not clean_label:
            clean_label = "كوبون"

        if c not in seen_codes:
            seen_codes.add(c)
            coupons.append(c)
            coupon_details.append({
                "code": c,
                "tier": clean_tier,
                "label": clean_label
            })
        else:
            # Upgrade existing entry if current match has a richer tier or more specific label
            for d in coupon_details:
                if d["code"] == c:
                    if not d.get("tier") and clean_tier:
                        d["tier"] = clean_tier
                    if (not d.get("label") or d.get("label") == "كوبون") and clean_label and clean_label != "كوبون":
                        d["label"] = clean_label
                    break

    # 1. Tier-First Pattern: '🎟️ 6/49$ : WOAE06' or 'كوبون 4/35$ : BDQT04' or 'خصم 2/15$ بكود OTPRD02'
    p1 = re.compile(
        r'(?P<prefix>🎟️?|🎫|•|\-|\*)?[^\S\r\n]*(?P<label>(?:ال)?كوبون(?:\s*آخر|\s*إضافي)?|(?:ال)?كود(?:\s*آخر|\s*إضافي)?|code\s*promo|(?:ال)?قسيمة|خصم|تخفيض)?[^\S\r\n]*'
        r'(?P<tier>[$€]?[0-9]+(?:\.[0-9]+)?[^\S\r\n]*/[^\S\r\n]*[$€]?[0-9]+(?:\.[0-9]+)?[$€]?)[^\S\r\n]*'
        r'(?:بكود|code|:|=|：|\-)?[^\S\r\n]*\r?\n?[^\S\r\n]*(?P<code>[A-Za-z0-9_-]{3,25})',
        re.IGNORECASE
    )
    for m in p1.finditer(norm):
        lbl = m.group('label')
        pfx = m.group('prefix')
        tier_val = m.group('tier') or ""
        # Guard: If no coupon label or prefix, tier MUST contain currency symbol to avoid specs like 3/64
        if not lbl and not pfx and not re.search(r'[$€]', tier_val):
            continue
        add_coupon(m.group('code'), label=lbl or "كوبون", tier=tier_val)

    # 2. Code-First Pattern: 'OTPRD02 : 2/15$' or 'كود OTPRD02 (2/15$)'
    p2 = re.compile(
        r'(?P<prefix>🎟️?|🎫|•|\-|\*)?[^\S\r\n]*(?P<label>(?:ال)?كوبون(?:\s*آخر|\s*إضافي)?|(?:ال)?كود(?:\s*آخر|\s*إضافي)?|code\s*promo|(?:ال)?قسيمة)?[^\S\r\n]*'
        r'(?P<code>[A-Za-z][A-Za-z0-9_-]{2,24})[^\S\r\n]*'
        r'(?:[:=：\-]|خصم|بخصم|\()?[^\S\r\n]*\r?\n?[^\S\r\n]*'
        r'(?P<tier>[$€]?[0-9]+(?:\.[0-9]+)?[^\S\r\n]*/[^\S\r\n]*[$€]?[0-9]+(?:\.[0-9]+)?[$€]?)\)?',
        re.IGNORECASE
    )
    for m in p2.finditer(norm):
        lbl = m.group('label')
        pfx = m.group('prefix')
        tier_val = m.group('tier') or ""
        # Guard: Require either label or prefix, AND tier must have currency symbol (avoids phone specs like Note 12 4/128, C71 3/64)
        if not lbl and not pfx:
            continue
        if not re.search(r'[$€]', tier_val):
            continue
        add_coupon(m.group('code'), label=lbl or "كوبون", tier=tier_val)

    # 3. Labeled Lines & Slashed / Multi-Code Lines:
    # 'كوبون: CODE1', 'كوبون آخر: CODE2', 'كود المتجر: CODE3', 'كود: CODE1 / CODE2'
    # 'Code promo: CODE1', 'قسيمة: CODE1', 'قسيمة المتجر: CODE1'
    p_line_label = re.compile(
        r'^[^\S\r\n]*(?P<label>'
        r'(?:[^\w\s\r\n]+\s*)?'
        r'(?:'
        r'(?:استخدم\s+|استعمل\s+|انسخ\s+|بكود\s+)?(?:ال)?كوبون\s*(?:آخر|اخر|إضافي|اضافي|خاص|البائع|المتجر|الخصم|التخفيض)?|'
        r'(?:استخدم\s+|استعمل\s+|انسخ\s+|بكود\s+)?(?:ال)?كود\s*(?:آخر|اخر|إضافي|اضافي|خاص|البائع|المتجر|الخصم|التخفيض|الشراء)?|'
        r'(?:ال)?قسيمة\s*(?:أخرى|اخرى|إضافية|اضافية|خاصة|البائع|المتجر|الخصم|التخفيض)?|'
        r'(?:ال)?قسيمـ?ة|'
        r'\bcode(?:\s*promo)?(?:\s*[-–]?\s*[$€]?[0-9]+(?:[\.,][0-9]+)?[$€]?)?|code\s*de\s*r[ée]duction|code\s*r[ée]duction|bon\s*de\s*r[ée]duction|'
        r'coupon\s*vendeur|store\s*coupon|seller\s*coupon|utilisez\s*(?:le\s*)?code|avec\s*(?:le\s*)?code|'
        r'promo\s*code|\bcoupon\b'
        r')'
        r'|'
        r'(?:🏷️|🎟️|🎫|👊)'
        r')'
        r'[\s:：\-=ـ_•*~|()✅🔥👉✔️⏺🙏💵💰🎁📌⚡💥🤐]*'
        r'(?P<content>[^\r\n]*)',
        re.IGNORECASE | re.MULTILINE
    )
    for m in p_line_label.finditer(norm):
        lbl = m.group('label') or "كوبون"
        content = m.group('content').strip()

        # Stop content at boundary markers (URLs, links, product markers, prices, section emojis)
        boundary_m = re.search(
            r'https?://|t\.me/|@[A-Za-z0-9_]+|'
            r'[\U0001f300-\U0001f9ff\u2600-\u26ff\u2700-\u27bf]|'
            r'(?:^|\s)(?:رابط|السعر|سعر|للشراء|لشراء|بوت|قناة|قناتنا)\b',
            content
        )
        if boundary_m:
            content = content[:boundary_m.start()].strip()

        # Check if content has an embedded spend tier e.g. "WOAE06 (6/49$)"
        tier_m = re.search(r'\(?([$€]?[0-9]+(?:\.[0-9]+)?/[0-9]+(?:\.[0-9]+)?[$€]?)\)?', content)
        line_tier = tier_m.group(1) if tier_m else ""
        if line_tier:
            content = content.replace(tier_m.group(0), "")

        # Split content on separators: '/', '|', '،', ',', ' أو ', ' ou ', ' or '
        parts = re.split(r'[\/\|,،]|\s+(?:أو|or|ou)\s+', content)
        found_tokens = 0
        for part in parts:
            cand = part.strip()
            tokens = re.findall(r'[A-Za-z0-9_-]{3,25}', cand)
            for tok in tokens:
                add_coupon(tok, label=lbl, tier=line_tier)
                found_tokens += 1

        # Fallback to next line if current line only had tier or punctuation (e.g. "كوبون 12€ :\nFRPRD12")
        if found_tokens == 0:
            pos = m.end()
            next_m = re.match(r'\r?\n[^\S\r\n]*(?:[⏺•\-*✔️✅👉]\s*)?([A-Za-z0-9_-]{3,25})', norm[pos:])
            if next_m:
                add_coupon(next_m.group(1), label=lbl, tier=line_tier or content)

    # 4. Fallback search for HTML <code> tags or backtick codes near coupon keywords
    p_tags = re.compile(
        r'(?:(?:ال)?كود|(?:ال)?كوبون|(?:ال)?قسيمة|code|coupon|promo)[^\r\n]{0,60}?(?:<code>|`|\*\*)([A-Za-z0-9_-]{3,25})(?:</code>|`|\*\*)',
        re.IGNORECASE
    )
    for m in p_tags.finditer(norm):
        add_coupon(m.group(1), label="كود الخصم")

    # 5. Clean Description Extraction (strips URLs, bot tags, affiliate links, and spam footers)
    strip_keywords = [
        'http://', 'https://', 't.me/', 's.click.aliexpress', 'aliexpress.com',
        'رابط الشراء', 'رابط العرض', 'رابط المنتج', 'رابط الطلب', 'رابط الكوبون', 'رابط التخفيض',
        'للشراء من هنا', 'للطلب من هنا', 'للشراء', 'للطلب', 'lien d\'achat', 'lien du produit', 'acheter ici',
        'بوت تخفيض', 'بوت العملات', 'بوت النقاط', 'بوت التخفيض', 'استخدم البوت', 'عبر البوت',
        'قناتنا', 'قناة التلغرام', 'اشترك في', 'تابعنا على', 'تابعونا', 'انضم الى', 'انضم إلى',
        'rejoignez', 'notre canal', 'notre chaîne',
        'خلي البلد', 'خلي بلد', 'بلد الحساب', 'ديرو بلاد', 'ديرو الجزائر', 'livraison france',
        'السعر بعد', 'سعر بعد', 'السعر :', 'السعر:', 'prix :', 'prix:', 'price :'
    ]

    cleaned_lines = []
    lines = [l.strip() for l in norm.splitlines() if l.strip()]
    for line in lines:
        line_lower = line.lower()

        # Check if line contains links, bots, or promo noise
        if any(kw in line_lower for kw in strip_keywords):
            continue
        if re.search(r'https?://|t\.me/|@[a-zA-Z0-9_]+', line):
            continue

        # Check if line is a pure coupon code line (already extracted)
        if re.match(r'^(?:🎟️|🎫|•|\-|\*)?\s*(?:(?:ال)?كوبون|(?:ال)?كود|code\s*promo|(?:ال)?قسيمة|code|coupon)\b', line, re.IGNORECASE):
            continue
        if re.match(r'^(?:🎟️|🎫)\s*[$€]?[0-9]+', line):
            continue

        # Clean inline residual tags if any
        clean_l = re.sub(r'https?://\S+', '', line)
        clean_l = re.sub(r'@[a-zA-Z0-9_]+', '', clean_l).strip()
        clean_l = re.sub(r'</?[a-zA-Z0-9_-]+>', '', clean_l).strip()

        if clean_l and len(clean_l) > 1:
            cleaned_lines.append(clean_l)

    description = '\n'.join(cleaned_lines).strip()
    primary_code = coupons[0] if coupons else None

    return {
        "coupons": coupons,
        "coupon_details": coupon_details,
        "coupon_code": primary_code,
        "description": description
    }


# Backward-compatible alias
extract_deal_coupons_and_description = extract_multi_coupons


def extract_coupon(text: str, title: Optional[str] = None) -> Optional[str]:
    """Extracts the primary/first coupon code for backward compatibility."""
    if not text:
        return None
    res = extract_multi_coupons(text, title=title)
    return res.get("coupon_code")


def extract_seller_coupon(text: str) -> Optional[str]:
    if not text:
        return None
    norm = re.sub(r'[\u0640]', '', text)
    blacklist = {"http", "https", "aliexpress", "link", "url", "temu", "t.me", "bot"}

    # 1. Combined amount and code: e.g. "احجز كوبون المتجر 8$ KR0864" or "حصل قسيمة البائع $80: T0F4TZ"
    p_combined = re.search(
        r'(?:حصل\s*|احجز\s*)?(?:قسيمة|كوبون|كود)\s*(?:البائع|المتجر|خاصة\s*بالمتجر|store\s*coupon|seller\s*coupon)'
        r'[\s:：\-=ـ_•*~|()✅🔥👉✔️🌷🙏\+💵💰🎁\r\n]*'
        r'[$]?\s*([0-9]+(?:\.[0-9]+)?)\s*[$]?'
        r'[\s:：\-=ـ_•*~|()✅🔥👉✔️🌷🙏\+💵💰🎁\r\n]+'
        r'([A-Za-z0-9_\-\s/]{3,35})',
        norm,
        re.IGNORECASE
    )
    if p_combined:
        amount = p_combined.group(1).strip()
        code = p_combined.group(2).strip().split('\n')[0].strip()
        code = re.sub(r'[🎟️🎫👊🔗📌💵💰].*$', '', code).strip()
        code = re.sub(r'[\u0600-\u06FF].*$', '', code).strip()
        try:
            if amount and float(amount) < 1.0:
                amount = ""
        except ValueError:
            pass
        if code and code.lower() not in blacklist and re.search(r'[A-Za-z0-9]', code):
            if not is_competitor_branded_code(code):
                return f"{amount}$ (كود: {code})" if amount else code

    # 2. Code only: e.g. "🎁💰احجز كوبون المتجر 💵:\nKR0864"
    p_code = re.search(
        r'(?:حصل\s*|احجز\s*)?(?:قسيمة|كوبون|كود)\s*(?:البائع|المتجر|خاصة\s*بالمتجر|store\s*coupon|seller\s*coupon)'
        r'[\s:：\-=ـ_•*~|()✅🔥👉✔️🌷🙏\+💵💰🎁\r\n]+'
        r'([A-Za-z][A-Za-z0-9_-]{3,24})',
        norm,
        re.IGNORECASE
    )
    if p_code:
        code = p_code.group(1).strip()
        if code.lower() not in blacklist and not code.lower().endswith(('$', 'usd', 'eur')):
            if not is_competitor_branded_code(code):
                return code

    # 3. Standard SELLER_COUPON_PATTERNS (amount or code)
    for pattern in SELLER_COUPON_PATTERNS:
        m = pattern.search(norm)
        if m:
            code = m.group(1).strip()
            # If purely numerical or dollar amount, ensure it is at least $1.00
            num_clean = re.sub(r'[^\d\.]', '', code)
            try:
                if num_clean and float(num_clean) < 1.0:
                    continue  # Ignore trivial sub-dollar coupons like 0.9$
                if num_clean and not code.endswith('$'):
                    code = f"{num_clean}$"
            except ValueError:
                pass
            if not is_competitor_branded_code(code):
                return code
    return None


def is_affiliate_exclusive_deal(text: str, title: Optional[str] = None) -> Tuple[bool, Optional[str]]:
    """
    Detects if a competitor Telegram post is an affiliate-exclusive deal.
    Such deals rely on channel-exclusive promo codes, exclusive partner coupons,
    or exclusive creator discounts (e.g. 'خاص بمتابعين القناة', 'كوبون حصري',
    or competitor-branded coupons like ZEDHAYHCS04, LODY10, ANIS05).

    These must NEVER be posted because:
    1. The discounted price is only valid with that specific channel's affiliate link/code.
    2. Followers of our channel cannot use the coupon with our affiliate link.
    3. Without the exclusive coupon, the advertised price is inaccurate/misleading.
    """
    if not text:
        return False, None

    norm = re.sub(r'[\u0640]', '', text)
    lower_text = norm.lower()

    # 1. Explicit channel-exclusive affiliate keywords
    AFFILIATE_EXCLUSIVE_KEYWORDS = [
        "خاص بمتابعين",
        "خاص بالمتابعين",
        "خاص بمتابعينا",
        "خاص بالقناة",
        "خاص بمشتركي",
        "خاص بالمشتركين",
        "كوبون حصري",
        "كود حصري",
        "قسيمة حصرية",
        "حصري لمتابعينا",
        "حصري للقناة",
        "حصريا لمتابعينا",
        "حصرياً لمتابعينا",
        "حصريا للقناة",
        "حصرياً للقناة",
        "exclusive to our followers",
        "exclusive code",
        "exclusive coupon"
    ]

    for kw in AFFILIATE_EXCLUSIVE_KEYWORDS:
        if kw in lower_text:
            return True, f"Affiliate-exclusive deal detected (phrase: '{kw}')"

    # 2. Check if post has coupon mentions where ALL codes are competitor-branded
    coupon_indicators = ["كوبون", "كود", "code", "قسيمة", "promo", "🎟️", "🎫"]
    has_coupon_mention = any(ind in lower_text for ind in coupon_indicators)

    if has_coupon_mention:
        # Find all alphanumeric tokens in the message that could be competitor codes
        tokens = re.findall(r'[A-Za-z0-9_-]{4,25}', norm)
        competitor_codes = [t for t in tokens if is_competitor_branded_code(t)]

        if competitor_codes:
            # Check if there are any valid non-competitor coupons extracted
            multi = extract_multi_coupons(text, title=title)
            valid_coupons = multi.get("coupons", [])
            if not valid_coupons:
                return True, f"Deal relies exclusively on competitor affiliate coupon(s): {competitor_codes}"

    return False, None


def detect_points_discount(text: str) -> bool:
    if not text:
        return False
    for pattern in POINTS_PATTERNS:
        if pattern.search(text):
            return True
    return False

def extract_country_instruction(text: str, url: str = "", title: str = "") -> Optional[str]:
    """
    Intelligently detects which country setting is needed for maximum discount.
    1. Reads explicit mentions or flags in text or url (Saudi Arabia 🇸🇦, UAE 🇦🇪, Canada 🇨🇦, Korea 🇰🇷, Algeria 🇩🇿, France 🇫🇷, Spain 🇪🇸, Australia 🇦🇺, Ukraine 🇺🇦, etc.).
    2. Returns None if no country change instruction is present (do NOT auto-default to Canada).
    """
    raw_combined = f"{text or ''} {url or ''} {title or ''}"
    norm_text = re.sub(r'[\u0640]', '', raw_combined)
    combined = norm_text.lower()

    # Extract isolated regional indicator flag pairs to prevent overlapping substring matches
    # (e.g. 🇦🇺🇦🇺 Australia flag repeated contains 🇺🇦 Ukraine as a substring if matched naively!)
    flag_pairs = set(re.findall(r'[\U0001F1E6-\U0001F1FF]{2}', raw_combined))

    # 0. Saudi Arabia detection (must be checked BEFORE fallback)
    if "🇸🇦" in flag_pairs or any(k in combined for k in ["السعودية", "سعودية", "saudi", "ksa", "shiptocountry=sa", "country=sa"]) or re.search(r'\bsar\b', combined):
        return "السعودية 🇸🇦"

    # 0.5 UAE & Gulf countries
    if "🇦🇪" in flag_pairs or any(k in combined for k in ["الإمارات", "الامارات", "امارات", "إمارات", "uae", "emirates", "shiptocountry=ae", "country=ae"]) or re.search(r'\baed\b', combined):
        return "الإمارات 🇦🇪"
    if "🇶🇦" in flag_pairs or any(k in combined for k in ["قطر", "qatar", "shiptocountry=qa", "country=qa"]) or re.search(r'\bqar\b', combined):
        return "قطر 🇶🇦"
    if "🇰🇼" in flag_pairs or any(k in combined for k in ["الكويت", "كويت", "kuwait", "shiptocountry=kw", "country=kw"]) or re.search(r'\bkwd\b', combined):
        return "الكويت 🇰🇼"
    if "🇧🇭" in flag_pairs or any(k in combined for k in ["البحرين", "بحرين", "bahrain", "shiptocountry=bh", "country=bh"]) or re.search(r'\bbhd\b', combined):
        return "البحرين 🇧🇭"
    if "🇴🇲" in flag_pairs or any(k in combined for k in ["عمان", "عُمان", "oman", "shiptocountry=om", "country=om"]) or re.search(r'\bomr\b', combined):
        return "عمان 🇴🇲"

    # 1. Canada detection (only when explicitly mentioned in text or url)
    if "🇨🇦" in flag_pairs or any(k in combined for k in ["كندا", "canada", "cad", "shiptocountry=ca", "country=ca"]):
        return "كندا 🇨🇦"

    # 2. Korea detection (only when explicitly specified in source post or URL)
    if "🇰🇷" in flag_pairs or any(k in combined for k in ["كوريا", "korea", "krw", "shiptocountry=kr", "country=kr"]):
        return "كوريا 🇰🇷"

    # 3. Algeria detection (rare cases: local shipping / DZ coin promo)
    if "🇩🇿" in flag_pairs or any(k in combined for k in ["الجزائر", "algeria", "shiptocountry=dz", "country=dz", "ديرو الجزائر", "بلاد الجزائر", "حساب جزائري"]):
        return "الجزائر 🇩🇿"

    # 4. France detection
    if "🇫🇷" in flag_pairs or any(k in combined for k in [
        "فرنسا", "france", "shiptocountry=fr", "country=fr",
        "european", "version européenne", "version europeenne", "livraison france",
        "francecp", "alifrdrop"
    ]) or re.search(r'\bfr(?:prd|ld|cd)?[0-9]{1,4}\b', combined):
        return "فرنسا 🇫🇷"

    # 5. Spain detection
    if "🇪🇸" in flag_pairs or any(k in combined for k in ["إسبانيا", "اسبانيا", "spain", "espana", "españa", "shiptocountry=es"]):
        return "إسبانيا 🇪🇸"

    # 5.5 Australia detection
    if "🇦🇺" in flag_pairs or any(k in combined for k in ["استراليا", "أستراليا", "australia", "shiptocountry=au"]) or re.search(r'\baud\b', combined):
        return "أستراليا 🇦🇺"

    # 5.6 Ukraine detection (frequent for low smartphone prices)
    if "🇺🇦" in flag_pairs or any(k in combined for k in ["أوكرانيا", "اوكرانيا", "ukraine", "shiptocountry=ua"]) or re.search(r'\buah\b', combined):
        return "أوكرانيا 🇺🇦"

    # 5.7 United Kingdom detection
    if "🇬🇧" in flag_pairs or any(k in combined for k in ["بريطانيا", "المملكة المتحدة", "united kingdom", "uk", "shiptocountry=gb", "shiptocountry=uk"]) or re.search(r'\bgbp\b', combined):
        return "المملكة المتحدة 🇬🇧"

    # 5.8 Brazil detection
    if "🇧🇷" in flag_pairs or any(k in combined for k in ["البرازيل", "برازيل", "brazil", "brasil", "shiptocountry=br"]) or re.search(r'\bbrl\b', combined):
        return "البرازيل 🇧🇷"

    # Explicit generic directives (e.g. "خلي البلد" or "ضع البلد" without country name)
    if any(k in combined for k in ["خلي البلد", "ضع البلد", "بلد الحساب"]):
        return "كندا 🇨🇦"

    # If no country directive was specified, return None (normal deals do not require changing country!)
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
        "جدول", "اكواد", "أكواد", "تخفيضات", "عروض الخريف", "تفعيل",
        "متوافق مع", "متوافقة مع", "يدعم أجهزة", "تدعم أجهزة",
        "أرض", "ارض", "اجري", "أجري", "تخفيض العملات", "تخفيض عملات", "خصم العملات", "رابط العملات",
        "تلقائي", "حساب كندي", "حساب سعودي", "غير البلد", "ضع البلد", "خلي البلد",
        "أضف إلى السلة", "اضف إلى السلة", "أضف في السلة", "اضف في السلة", "أضف للسلة", "اضف للسلة",
        "أضف الآن", "اضف الان", "أضف للمفضلة", "اضف للمفضلة", "دير في السلة", "ديرو في السلة",
        "عمرو السلة", "عمّروا السلة", "البيع يبدأ", "البيع يبدا", "يوم الأحد", "يوم الاحد",
        "يوم 1 نوفمبر", "نهار التخفيضات", "تسخينات", "تسخينات 11.11", "سعر أرض", "سعر ارض",
        "متوسط سعره", "سعره حالياً", "سعره حاليا", "سعرو حالياً", "سعرو حاليا", "في البلاد",
        "السوق الجزائرية", "السوق الجزائري", "عليه طلب"
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
        # Reject market pricing notes / currency mentions in titles
        if any(w in norm for w in ["متوسط سعره", "سعره", "سعرو", "في البلاد", "السوق الجزائرية", "دج", "dzd"]):
            return True

        # Reject candidate titles starting with description verbs
        if any(norm.startswith(v) for v in ["يلحقك", "تأتي", "تحتوي", "يأتي", "معاها", "طريقة", "كيفية", "شرح", "متوافق", "متوافقة", "يدعم", "تدعم", "أجهزة", "اجهزة"]):
            return True
        return False

    # 0. Look for explicit star bullet title line (ZedStore & top Algerian channels standard: ⭐️ [Title] or [Country] ⭐️ [Title])
    for i, line in enumerate(lines):
        if any(s in line for s in ["⭐️", "⭐", "🌟"]):
            parts = re.split(r'[⭐️⭐🌟]', line)
            cand = parts[-1].strip()
            if (not cand or len(cand) < 3) and i + 1 < len(lines):
                cand = lines[i + 1].strip()
                if i + 2 < len(lines) and not any(k in lines[i + 2] for k in ['$', '€', 'السعر', 'احجز', 'كوبون', 'رابط', '🔗', '💵']):
                    cand += ' ' + lines[i + 2].strip()
            cand = re.sub(r'[\$€💵].*$', '', cand).strip()
            cand = re.sub(r'https?://\S+', '', cand).strip()
            cand = re.sub(r'^[✅✔️☑️📱🎮🎧\s\-:]+', '', cand).strip()
            if not is_noisy(cand) and len(cand) >= 3:
                return cand[:100]

    # 0.5 Look for checkmark / device / channel bullet title line (DealScout DZ, Megaphonna Ⓜ, etc.)
    for i, line in enumerate(lines):
        if any(line.startswith(s) for s in ["✅", "✔️", "☑️", "📱", "🎮", "🎧", "Ⓜ️", "Ⓜ"]):
            cand = re.sub(r'^[✅✔️☑️📱🎮🎧Ⓜ️Ⓜ\s\-:]+', '', line).strip()
            if (not cand or len(cand) < 3) and i + 1 < len(lines):
                cand = lines[i + 1].strip()
            cand = re.sub(r'[\$€💵].*$', '', cand).strip()
            cand = re.sub(r'https?://\S+', '', cand).strip()
            cand = re.sub(r'</?[^>]+(>|$)', '', cand).strip()
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
        c = re.sub(r'^(?:غير\s+البلد|ضع\s+البلد|خلي\s+البلد|بلد\s+الحساب)[^\n]*[🇨🇦🇸🇦🇫🇷🇦🇺🇩🇿🇶🇦🇰🇼🇦🇪⭐️⭐🌟✅]\s*', '', line).strip()
        c = re.sub(r'^[❗️🔖📌🔥🚨⚡💥✨📦🛒🎁📢✅💎💰🔻ـ\s\-:⭐️🌷⏺📎]+', '', c).strip()
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
    Prevents French offers from ever leaking into Algerian channel @DzAliexpress0,
    and prevents non-French Arabic deals from leaking into France channel @francedealsdz.
    """
    combined = f"{text or ''} {url or ''}".lower()

    # Reject immediately if domestic Algerian indicators are present
    algerian_indicators = [
        "الجزائر", "dzd", "دينار", "بريدي موب", "بريد الجزائر", "58 ولاية",
        "yalidine", "kazi tour", "carré", "livraison algerie", "algeria", "algerie"
    ]
    if any(ind in combined for ind in algerian_indicators):
        return False

    # Auto-extract country instruction if not passed explicitly
    if country_info is None and text:
        country_info = extract_country_instruction(text)

    if country_info and any(k in str(country_info).lower() for k in ["فرنسا", "france", "🇫🇷"]):
        return True

    # Explicit Arabic drop indicators as typed by Algerian/Arabic deal hunters
    explicit_arabic_france_markers = [
        "عروض ففرنسا", "عروض فرنسا", "عرض فرنسا", "عرض ففرنسا",
        "خاص بفرنسا", "فرنسا فقط", "فقط لفرنسا",
        "شحن لفرنسا", "شحن فرنسا", "شحن الى فرنسا", "شحن إلى فرنسا", "شحن نحو فرنسا",
        "الشحن لفرنسا", "الشحن فرنسا", "الشحن الى فرنسا", "الشحن إلى فرنسا", "الشحن نحو فرنسا",
        "توصيل لفرنسا", "توصيل فرنسا", "توصيل الى فرنسا", "توصيل إلى فرنسا", "توصيل نحو فرنسا",
        "التوصيل لفرنسا", "التوصيل فرنسا", "التوصيل الى فرنسا", "التوصيل إلى فرنسا", "التوصيل نحو فرنسا",
        "نحو فرنسا", "لفرنسا", "إلى فرنسا", "الى فرنسا", "في فرنسا",
        "البلد فرنسا", "البلد : فرنسا", "بلد فرنسا",
        "كودات فرنسا", "كوبونات فرنسا", "كوبون فرنسا", "كود فرنسا", "كوبون فرنسي", "كوبونات فرنسية",
        "فرنسا 🇫🇷", "france 🇫🇷"
    ]
    if any(k in combined for k in explicit_arabic_france_markers):
        return True

    # If post mentions France and currency is Euro, it's definitely a France deal
    if any(f in combined for f in ["فرنسا", "france", "🇫🇷"]) and any(e in combined for e in ["€", "اورو", "أورو", "eur", "euro"]):
        return True

    # Native French phrasing
    native_french_markers = [
        "livraison france", "vers la france", "pour la france", "france seulement",
        "codes promo france", "livraison : france", "livraison en france",
        "livré en france", "livraison gratuite en france", "bon plan france", "prix constaté"
    ]
    if any(k in combined for k in native_french_markers):
        return True

    # French promo codes (e.g. FRPRD12, FRLD30, CDFR25, FWFR11, SUNFR30, SUNFR20, FR20)
    if re.search(r'\b(?:[A-Za-z]{0,4}FR|FR[A-Za-z]{0,4})\d{1,3}\b', combined, re.IGNORECASE):
        # Ensure it's not a false positive with standard words
        if any(euro in combined for euro in ["€", "eur", "اورو", "أورو", "france", "فرنسا"]) or re.search(r'\b(?:frprd|frld|frcd|cdfr|frfw|fwfr|sunfr)\d{1,3}\b', combined, re.IGNORECASE):
            return True

    # Explicit URL shipping parameters for France
    if "shiptocountry=fr" in combined or "country=fr" in combined:
        return True

    return False


def detect_deal_type(raw_text: str, url: str = "") -> str:
    """
    Intelligently determines whether a deal is a 'bundle', 'coin', or standard 'item' deal.
    - Bundle deals: Choice Bundle / 3 items / sourceType=562.
    - Coin deals: explicitly mentions coins/points AND is a small gadget/peripheral or sourceType=620.
    - Standard item deals: phones, tablets, CPUs/hardware, or coupon-only deals (canonical item page).
    """
    text_lower = (raw_text or "").lower()
    url_lower = (url or "").lower()

    # Check for accessories so accessories (e.g. laptop stand, phone holder, cable)
    # are never mistakenly treated as high-value whole tech devices
    accessory_keywords = [
        "holder", "stand", "case", "cover", "cable", "adapter", "charger", "screen protector", "film",
        "mouse", "keyboard", "fara", "souris", "pad", "mousepad", "headphone", "earphone", "earbuds",
        "حامل", "كفر", "جراب", "غلاف", "كابل", "شاحن", "حماية", "لاصقة", "قاعدة", "مسند", "سماعة", "سماعات"
    ]
    is_accessory = any(w in text_lower for w in accessory_keywords)

    # High-value tech (phones, tablets, CPUs, GPUs, laptops) must NEVER be classified as bundle deals
    high_value_keywords = [
        "phone", "smartphone", "هاتف", "هواتف", "redmi", "poco", "xiaomi",
        "realme", "oneplus", "oppo", "honor", "infinix", "tecno", "samsung",
        "galaxy", "iphone", "تابلت", "ipad", "tablet",
        "cpu", "ryzen", "intel core", "processor", "معالج", "gpu", "rtx",
        "gtx", "motherboard", "carte mere", "لوحة أم", "laptop", "pc portable", "حاسوب"
    ]
    is_high_value = not is_accessory and (any(w in text_lower for w in high_value_keywords) or any(w in url_lower for w in high_value_keywords))

    # Bundle deals check (high-value devices are excluded from Choice Bundle)
    if not is_high_value:
        bundle_keywords = [
            "bundle", "bundledraw", "bundledeals", "bundle deals", "bundledeals2",
            "300000512", "sourcetype=562", "channel=bundle",
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
        if re.search(r'300000512|sourcetype=562|bundledeals', url_lower):
            return "bundle"

    if is_high_value:
        return "item"

    # Super deals
    if "superdeal" in url_lower or "sourcetype=561" in url_lower or "سوبر ديل" in text_lower:
        return "super"

    # In Algerian Deal channels and DealScout DZ, all standard product deals are coin deals
    # (they route to the coin-index landing page to maximize discounts).
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
        if not ali_link_match:
            ali_link_match = re.search(r'https?://[a-zA-Z0-9_\.]*aliexpress\.com/[^\s<>"\']+', text)
        if not ali_link_match:
            # Never default to a naked unmonetized homepage link
            return False, None, None
        from api.coin_bot import ensure_affiliate
        raw_link = ali_link_match.group(0)
        ali_link = ensure_affiliate(raw_link)
        formatted = (
            "🎟️ <b>الحقوووا عودة الكوبونات.. احجزوها قبل ما تخلاص! 🏃‍♂️🔥</b>\n\n"
            "AliExpress رجعت توزع في <b>كوبونات خصم عشوائية</b> 🎁\n"
            "احجزوها الآن مباشرة قبل نفاذها:\n\n"
            f"🔗 <b>رابط حجز الكوبونات ⤵️</b>\n{ali_link}\n\n"
            "📌 <b>ملاحظة:</b> حوّل دولة التطبيق إلى الجزائر 🇩🇿 لحجز الكوبونات\n\n"
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


def extract_telegram_html_text(text_div) -> str:
    """
    Safely extracts text from Telegram web widget message HTML without
    chopping numbers or inline formatting across inline tags (<b>, <code>, <i>, <span>).
    Only converts block-level tags (<br>, </p>, </div>, </blockquote>) to newlines.
    """
    if not text_div:
        return ""
    from bs4 import BeautifulSoup
    html = text_div.decode_contents() if hasattr(text_div, "decode_contents") else str(text_div)
    # Replace block breaks and emoji container breaks with newlines
    html = re.sub(r'<(?:br|/p|/div|/blockquote|/tg-emoji|tg-emoji)[^>]*>', '\n', html, flags=re.IGNORECASE)
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()
    # Normalize excessive newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


BRAND_TRANSLITERATIONS = {
    "بوكو": "poco",
    "شاومي": "xiaomi",
    "ريدمي": "redmi",
    "ريلمي": "realme",
    "هونر": "honor",
    "هواوي": "huawei",
    "سامسونج": "samsung",
    "انفينكس": "infinix",
    "تكنو": "tecno",
    "نوبيا": "nubia",
    "لينوفو": "lenovo",
    "اسوس": "asus",
    "انكر": "anker",
    "بيسوس": "baseus",
    "يوغرين": "ugreen",
    "يوجرين": "ugreen",
    "لوجيتك": "logitech",
    "لوجيتيك": "logitech",
    "أجاز": "ajazz",
    "اجاز": "ajazz",
    "امشوز": "mchose",
    "ام شوز": "mchose",
    "مشوز": "mchose",
    "ماتشوز": "mchose",
    "اتاك شارك": "attack shark",
    "أتاك شارك": "attack shark",
    "كولمي": "colmi",
    "كيزيد": "kz",
    "كي زي": "kz",
    "كي زيد": "kz",
    "موندروب": "moondrop",
    "تانغزو": "tangzu",
    "كنترولر": "controller",
    "كنترولرز": "controller",
    "جيمباد": "gamepad",
    "قيمباد": "gamepad",
}

CATEGORY_MAPPINGS = {
    "ماوس": ["mouse", "mice"],
    "كيبورد": ["keyboard"],
    "لوحة مفاتيح": ["keyboard"],
    "سماعة": ["headset", "headphone", "earphone", "earphones", "earbuds", "audio", "tws", "iem", "iems", "kz"],
    "سماعات": ["headset", "headphone", "earphone", "earphones", "earbuds", "audio", "tws", "iem", "iems", "kz"],
    "اذن": ["earphone", "earphones", "earbuds", "in-ear", "iem", "iems", "headphone"],
    "أذن": ["earphone", "earphones", "earbuds", "in-ear", "iem", "iems", "headphone"],
    "الاذن": ["earphone", "earphones", "earbuds", "in-ear", "iem", "iems", "headphone"],
    "الأذن": ["earphone", "earphones", "earbuds", "in-ear", "iem", "iems", "headphone"],
    "كاميرا": ["camera", "webcam"],
    "ويبكام": ["webcam", "camera"],
    "ويب كام": ["webcam", "camera"],
    "هاتف": ["phone", "smartphone", "mobile"],
    "جوال": ["phone", "smartphone", "mobile"],
    "ساعة": ["watch", "smartwatch"],
    "شاحن": ["charger", "gan"],
    "كابل": ["cable", "cord"],
    "تحكم": ["controller", "gamepad", "joystick"],
    "يد تحكم": ["gamepad", "controller", "joystick"],
    "كنترولر": ["controller", "gamepad", "joystick"],
    "كنترولرز": ["controller", "gamepad", "joystick"],
    "جيمباد": ["gamepad", "controller"],
    "قيمباد": ["gamepad", "controller"],
    "مغناطيسي": ["magnetic", "rapid trigger", "hall effect", "keyboard"],
    "مغناطيسية": ["magnetic", "rapid trigger", "hall effect", "keyboard"],
    "ميكانيكي": ["mechanical", "keyboard"],
    "ميكانيكية": ["mechanical", "keyboard"],
    "سلكي": ["wired"],
    "سلكية": ["wired"],
    "لاسلكي": ["wireless"],
    "معالج": ["cpu", "processor", "ryzen", "intel"],
    "مذربورد": ["motherboard", "mainboard"],
    "لوحة ام": ["motherboard", "mainboard"],
    "لوحة أم": ["motherboard", "mainboard"],
    "مايك": ["microphone", "mic"],
    "ميكروفون": ["microphone", "mic"],
    "مايكروفون": ["microphone", "mic"],
}


def compute_title_compatibility(extracted_title: str, candidate_title: str) -> float:
    """
    Computes keyword and category overlap between the message deal title and
    the resolved API / webpage title. Returns a score between 0.0 and 1.0.
    """
    if not extracted_title or not candidate_title:
        return 0.5

    def tokenize(s):
        s = s.lower()
        s = re.sub(r'[^a-zA-Z0-9\u0600-\u06FF]+', ' ', s)
        tokens = set(w for w in s.split() if len(w) >= 2)
        stop = {
            "algeria", "global", "version", "original", "aliexpress", "deal", "drops",
            "edition", "sale", "new", "free", "pro", "max", "ultra", "plus", "lite",
            "الهاتف", "نسخة", "عالمية", "تخفيض", "سعر", "ممتاز",
            "فخمة", "فخم", "احترافية", "احترافي", "ممتازة", "رهيبة", "رهيب",
            "اسطوري", "أسطوري", "أقوى", "اقوى", "أفضل", "افضل", "عرض", "جديد", "جديدة",
            "أصلي", "اصلي", "يد"
        }
        return tokens - stop

    t1 = tokenize(extracted_title)
    t2 = tokenize(candidate_title)
    if not t1 or not t2:
        return 0.5

    # Direct token intersection
    common = t1.intersection(t2)

    # Brand transliteration matching
    for ar_b, en_b in BRAND_TRANSLITERATIONS.items():
        if (ar_b in t1 and en_b in t2) or (en_b in t1 and ar_b in t2):
            common.add(ar_b)

    # Category cross-matching (Arabic to English)
    s1_lower = extracted_title.lower()
    s2_lower = candidate_title.lower()
    for ar_term, en_terms in CATEGORY_MAPPINGS.items():
        matched_1 = ar_term in t1 or (len(ar_term.split()) > 1 and ar_term in s1_lower)
        matched_2 = any(en in t2 for en in en_terms) or (any(en in s2_lower for en in en_terms))
        if matched_1 and matched_2:
            common.add(ar_term)
        matched_rev_1 = ar_term in t2 or (len(ar_term.split()) > 1 and ar_term in s2_lower)
        matched_rev_2 = any(en in t1 for en in en_terms) or (any(en in s1_lower for en in en_terms))
        if matched_rev_1 and matched_rev_2:
            common.add(ar_term)

    score = len(common) / min(len(t1), len(t2))
    return score



