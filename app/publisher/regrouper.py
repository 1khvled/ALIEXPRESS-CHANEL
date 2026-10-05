"""
Daily Tajmi3at & Auto-Regrouping Bulletin Algorithm
Automatically aggregates published deals of the exact same category (e.g. 4+ Phones, 4+ Mice, 4+ Keyboards)
into high-converting index bulletins linking back to the channel's own posts at the end of each day (~10:00 PM UTC+1).
Strict Rule: Minimum 4 items required for category bulletins. If no category reaches 4, builds a Master Daily Roundup.
"""
import os
import sys
import json
import re
import asyncio
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Tuple, Optional, Set
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
import httpx

try:
    from sqlalchemy import select
    from app.db.session import db_context
    from app.db.models import Deal, TelegramPost
    HAS_DB = True
except (ImportError, Exception):
    HAS_DB = False

from app.config.settings import settings
from app.utils.logger import logger
from app.publisher.state_tracker import (
    load_persistent_state,
    save_persistent_state,
    is_tajmi3at_time_window,
    is_daily_tajmi3at_eligible,
    record_daily_tajmi3at_published,
    get_regrouped_channel_msg_ids,
    record_deals_regrouped,
    TARGET_CHANNEL_ID
)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8900887118:AAELbFHyV2joUO-4EJ0fPSoZurkQNuENbfY")
ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN", "8708965924:AAH7SoSX7VV3Nx_yI_J39VzWjlsc-XPgXAQ")

