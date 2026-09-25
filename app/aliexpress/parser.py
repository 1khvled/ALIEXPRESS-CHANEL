import re
from dataclasses import dataclass
from typing import Optional, Tuple
from app.config.settings import settings

# Regex patterns for price detection
PRICE_PATTERNS = [
    # $29.99 or $ 29.99 or 29.99$ or 29,99$
    re.compile(r'\$\s*([0-9]+(?:[\.,][0-9]{1,2})?)', re.IGNORECASE),
    re.compile(r'([0-9]+(?:[\.,][0-9]{1,2})?)\s*\$', re.IGNORECASE),
    # 29.99 USD or USD 29.99
    re.compile(r'([0-9]+(?:[\.,][0-9]{1,2})?)\s*USD', re.IGNORECASE),
    re.compile(r'USD\s*([0-9]+(?:[\.,][0-9]{1,2})?)', re.IGNORECASE),
    # السعر : 20.12 or السعر: 20.12
    re.compile(r'السعر\s*[:：]\s*([0-9]+(?:[\.,][0-9]{1,2})?)', re.IGNORECASE),
]

EUR_PRICE_PATTERNS = [
    re.compile(r'([0-9]+(?:[\.,][0-9]{1,2})?)\s*€', re.IGNORECASE),
    re.compile(r'€\s*([0-9]+(?:[\.,][0-9]{1,2})?)', re.IGNORECASE),
    re.compile(r'([0-9]+(?:[\.,][0-9]{1,2})?)\s*EUR', re.IGNORECASE),
]

# Patterns for coupon code
COUPON_PATTERNS = [
    re.compile(r'(?:كوبون|كود|code|coupon)\s*[:：\-]\s*([A-Za-z0-9_-]{3,25})', re.IGNORECASE),
    re.compile(r'🎟️?\s*(?:كوبون|كود|code|coupon)\s*[:：\-]?\s*([A-Za-z0-9_-]{3,25})', re.IGNORECASE),
    re.compile(r'(?:استخدم كود|استعمل كود)\s*([A-Za-z0-9_-]{3,25})', re.IGNORECASE),
]

# Points discount patterns
POINTS_PATTERNS = [
    re.compile(r'خصم\s*(?:النقاط|نقاط|العملات)', re.IGNORECASE),
    re.compile(r'نقاط\s*علي\s*إكسبريس', re.IGNORECASE),
    re.compile(r'coins\s*discount', re.IGNORECASE),
]

def extract_prices(text: str) -> Tuple[Optional[float], Optional[float]]:
    """
    Extracts USD and EUR prices from text.
    If only one is found, calculates the other using configured EUR_USD_RATE.
    """
    usd_val: Optional[float] = None
    eur_val: Optional[float] = None

    if not text:
        return None, None

    # Check EUR pattern
    for pattern in EUR_PRICE_PATTERNS:
        m = pattern.search(text)
        if m:
            try:
                eur_val = float(m.group(1).replace(",", "."))
                break
            except ValueError:
                pass

    # Check USD / standard patterns
    for pattern in PRICE_PATTERNS:
        m = pattern.search(text)
        if m:
            try:
                candidate = float(m.group(1).replace(",", "."))
                # Skip zero or unreasonable numbers
                if 0.1 <= candidate <= 10000:
                    usd_val = candidate
                    break
            except ValueError:
                pass

    # Rate conversion if one is missing
    rate = settings.EUR_USD_RATE or 0.92
    if usd_val is not None and eur_val is None:
        eur_val = round(usd_val * rate, 2)
    elif eur_val is not None and usd_val is None:
        usd_val = round(eur_val / rate, 2)

    return usd_val, eur_val

def extract_coupon(text: str) -> Optional[str]:
    """Extracts coupon or discount promo code from text."""
    if not text:
        return None
    for pattern in COUPON_PATTERNS:
        m = pattern.search(text)
        if m:
            code = m.group(1).strip()
            # Exclude false positives like "http", "https", "aliexpress"
            if code.lower() not in {"http", "https", "aliexpress", "item", "link", "url"}:
                return code
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
    Extracts product title from message text.
    Usually the first line or line after emoji like 🔥 or تخفيض لـ.
    """
    if not text:
        return None

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return None

    # Check for prefix lines like "تخفيض لـ X" or "عرض لـ X"
    for line in lines:
        m = re.search(r'(?:تخفيض لـ|عرض لـ|عرض خاص لـ|خصم لـ)\s*(.+)', line)
        if m:
            title = m.group(1).strip()
            title = re.sub(r'[\$€].*$', '', title).strip()
            if len(title) > 3:
                return title

    # Fallback to the first non-empty line that doesn't start with URL
    first_line = lines[0]
    # Remove leading decorative emojis
    first_line = re.sub(r'^[🔥🚨⚡💥✨📦🛒🎁📢\s\-:]+', '', first_line).strip()
    # Strip trailing price or link if mixed in line
    first_line = re.sub(r'https?://\S+', '', first_line).strip()
    first_line = re.sub(r'[\$€].*$', '', first_line).strip()

    if len(first_line) > 3:
        return first_line[:120]

    return None
