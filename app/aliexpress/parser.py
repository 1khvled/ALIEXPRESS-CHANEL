import re
from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict
from app.config.settings import settings

# Regex patterns for price detection
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

# Patterns for single coupon code
COUPON_PATTERNS = [
    re.compile(r'(?:كوبـــ?ون|كود|code|coupon)\s*(?:[0-9]+(?:\.[0-9]+)?/[0-9]+(?:\.[0-9]+)?\$?)?\s*[:：\-]\s*([A-Za-z0-9_-]{3,25})', re.IGNORECASE),
    re.compile(r'🎟️?\s*(?:كوبـــ?ون|كود|code|coupon)\s*[:：\-]?\s*([A-Za-z0-9_-]{3,25})', re.IGNORECASE),
    re.compile(r'(?:استخدم كود|استعمل كود|قسيمة)\s*[:：\-]?\s*([A-Za-z0-9_-]{3,25})', re.IGNORECASE),
]

# Points discount patterns
POINTS_PATTERNS = [
    re.compile(r'خصم\s*(?:النقاط|نقاط|العملات)', re.IGNORECASE),
    re.compile(r'نقاط\s*علي\s*إكسبريس', re.IGNORECASE),
    re.compile(r'coins\s*discount', re.IGNORECASE),
    re.compile(r'تخفيض\s*العملات', re.IGNORECASE),
    re.compile(r'تحتاج\s*الى\s*العملات', re.IGNORECASE),
    re.compile(r'رابط\s*العملات', re.IGNORECASE),
]

# Spam & non-deal keywords
BLOCKED_STORE_KEYWORDS = [
    "temu", "تيمو", "amazon", "امازون", "أمازون", "shein", "شي ان", "noon", "نون"
]

NON_DEAL_INDICATORS = [
    "pinned a photo", "pinned a message", "تبادل إعلاني", "تبادل اعلاني",
    "اشترك في قناتنا", "قناتنا الاحتياطية", "مسابقة ربح", "قنواتنا"
]

def is_spam_or_non_deal(text: str) -> Tuple[bool, Optional[str]]:
    """
    Identifies spam, competing platforms (Temu, Amazon), or random non-deal messages.
    """
    if not text or len(text.strip()) < 10:
        return True, "Message is too short or empty"

    lower_text = text.lower()

    # Block competing e-commerce platforms
    for store in BLOCKED_STORE_KEYWORDS:
        if store in lower_text:
            return True, f"Blocked store or platform detected: {store}"

    # Block channel admin spam / meta chatter without deal context
    for spam_kw in NON_DEAL_INDICATORS:
        if spam_kw in lower_text and not any(k in lower_text for k in ["aliexpress", "s.click", "تخفيض", "سعر", "كوبون"]):
            return True, f"Non-deal announcement: {spam_kw}"

    return False, None

def extract_coupon_list(text: str) -> List[Dict[str, str]]:
    """
    Detects and extracts lists of multiple promo codes from bulletin posts.
    e.g. 🎟️ كوبون 4/35$ : BDQT04
    """
    if not text:
        return []

    coupons = []
    lines = text.splitlines()

    for line in lines:
        line_clean = line.strip()
        if not line_clean or "http://" in line_clean or "https://" in line_clean:
            continue

        # Look for pattern: [كوبون] [tier] : [CODE]
        # Match lines like: كوبون 4/35$ : BDQT04 or 4/35$ : BDQT04 or 10/99$: BDQT10
        m = re.search(
            r'(?:🎟️?|🎫)?\s*(?:كوبـــ?ون|كود|code)?\s*([0-9]+(?:\.[0-9]+)?/[0-9]+(?:\.[0-9]+)?\$?|[0-9]+\$?(?:\s*/\s*[0-9]+\$?)?)\s*[:：\-]?\s*([A-Za-z0-9_-]{4,20})',
            line_clean,
            re.IGNORECASE
        )
        if m:
            tier = m.group(1).strip()
            code = m.group(2).strip()
            if not tier.endswith("$"):
                tier += "$"
            # Avoid picking false codes like "https", "aliexpress"
            if code.lower() not in {"http", "https", "aliexpress", "item", "link", "t.me"}:
                coupons.append({"tier": tier, "code": code.upper()})

    return coupons

def extract_prices(text: str) -> Tuple[Optional[float], Optional[float]]:
    """
    Extracts USD and EUR prices from text.
    If only one is found, calculates the other using configured EUR_USD_RATE.
    """
    usd_val: Optional[float] = None
    eur_val: Optional[float] = None

    if not text:
        return None, None

    for pattern in EUR_PRICE_PATTERNS:
        m = pattern.search(text)
        if m:
            try:
                eur_val = float(m.group(1).replace(",", "."))
                break
            except ValueError:
                pass

    for pattern in PRICE_PATTERNS:
        m = pattern.search(text)
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
    """Extracts single coupon or promo code from a product deal post."""
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
    """Checks if the post mentions points or coins discount."""
    if not text:
        return False
    for pattern in POINTS_PATTERNS:
        if pattern.search(text):
            return True
    return False

def extract_clean_title(text: str) -> Optional[str]:
    """
    Extracts clean product title from message text, stripping competitor channel watermarks,
    bot links, and instructions.
    """
    if not text:
        return None

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return None

    # Ignore lines that are competitor plugs or bot mentions
    filtered_lines = []
    for l in lines:
        l_lower = l.lower()
        if any(ign in l_lower for l in [
            "t.me/", "youtube.com", "youtu.be", "قناتنا", "البوت", "تحويل دولة", "طريقة حجز",
            "سعر تخفيض", "سعر العملات", "السعر", "الرابط", "رابط العملات"
        ]):
            continue
        filtered_lines.append(l)

    # 1. Look for explicit title prefix lines like "تخفيض لـ X"
    for line in lines:
        m = re.search(r'(?:تخفيض لـ[ــ]*|عرض لـ[ــ]*|خصم لـ[ــ]*|تخفيض الآن لـ?)\s*[:：\-]?\s*(.+)', line)
        if m:
            title = m.group(1).strip()
            title = re.sub(r'[\$€].*$', '', title).strip()
            title = re.sub(r'https?://\S+', '', title).strip()
            if len(title) > 3:
                return title[:120]

    # 2. Check filtered lines
    for line in filtered_lines:
        clean = re.sub(r'^[❗️🔖📌🔥🚨⚡💥✨📦🛒🎁📢✅💎💰🔻\s\-:]+', '', line).strip()
        clean = re.sub(r'https?://\S+', '', clean).strip()
        clean = re.sub(r'[\$€].*$', '', clean).strip()
        if len(clean) >= 5 and not any(k in clean for k in ["السعر", "رابط", "كوبون"]):
            return clean[:120]

    return None