CATEGORIES_CONFIG = {
    "phones": {
        "header": "📱 <b>تجميعة أقوى عروض الهواتف الذكية لنهار اليوم 🇩🇿🔥</b>",
        "tag": "#تجميعة_الهواتف",
        "keywords": [
            "phone", "phones", "smartphone", "smartphones", "هاتف", "جوال", "موبايل",
            "poco", "redmi", "realme", "honor", "samsung", "infinix", "oppo", "vivo",
            "iphone", "nubia", "zte", "motorola", "iqoo", "oneplus", "meizu", "tecno"
        ],
        "negative_keywords": [
            "headset", "earphone", "case", "cover", "holder", "charger",
            "cable", "cooler", "mousepad", "mouse pad", "screen protector", "glass", "film",
            "watch", "band", "ساعة", "سوار", "smartwatch", "قلم", "stylus",
            "بوشات", "زجاج", "واقي", "تابلت", "tablet", "pad"
        ]
    },
    "gaming_pads": {
        "header": "🖱️ <b>تجميعة أفضل ماوس باد وسجادات القيمنق لنهار اليوم 🇩🇿🔥</b>",
        "tag": "#تجميعة_الماوس_باد",
        "keywords": [
            "mousepad", "mouse pad", "mouse mat", "desk mat", "gaming pad",
            "ماوس باد", "باد ماوس", "سجادة ماوس", "بساط ماوس", "سجادة مكتب",
            "pad gaming", "attack shark pad", "speed pad", "control pad", "cordura pad",
            "glass mousepad"
        ],
        "negative_keywords": [
            "thermal pad", "ptm7950", "tablet", "phone", "هاتف", "تابلت"
        ]
    },
    "controllers": {
        "header": "🎮 <b>تجميعة أجهزة وأيادي التحكم (Gamepads) لنهار اليوم 🇩🇿🔥</b>",
        "tag": "#تجميعة_الكونترولر",
        "keywords": [
            "gamepad", "controller", "joystick", "يد تحكم", "ذراع تحكم", "كنترولر",
            "جيم باد", "يد العاب", "manette", "easysmx", "gamesir", "machenike g3",
            "machenike g5", "machenike g6", "fantech shooter", "fantech nova",
            "flydigi", "8bitdo", "gulikit", "tarantula 8k", "dobe"
        ],
        "negative_keywords": [
            "holder", "stand", "case", "cover"
        ]
    },
    "mice": {
        "header": "🖱️ <b>تجميعة ماوسات القيمنق الاحترافية لنهار اليوم 🇩🇿🔥</b>",
        "tag": "#تجميعة_الماوسات",
        "keywords": [
            "mouse", "mice", "ماوس", "فأرة", "فارة", "wireless mouse", "gaming mouse",
            "attack shark x3", "attack shark r1", "attack shark x1", "attack shark x11",
            "attack shark x6", "attack shark r3", "attack shark r6", "attack shark x5",
            "attack shark x7", "attack shark mouse", "ajazz aj", "aj199", "aj139", "aj159",
            "aj099", "vxe r1", "vxe mad", "vgn dragonfly", "vgn f1", "scyrox", "zaopin",
            "darmoshark m", "fantech aria", "fantech xd7", "delux m"
        ],
        "negative_keywords": [
            "mousepad", "mouse pad", "pad", "باد", "باد ماوس", "سجادة", "mat"
        ]
    },
    "keyboards": {
        "header": "⌨️ <b>تجميعة الكيبوردات الميكانيكية لنهار اليوم 🇩🇿🔥</b>",
        "tag": "#تجميعة_الكيبوردات",
        "keywords": [
            "keyboard", "keyboards", "كيبورد", "لوحة مفاتيح", "mechanical keyboard",
            "ak820", "ak870", "ak992", "ak680", "rainy75", "hi75", "crush80",
            "aula f75", "aula f87", "aula f99", "attack shark k86", "attack shark k98",
            "attack shark k75", "attack shark k87", "attack shark k68", "ajazz ak",
            "machenike k500", "kzzi", "epomaker", "fantech maxfit"
        ],
        "negative_keywords": [
            "keycap", "keycaps", "switch", "switches", "سويتش", "كيكاب"
        ]
    },
    "gaming_gear": {
        "header": "🎮 <b>تجميعة ملحقات وعتاد القيمنق لنهار اليوم 🇩🇿🔥</b>",
        "tag": "#تجميعة_القيمنق",
        "keywords": [],
        "negative_keywords": []
    },
    "headsets": {
        "header": "🎧 <b>تجميعة أفضل السماعات والصوتيات لنهار اليوم 🇩🇿🔥</b>",
        "tag": "#تجميعة_السماعات",
        "keywords": [
            "headset", "headsets", "headphone", "headphones", "earbuds", "earbud",
            "earphone", "earphones", "tws", "iem", "سماعة", "سماعات", "سماعة محيطية",
            "attack shark l80", "attack shark l90", "lenovo xt", "lenovo lp", "lenovo th",
            "htc ne", "kz edx", "kz castor", "moondrop", "qcy", "soundcore",
            "monster mqt", "monster maxstar", "cmf buds", "baseus bowie", "redmi buds", "edifier"
        ],
        "negative_keywords": [
            "case", "cover", "cable", "كابل", "stand", "holder"
        ]
    },
    "tablets": {
        "header": "📟 <b>تجميعة أجهزة التابلت واللوحيات لنهار اليوم 🇩🇿🔥</b>",
        "tag": "#تجميعة_التابلت",
        "keywords": [
            "tablet", "tablets", "tab", "ipad", "تابلت", "ايباد", "لوحي",
            "xiaomi pad", "redmi pad", "realme pad", "blackview pad", "blackview link",
            "blackview mega", "blackview tab", "honor pad", "oneplus pad", "lenovo tab",
            "xiaoxin", "matepad", "teclast", "chuwi", "alldocube", "oscal pad"
        ],
        "negative_keywords": [
            "mousepad", "mouse pad", "thermal pad", "ptm7950", "cooling pad",
            "case", "cover", "holder", "stand", "screen protector", "بوشات", "واقي"
        ]
    },
    "smartwatches": {
        "header": "⌚ <b>تجميعة الساعات الذكية المعتمدة لنهار اليوم 🇩🇿🔥</b>",
        "tag": "#تجميعة_الساعات",
        "keywords": [
            "smartwatch", "smart watch", "smart band", "ساعة ذكية", "ساعة",
            "سوار ذكي", "watch", "colmi", "zeblaze", "amazfit", "choice watch",
            "watch x", "watch 2", "watch 3", "watch 4", "watch 5", "watch pro",
            "cmf watch", "btalk", "curren", "naviforce", "skmei", "poedagar", "lige"
        ],
        "negative_keywords": [
            "strap", "حزام", "screen protector", "حماية", "charger", "cable"
        ]
    },
    "pc_parts": {
        "header": "🖥️ <b>تجميعة عتاد وقطع البي سي لنهار اليوم 🇩🇿🔥</b>",
        "tag": "#تجميعة_البي_سي",
        "keywords": [
            "ram", "ssd", "nvme", "gpu", "graphics card", "cooler", "thermal pad",
            "ptm7950", "كارت شاشة", "كرت شاشة", "معالج", "مشتت", "رام", "ddr4", "ddr5",
            "ryzen", "somnambulist", "cpu", "motherboard", "لوحة أم", "carte mere",
            "b450", "b550", "b650", "x470", "x570", "x670", "z790", "z690",
            "fenvi", "network card", "pcie"
        ],
        "negative_keywords": [
            "case phone", "cover phone"
        ]
    },
    "chargers_cables": {
        "header": "⚡ <b>تجميعة الشواحن السريعة والباوربانك لنهار اليوم 🇩🇿🔥</b>",
        "tag": "#تجميعة_الشواحن",
        "keywords": [
            "gan charger", "شاحن سريع", "شاحن سيارة", "شاحن جداري", "powerbank", "باور بانك",
            "ugreen 30w", "ugreen 65w", "ugreen charger", "toocki 60w", "toocki 100w",
            "toocki charger", "toocki usb", "toocki 2.4a", "baseus charger", "samsung charger",
            "anker charger"
        ],
        "negative_keywords": [
            "phone", "smartphone", "watch"
        ]
    }
}

