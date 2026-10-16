"""
Category Firewall & Product Type Verification.
Guarantees that headphones, smartwatches, tablets, accessories, and PC parts
can NEVER be mislabeled as smartphones or assigned phone hooks in Telegram captions.
"""

import re
from typing import Tuple

# Audio keywords & Arabic equivalents (pure product nouns, NO brand names)
AUDIO_PATTERNS = [
    r'\b(?:headphone|headphones|earphone|earphones|earbud|earbuds|buds|headset|headsets|tws|iem|iems)\b',
    r'\b(?:soundbar|speaker|speakers|microphone|mic)\b',
    r'سماعة|سماعات|سماعه|ميكروفون|مايك|مكبر\s*صوت'
]

# Smartwatch keywords (excluding watch bands/accessories unless the watch itself)
WEARABLE_PATTERNS = [
    r'\b(?:smartwatch|smart\s*watch)\b',
    r'(?<![a-zA-Z])watch(?!s?[a-zA-Z])',
    r'\b(?:fitness\s*tracker|smart\s*band)\b',
    r'ساعة\s*ذكية|ساعة\s*يد|ساعات\s*ذكية|سوار\s*ذكي'
]

# Tablet keywords (excluding mouse pad / thermal pad)
TABLET_PATTERNS = [
    r'\b(?:tablet|tablets|ipad)\b',
    r'(?<!mouse\s)(?<!thermal\s)(?<!cooling\s)\bpad\b',
    r'تابلت|أجهزة\s*التابلت|جهاز\s*لوحي|لوحي'
]

# PC / Gaming gear
GAMING_PATTERNS = [
    r'\b(?:mouse|keyboard|gamepad|controller|joystick|keycap|switch|rgb|gaming|gamer)\b',
    r'\b(?:gpu|cpu|motherboard|nvme|ssd|ddr4|ddr5|cooler|ryzen|radeon|geforce|rtx)\b',
    r'عتاد\s*قيمنق|فأرة|لوحة\s*مفاتيح|كرت\s*شاشة|معالج'
]

# Accessories (cases, chargers, cables)
ACCESSORY_PATTERNS = [
    r'\b(?:case|cover|holder|charger|cable|protector|glass|film|stand|skin|adapter|mount|strap|powerbank|power\s*bank)\b',
    r'كفر|جراب|شاحن|كابل|سلك|لاصق|حامي\s*شاشة|حامل'
]

# Genuine phone identifiers
PHONE_EXPLICIT_PATTERNS = [
    r'\b(?:smartphone|smartphones|mobile)\b',
    r'(?<![a-zA-Z])phone(?!s?[a-zA-Z])',
    r'هاتف|الهواتف|جوال|الجوال|موبايل'
]

PHONE_BRANDS = [
    "poco", "redmi", "realme", "xiaomi", "infinix", "oneplus",
    "oppo", "vivo", "honor", "samsung", "pixel", "iqoo", "nubia", "zte", "motorola"
]

PHONE_SPEC_PATTERNS = [
    r'\b(?:\d+/\d+|\d+\s*gb|5g|4g|snapdragon|helio|dimensity|pro\+|ultra|gt|note)\b'
]


def is_audio_product(title: str) -> bool:
    t = title.lower()
    return any(bool(re.search(p, t)) for p in AUDIO_PATTERNS)


def is_wearable_product(title: str) -> bool:
    t = title.lower()
    if is_audio_product(t):
        return False
    return any(bool(re.search(p, t)) for p in WEARABLE_PATTERNS)


def is_tablet_product(title: str) -> bool:
    t = title.lower()
    if is_audio_product(t):
        return False
    # Avoid mouse pad / thermal pad
    if "mouse pad" in t or "thermal pad" in t or "cooling pad" in t:
        return False
    return any(bool(re.search(p, t)) for p in TABLET_PATTERNS)


def is_gaming_or_pc_product(title: str) -> bool:
    t = title.lower()
    if is_audio_product(t):
        return False
    return any(bool(re.search(p, t)) for p in GAMING_PATTERNS)


def is_accessory_product(title: str) -> bool:
    t = title.lower()
    return any(bool(re.search(p, t)) for p in ACCESSORY_PATTERNS)


def is_genuine_smartphone(title: str) -> bool:
    """
    Returns True ONLY if the product is verified to be an actual smartphone,
    and NOT headphones, smartwatches, tablets, PC gear, or accessories.
    """
    t = title.lower()

    # Absolute exclusions
    if is_audio_product(t) or is_wearable_product(t) or is_tablet_product(t) or is_accessory_product(t):
        return False

    # Check for explicit phone terms
    if any(bool(re.search(p, t)) for p in PHONE_EXPLICIT_PATTERNS):
        return True

    # Check for phone brand + specs/model series
    has_brand = any(re.search(r'\b' + b + r'\b', t) for b in PHONE_BRANDS)
    has_spec = any(bool(re.search(p, t)) for p in PHONE_SPEC_PATTERNS)

    return has_brand and has_spec


def sanitize_caption_category(caption: str, title: str) -> Tuple[str, bool]:
    """
    Validates that caption hooks match product reality.
    If a non-phone product caption contains smartphone hooks (هاتف, الهواتف, 📱 in hook),
    replaces it with the appropriate category hook.
    Returns (sanitized_caption, was_sanitized).
    """
    if not caption or not title:
        return caption, False

    # If it is a real smartphone, phone hooks are valid
    if is_genuine_smartphone(title):
        return caption, False

    # Check if caption contains a phone hook (search across inner tags like <b>)
    phone_hook_patterns = [
        r'<blockquote>[\s\S]*?(?:هاتف|الهواتف|عالم\s*الهواتف)[\s\S]*?</blockquote>',
        r'<blockquote>[\s\S]*?📱[\s\S]*?(?:مواصفات|لافار|صفقة|هواتف)[\s\S]*?</blockquote>'
    ]

    has_phone_hook = any(bool(re.search(p, caption)) for p in phone_hook_patterns)
    if not has_phone_hook:
        return caption, False

    # Determine correct replacement hook based on actual product category
    if is_audio_product(title):
        replacement = "<blockquote>🎧 <b>سماعات بمواصفات ممتازة وعزل قوي بسعر لافار 🔥🎧</b></blockquote>"
    elif is_wearable_product(title):
        replacement = "<blockquote>⌚ <b>ساعة ذكية بمواصفات ممتازة وسعر لافار متتراطاش 🔥⚡</b></blockquote>"
    elif is_tablet_product(title):
        replacement = "<blockquote>📱 <b>تخفيض قوي في التابلت بمواصفات ممتازة وسعر لافار 🔥⚡</b></blockquote>"
    elif is_gaming_or_pc_product(title):
        replacement = "<blockquote>🎮 <b>صفقة قوية في عتاد قيمنق بسعر ممتاز متتراطاش 🔥⚡</b></blockquote>"
    else:
        replacement = "<blockquote>🔥 <b>سعر ممتاز لافار نهار اليوم 🔥⚡</b></blockquote>"

    sanitized = caption
    for p in phone_hook_patterns:
        sanitized = re.sub(p, replacement, sanitized, count=1)

    return sanitized, True