def classify_deal_category(title: str, text: str = "") -> Optional[str]:
    """Strictly classifies a deal into a primary homogeneous product category using word boundaries."""
    if not title:
        return None

    # Exclude multi-accessory combo packs (e.g. بوشات / كابل / ماوس / قلم)
    if title.count("/") >= 3:
        return None

    combined = f"{title or ''} {text or ''}".lower()

    # Priority order: specialized/niche items first before broader categories
    priority_order = [
        "gaming_pads",
        "controllers",
        "tablets",
        "keyboards",
        "mice",
        "headsets",
        "smartwatches",
        "pc_parts",
        "chargers_cables",
        "phones"
    ]

    for cat_name in priority_order:
        config = CATEGORIES_CONFIG[cat_name]

        # Check negative keywords first
        has_negative = False
        for neg in config["negative_keywords"]:
            if re.search(rf'(?:\b|_){re.escape(neg)}(?:\b|_)', combined) or neg in combined:
                has_negative = True
                break
        if has_negative:
            continue

        # Special regex pattern for tablets (e.g. Pad 6, Pad7, Pad Pro)
        if cat_name == "tablets" and re.search(r'\bpad\d*\b', combined):
            return cat_name

        # Check positive keywords with word boundaries
        for kw in config["keywords"]:
            if any(ord(char) > 127 for char in kw):
                if kw in combined:
                    return cat_name
            else:
                if re.search(rf'\b{re.escape(kw)}\b', combined) or kw in combined:
                    return cat_name

    return None


NUMBER_BADGES = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟", "1️⃣1️⃣", "1️⃣2️⃣", "1️⃣3️⃣", "1️⃣4️⃣", "1️⃣5️⃣"]

def clean_product_name_short(raw_title: str, max_chars: int = 32) -> str:
    """
    Extracts clean, concise Brand and Model name from an AliExpress title.
    Transforms verbose SEO spam into sleek titles like 'EasySMX X15' or 'Haylou S40 ANC'.
    """
    if not raw_title:
        return "منتج مميز"

    t = raw_title.strip()
    # Remove leading emojis and bullet symbols
    t = re.sub(r'^[❗️🔖📌🔥🚨⚡💥✨📦🛒🎁📢✅💎💰🔻ـ\s\-:]+', '', t).strip()
    # Remove prices inside title
    t = re.sub(r'[\$€].*$', '', t).strip()
    # Remove store suffixes / watermarks
    t = re.sub(r'(\s*-\s*AliExpress.*$|\s*\|\s*AliExpress.*$)', '', t, flags=re.IGNORECASE).strip()
    # Remove marketing buzzwords
    t = re.sub(
        r'\b(Global\s+Version|Original|Hot\s+Sale|Brand\s+New|Top\s+Selling|Official\s+Store|Official|Edition|Newest|Version\s+Globale|202[4-9])\b',
        '', t, flags=re.IGNORECASE
    ).strip()

    trim_patterns = [
        r'\b(?:(?:Wireless|PC\s+Gaming|PC|Gaming|Tri-Mode)?\s*(?:Gamepad|Controller|Game\s+Controller|Joystick|Manette))\b.*$',
        r'\b(?:(?:Wireless|Optical|Wired)?\s*(?:Gaming\s+Mouse|Mouse\s+Gamer|Mouse|Mice))\b.*$',
        r'\b(?:(?:Mechanical|Gaming|Wireless)?\s*(?:Keyboard|Keyboards|Clavier))\b.*$',
        r'\b(?:(?:Wireless|Gaming)?\s*(?:Headphones?|Headsets?|Earphones?|Earbuds?|Casque))\b.*$',
        r'\b(?:Tri-Mode|Dual-Mode|Tri\s+Mode|Dual\s+Mode)\b.*$',
        r'\b(?:Wireless\s+Bluetooth|Bluetooth\s+[0-9\.]+|Bluetooth)\b.*$',
        r'\b(?:Hall\s+Effect\b.*$)',
        r'\b(?:Noise\s+Cancell\w*|50dB|45dB|42dB|40dB|35dB)\b.*$',
        r'\b(?:with\s+Charging\s+Dock|Charging\s+Dock)\b.*$',
        r'\b(?:Smartphones?|Smart\s+Phone|Mobile\s+Phone)\b.*$',
        r'\b(?:Smart\s*Watch|Smart\s*Band)\b.*$',
        r'\b(?:Internal\s+Solid\s+State|Internal\s+SSD|Solid\s+State\s+Drive)\b.*$',
        r'\b(?:Fast\s+Charging|GaN\s+Fast\s+Charger|Wall\s+Charger)\b.*$',
        r'\b(?:Large\s+Desk\s+Mat|Desk\s+Mat|Mousepad|Mouse\s+Pad|Tapis\s+de\s+Souris)\b.*$',
        r'\b(?:Dynamic\s+Drivers?|Dynamic)\b.*$'
    ]
    for pat in trim_patterns:
        m = re.search(pat, t, flags=re.IGNORECASE)
        if m and m.start() >= 5:
            t = t[:m.start()].strip()
            break

    # Strip trailing loose descriptors
    t = re.sub(r'\b(?:Wireless|PC|SATA\s*\d*|Dynamic)\b\s*$', '', t, flags=re.IGNORECASE).strip()
    t = t.rstrip(" -,/:;|+")

    dangling_words = {'with', 'for', 'and', 'to', 'in', 'on', 'of', 'by', 'the', 'a', 'an', 'wit', 'fo', 'avec', 'pour', 'et', 'de', 'du', 'en', 'sur', 'dans', 'مع', 'من', 'في', 'على', 'لـ', 'إلى', 'ل'}
    words = t.split()
    if words and words[-1].lower() in dangling_words:
        t = " ".join(words[:-1]).rstrip(" -,/:;|+")

    if len(t) > max_chars:
        words = t.split()
        shortened = ""
        for w in words:
            if len(shortened + " " + w) <= max_chars:
                shortened = (shortened + " " + w).strip()
            else:
                break
        if len(shortened) >= 6:
            t = shortened.rstrip(" -,/:;|+")
        else:
            t = t[:max_chars].strip()

    return t or raw_title[:max_chars].strip()

def clean_item_title(raw_title: str, max_chars: int = 32) -> str:
    """Produces clean, readable title for the bulletin line without slicing words in half."""
    return clean_product_name_short(raw_title, max_chars=max_chars)

def get_deal_dedup_key(product_id: Optional[Any], raw_title: str, msg_id: int) -> str:
    """Builds a unique deduplication key for a product to prevent identical products from appearing twice."""
    if product_id:
        p_clean = str(product_id).strip()
        if p_clean and p_clean.lower() not in ("none", "null", "0", "") and not p_clean.startswith("msg_"):
            return f"pid_{p_clean}"

    t = (raw_title or "").lower()
    t = re.sub(r'[\$€].*$', '', t)
    t = re.sub(r'^[❗️🔖📌🔥🚨⚡💥✨📦🛒🎁📢✅💎💰🔻ـ\s\-:]+', '', t)
    t = re.sub(r'[^\w\s]', ' ', t)
    stop_words = {
        'original', 'global', 'version', 'new', 'hot', 'sale', 'official',
        'free', 'shipping', 'edition', 'جديد', 'اصلي', 'نسخة', 'تخفيض', 'عرض'
    }
    tokens = [w for w in t.split() if len(w) > 2 and w not in stop_words]
    if len(tokens) >= 2:
        return "norm_" + "_".join(tokens[:4])
    elif tokens:
        return f"norm_{tokens[0]}"
    return f"msg_{msg_id}"

def is_better_deal(candidate: Dict[str, Any], current: Dict[str, Any]) -> bool:
    """Selects the best deal entry between duplicate posts of the same product."""
    cand_price = float(candidate.get("price") or 0.0)
    curr_price = float(current.get("price") or 0.0)

    # 1. If both have positive prices, strictly lower price wins (e.g. $5.09 vs $13.20 flash drop)
    if cand_price > 0 and curr_price > 0:
        if cand_price < curr_price:
            return True
        if curr_price < cand_price:
            return False
    elif cand_price > 0 and curr_price <= 0:
        return True
    elif curr_price > 0 and cand_price <= 0:
        return False

    # 2. If prices are identical (or both <= 0), prefer the freshest post
    return int(candidate.get("channel_msg_id") or 0) > int(current.get("channel_msg_id") or 0)

def get_recent_published_deals_for_roundup(max_age_hours: float = 24.0) -> List[Dict[str, Any]]:
    """
    Collects active deals published to @DzAliexpress0 within the last 24 hours.
    Deduplicates identical products posted multiple times during the day (keeps lowest price / latest post).
    """
    state = load_persistent_state()
    deals_dict = state.get("channel_published_deals", {})
    now = datetime.now(timezone.utc).timestamp()
    max_age_sec = max_age_hours * 3600

    collected: Dict[str, Dict[str, Any]] = {}

    # 1. Load from persistent state (primary in GitHub Actions & production)
    target_clean = str(TARGET_CHANNEL_ID).lstrip("@")
    for post_key, info in deals_dict.items():
        if info.get("status") == "DELETED":
            continue
        msg_id = info.get("channel_msg_id")
        if not msg_id or int(msg_id) <= 0:
            continue
        ts = info.get("timestamp", 0)
        if (now - ts) > max_age_sec:
            continue

        msg_id_int = int(msg_id)
        raw_title = info.get("title", "")
        title = clean_item_title(raw_title)
        price = float(info.get("price") or 0.0)
        category = classify_deal_category(raw_title)
        product_id = info.get("product_id")

        deal_entry = {
            "channel_msg_id": msg_id_int,
            "product_id": product_id,
            "title": title,
            "price": price,
            "timestamp": ts,
            "category": category,
            "channel_url": f"https://t.me/{target_clean}/{msg_id_int}"
        }

        dedup_key = get_deal_dedup_key(product_id, raw_title, msg_id_int)
        if dedup_key not in collected:
            collected[dedup_key] = deal_entry
        else:
            if is_better_deal(deal_entry, collected[dedup_key]):
                collected[dedup_key] = deal_entry

    return list(collected.values())

def format_deal_line(item: Dict[str, Any], channel_username: str, index: int = 1) -> str:
    """Formats a single product line for the bulletin matching the clean Anis/Lody index style."""
    title = clean_product_name_short(item.get("title") or "منتج مميز")
    price_val = float(item.get("price") or 0.0)

    if price_val > 0:
        if price_val.is_integer():
            price_str = f"${int(price_val)}"
        else:
            price_str = f"${price_val:.2f}"
    else:
        price_str = "سعر خاص 🔥"

    badge = NUMBER_BADGES[index - 1] if 1 <= index <= len(NUMBER_BADGES) else f"{index}️⃣"
    clean_ch = channel_username.replace("@", "")
    post_url = item.get("channel_url") or f"https://t.me/{clean_ch}/{item['channel_msg_id']}"
    return f"{badge} 🌐 <a href=\"{post_url}\"><b>{title}</b></a> ▫️ <b>{price_str}</b>"

def build_category_bulletin_text(
    category_name: str,
    items: List[Dict[str, Any]],
    channel_username: str,
    part: Optional[int] = None,
    total_parts: Optional[int] = None
) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Builds the caption for a category bulletin matching the sleek Anis/Lody index style.
    Supports multi-part pagination (الجزء 1, الجزء 2) when a category has many deals.
    Dynamically fits items to guarantee the total length strictly never exceeds 980 characters (Telegram photo caption limit: 1024).
    """
    cat_config = CATEGORIES_CONFIG.get(category_name, {
        "header": f"📦 <b>تجميعة عروض {category_name} لنهار اليوم 🇩🇿🔥</b>"
    })
    clean_ch = channel_username.replace("@", "")

    base_header = cat_config["header"]
    if part and total_parts and total_parts > 1:
        if "🇩🇿🔥</b>" in base_header:
            header_text = base_header.replace("🇩🇿🔥</b>", f"(الجزء {part}) 🇩🇿🔥</b>")
        else:
            header_text = base_header.replace("</b>", f" (الجزء {part})</b>")
    else:
        header_text = base_header

    header_lines = [
        header_text,
        "",
        "👈 <b>إضغط على إسم المنتج ليأخذك مباشرة للعرض ⚪️</b>",
        ""
    ]
    footer_lines = [
        "",
        "━━━━━━━━━━━━━━━━━",
        "🪙 <b>تخفيض العملات:</b> أرسل رابط أي منتج للبوت (@Alilo07BOT)",
        f"📢 <b>قناتنا:</b> @{clean_ch}"
    ]
    footer_text = "\n".join(footer_lines)

    selected_items: List[Dict[str, Any]] = []
    body_lines: List[str] = []

    for idx, item in enumerate(items, start=1):
        line = format_deal_line(item, channel_username, index=idx)
        candidate_text = "\n".join(header_lines + body_lines + [line, footer_text])
        if len(candidate_text) > 980:
            break
        body_lines.append(line)
        selected_items.append(item)

    full_caption = "\n".join(header_lines + body_lines + footer_lines)
    return full_caption, selected_items

def build_master_daily_roundup_text(deals: List[Dict[str, Any]], channel_username: str) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Builds the Master Daily Roundup when individual categories don't have >= 4 items.
    Selects top deals across diverse categories matching the sleek Anis/Lody index style.
    """
    clean_ch = channel_username.replace("@", "")
    header_lines = [
        "🌙 <b>تجميعة أفضل صفقات وعروض اليوم على AliExpress 🇩🇿🔥</b>",
        "",
        "👈 <b>إضغط على إسم المنتج ليأخذك مباشرة للعرض ⚪️</b>",
        ""
    ]
    footer_lines = [
        "",
        "━━━━━━━━━━━━━━━━━",
        "🪙 <b>تخفيض العملات:</b> أرسل رابط أي منتج للبوت (@Alilo07BOT)",
        f"📢 <b>قناتنا:</b> @{clean_ch}"
    ]
    footer_text = "\n".join(footer_lines)

    selected_items: List[Dict[str, Any]] = []
    body_lines: List[str] = []

    # Take deals with valid prices, prioritized
    sorted_deals = sorted(deals, key=lambda x: x.get("price", 0), reverse=True)

    for idx, item in enumerate(sorted_deals, start=1):
        line = format_deal_line(item, channel_username, index=idx)
        candidate_text = "\n".join(header_lines + body_lines + [line, footer_text])
        if len(candidate_text) > 980:
            break
        body_lines.append(line)
        selected_items.append(item)

    full_caption = "\n".join(header_lines + body_lines + footer_lines)
    return full_caption, selected_items

async def check_and_publish_regrouped_bulletins(
    bot_token: Optional[str] = None,
    force: bool = False,
    min_items: int = 3,
    max_bulletins: int = 4
) -> List[Dict[str, Any]]:
    """
    Daily 10:00 PM Tajmi3at (Roundups) Publisher.
    - If not forced: strictly verifies the ~10 PM window (21:30 - 23:45 UTC+1) and daily idempotency.
    - Collects deals published today on @DzAliexpress0.
    - Publishes category roundups for categories meeting min_items (default 3).
    - If no category reaches min_items, publishes a Master Daily Roundup.
    - Attaches storage/assets/tajmi3at_banner.png.
    - Records daily completion to prevent duplicate postings.
    """
    token = bot_token or TELEGRAM_BOT_TOKEN or ADMIN_BOT_TOKEN
    target = TARGET_CHANNEL_ID
    target_clean = str(target).lstrip("@")

    # 1. Timing check: STRICTLY AT NIGHT ONLY (21:30 - 23:45 Algiers time UTC+1)
    if not force:
        if not is_tajmi3at_time_window():
            logger.info("[TAJMI3AT] Outside night window (21:30 - 23:45 Algiers time UTC+1). Tajmi3at runs strictly at night. Skipping.")
            return []

        from app.aliexpress.promos import promo_tracker
        active_promo = promo_tracker.get_active_promo()
        if not active_promo:
            # When promo event has ended: strictly at most once per calendar day (no reposting)
            eligible, reason = is_daily_tajmi3at_eligible()
            if not eligible:
                logger.info(f"[TAJMI3AT] Daily tajmi3at not eligible: {reason}. Skipping.")
                return []

    from app.aliexpress.promos import promo_tracker
    active_promo = promo_tracker.get_active_promo()
    logger.info(f"[TAJMI3AT] Starting Night Tajmi3at roundup execution (Active Promo: {active_promo.name if active_promo else 'None'})...")

    # 2. Fetch all active deals published to @DzAliexpress0 in the last 24-48h
    lookup_hours = 48.0 if active_promo else 24.0
    today_deals = get_recent_published_deals_for_roundup(max_age_hours=lookup_hours)
    if not today_deals:
        logger.info("[TAJMI3AT] No deals published in the lookup window found in state. Skipping.")
        return []

    # 3. Filter deals: during active promos, all deals of the event are available for roundup!
    if active_promo:
        available_deals = today_deals
    else:
        regrouped_ids = get_regrouped_channel_msg_ids()
        available_deals = [d for d in today_deals if d["channel_msg_id"] not in regrouped_ids] if not force else today_deals

    # 4. Group by category
    deals_by_category: Dict[str, List[Dict[str, Any]]] = {k: [] for k in CATEGORIES_CONFIG.keys()}
    other_deals: List[Dict[str, Any]] = []

    for d in available_deals:
        cat = d.get("category")
        if cat and cat in deals_by_category:
            deals_by_category[cat].append(d)
        else:
            other_deals.append(d)

    # 5. Smart Grouping & Aggregation
    qualifying_categories: List[Tuple[str, List[Dict[str, Any]]]] = []

    # Gaming peripheral categories: mice, keyboards, controllers, gaming_pads
    GAMING_CATS = ["mice", "keyboards", "controllers", "gaming_pads"]
    unassigned_gaming_deals: List[Dict[str, Any]] = []

    for cat_name, items in deals_by_category.items():
        if cat_name in GAMING_CATS:
            if len(items) >= min_items:
                qualifying_categories.append((cat_name, items))
            else:
                unassigned_gaming_deals.extend(items)
        elif cat_name != "gaming_gear":
            if len(items) >= min_items:
                qualifying_categories.append((cat_name, items))

    # Smart fallback for gaming gear:
    # If individual gaming categories had < min_items, but combined they reach >= min_items,
    # bundle them into a high-converting 'gaming_gear' bulletin!
    if len(unassigned_gaming_deals) >= min_items:
        logger.info(f"[TAJMI3AT] Smart Gaming Aggregation: Grouped {len(unassigned_gaming_deals)} items into 'gaming_gear' bulletin.")
        qualifying_categories.append(("gaming_gear", unassigned_gaming_deals))

    # Sort by number of items descending (most abundant categories first)
    qualifying_categories.sort(key=lambda x: len(x[1]), reverse=True)

    published_bulletins: List[Dict[str, Any]] = []
    all_regrouped_msg_ids: List[int] = []

    banner_path = Path(settings.BASE_DIR) / "storage" / "assets" / "tajmi3at_banner.png"
    if not banner_path.exists():
        banner_path = Path(settings.BASE_DIR) / "assets" / "tajmi3at_banner.png"

    reply_markup = {
        "inline_keyboard": [
            [
                {"text": "🪙 فتح بوت تخفيض العملات", "url": "https://t.me/Alilo07BOT"}
            ],
            [
                {"text": "📢 قناة الصفقات المعتمدة", "url": f"https://t.me/{target_clean}"}
            ]
        ]
    }

    api_url = f"https://api.telegram.org/bot{token}"

    async with httpx.AsyncClient(timeout=25.0) as client:
        # CASE A: At least one category meets min_items (>= 4)
        if qualifying_categories:
            to_publish = qualifying_categories[:max_bulletins]
            for cat_name, cat_items in to_publish:
                remaining_items = list(cat_items)
                total_parts = (len(cat_items) + 7) // 8 if len(cat_items) > 8 else 1
                part = 1

                while remaining_items:
                    bulletin_text, used_items = build_category_bulletin_text(
                        cat_name, remaining_items, target_clean,
                        part=part if total_parts > 1 else None,
                        total_parts=total_parts if total_parts > 1 else None
                    )
                    if not used_items:
                        break

                    sent_data = None
                    # Send photo with caption
                    if banner_path.exists() and len(bulletin_text) <= 1024:
                        with open(banner_path, "rb") as bf:
                            mime = "image/png" if banner_path.suffix.lower() == ".png" else "image/jpeg"
                            resp = await client.post(
                                f"{api_url}/sendPhoto",
                                data={
                                    "chat_id": target,
                                    "caption": bulletin_text,
                                    "parse_mode": "HTML",
                                    "reply_markup": json.dumps(reply_markup)
                                },
                                files={"photo": (banner_path.name, bf, mime)}
                            )
                            sent_data = resp.json()

                    # Fallback to sendMessage if photo upload failed or text > 1024
                    if not sent_data or not sent_data.get("ok"):
                        resp = await client.post(
                            f"{api_url}/sendMessage",
                            json={
                                "chat_id": target,
                                "text": bulletin_text,
                                "parse_mode": "HTML",
                                "disable_web_page_preview": True,
                                "reply_markup": reply_markup
                            }
                        )
                        sent_data = resp.json()

                    if sent_data and sent_data.get("ok"):
                        b_msg_id = sent_data["result"]["message_id"]
                        used_ids = [it["channel_msg_id"] for it in used_items]
                        all_regrouped_msg_ids.extend(used_ids)

                        part_label = f" (Part {part}/{total_parts})" if total_parts > 1 else ""
                        logger.info(f"[TAJMI3AT] Published {cat_name}{part_label} bulletin #{b_msg_id} with {len(used_items)} items to {target}")
                        published_bulletins.append({
                            "category": f"{cat_name}_part{part}" if total_parts > 1 else cat_name,
                            "message_id": b_msg_id,
                            "count": len(used_items)
                        })
                        await asyncio.sleep(2.5)
                    else:
                        logger.error(f"[TAJMI3AT] Failed to publish {cat_name} bulletin: {sent_data}")
                        break

                    remaining_items = remaining_items[len(used_items):]
                    part += 1

        # CASE B: No single category reached 4 items, but we have >= 3 deals today
        elif len(available_deals) >= 3:
            logger.info(f"[TAJMI3AT] No category reached {min_items} items. Building Master Daily Roundup with {len(available_deals)} deals.")
            bulletin_text, used_items = build_master_daily_roundup_text(available_deals, target_clean)
            if used_items:
                sent_data = None
                if banner_path.exists() and len(bulletin_text) <= 1024:
                    with open(banner_path, "rb") as bf:
                        mime = "image/png" if banner_path.suffix.lower() == ".png" else "image/jpeg"
                        resp = await client.post(
                            f"{api_url}/sendPhoto",
                            data={
                                "chat_id": target,
                                "caption": bulletin_text,
                                "parse_mode": "HTML",
                                "reply_markup": json.dumps(reply_markup)
                            },
                            files={"photo": (banner_path.name, bf, mime)}
                        )
                        sent_data = resp.json()

                if not sent_data or not sent_data.get("ok"):
                    resp = await client.post(
                        f"{api_url}/sendMessage",
                        json={
                            "chat_id": target,
                            "text": bulletin_text,
                            "parse_mode": "HTML",
                            "disable_web_page_preview": True,
                            "reply_markup": reply_markup
                        }
                    )
                    sent_data = resp.json()

                if sent_data and sent_data.get("ok"):
                    b_msg_id = sent_data["result"]["message_id"]
                    used_ids = [it["channel_msg_id"] for it in used_items]
                    all_regrouped_msg_ids.extend(used_ids)

                    logger.info(f"[TAJMI3AT] Published Master Daily Roundup #{b_msg_id} with {len(used_items)} items to {target}")
                    published_bulletins.append({
                        "category": "master_roundup",
                        "message_id": b_msg_id,
                        "count": len(used_items)
                    })

    # 6. Record state & idempotency if any bulletin was published
    if published_bulletins:
        record_deals_regrouped(all_regrouped_msg_ids)
        record_daily_tajmi3at_published(bulletins_count=len(published_bulletins))
        logger.info(f"[TAJMI3AT] Successfully finished Daily Tajmi3at: {len(published_bulletins)} bulletin(s) published.")
    else:
        logger.info("[TAJMI3AT] No bulletins published during this cycle.")

    return published_bulletins

if __name__ == "__main__":
    force_mode = "--force" in sys.argv or "-f" in sys.argv
    print(f"Running check_and_publish_regrouped_bulletins(force={force_mode})...")
    res = asyncio.run(check_and_publish_regrouped_bulletins(force=force_mode))
    print(f"Result: {len(res)} bulletin(s) published: {res}")
