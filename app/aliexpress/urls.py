import re
from typing import List, Optional, Tuple
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode

ALIEXPRESS_DOMAINS = [
    "aliexpress.com",
    "aliexpress.ru",
    "a.aliexpress.com",
    "s.click.aliexpress.com",
    "click.aliexpress.com",
    "alitems.com",
    "alitems.site",
]

COMMON_SHORTENERS = [
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "cutt.ly",
    "rb.gy",
    "is.gd",
    "buff.ly",
]

# Regex for URLs in text (matches full https:// or bare domains like s.click.aliexpress.com/...)
URL_REGEX = re.compile(
    r'(https?://[^\s<>"\',;]+|(?:[a-zA-Z0-9_\-]+\.)*(?:aliexpress\.com|alitems\.com|alitems\.site|bit\.ly|tinyurl\.com|t\.co|cutt\.ly|rb\.gy|is\.gd|buff\.ly)/[^\s<>"\',;]+)',
    re.IGNORECASE
)

# Product ID regex patterns (strictly 10 to 18 digits)
ITEM_HTML_PATTERN = re.compile(r'/item/(\d{10,18})\.html', re.IGNORECASE)
ITEM_ID_PATTERN = re.compile(r'/item/(\d{10,18})', re.IGNORECASE)

def extract_all_urls(text: str) -> List[str]:
    """Extracts all HTTP/HTTPS URLs and bare AliExpress/shortener links from raw text."""
    if not text:
        return []
    urls = URL_REGEX.findall(text)
    cleaned_urls = []
    for u in urls:
        # Strip trailing non-ASCII characters touching URLs (Arabic, emojis, etc. e.g. _c4LARstxكوبون)
        cleaned = re.sub(r'[^\x21-\x7E].*$', '', u)
        cleaned = cleaned.rstrip('.,;!?:)]}"\'>')
        if not cleaned.startswith("http://") and not cleaned.startswith("https://"):
            cleaned = "https://" + cleaned
        if cleaned not in cleaned_urls:
            cleaned_urls.append(cleaned)
    return cleaned_urls

def is_aliexpress_url(url: str) -> bool:
    """Checks if a URL belongs to AliExpress or known AliExpress affiliate domains."""
    try:
        parsed = urlparse(url)
        hostname = (parsed.hostname or "").lower()
        for domain in ALIEXPRESS_DOMAINS:
            if hostname == domain or hostname.endswith("." + domain):
                return True
        return False
    except Exception:
        return False

def is_potential_shortener(url: str) -> bool:
    """Checks if a URL is from a known URL shortener."""
    try:
        parsed = urlparse(url)
        hostname = (parsed.hostname or "").lower()
        for s in COMMON_SHORTENERS:
            if hostname == s or hostname.endswith("." + s):
                return True
        return False
    except Exception:
        return False

def extract_product_id_from_url(url: str) -> Optional[str]:
    """
    Extracts numerical product ID from various AliExpress URL formats.
    e.g. https://www.aliexpress.com/item/1005006382910245.html -> 1005006382910245
    Strictly validates that the extracted ID is between 10 and 18 digits.
    """
    if not url:
        return None

    clean = url.strip()
    if clean.isdigit() and 10 <= len(clean) <= 18:
        return clean

    # Check /item/{id}.html
    m = ITEM_HTML_PATTERN.search(url)
    if m:
        return m.group(1)

    # Check /item/{id}
    m = ITEM_ID_PATTERN.search(url)
    if m:
        return m.group(1)

    # Check query parameters (productId, id, itemId)
    try:
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        for key in ["productIds", "productId", "product_id", "itemId", "item_id", "productIdList", "id"]:
            if key in qs and qs[key]:
                val = qs[key][0].split(',')[0].strip()
                if val.isdigit() and 10 <= len(val) <= 18:
                    return val

        # Strict regex for pure id=, not terminal_id or sceneId
        m = re.search(r'(?:^|[?&#;])(?:productIds?|itemId|id)=(\d{10,18})(?:$|[&#;])', url, re.IGNORECASE)
        if m:
            return m.group(1)
    except Exception:
        pass

    return None


def normalize_aliexpress_url(url: str, product_id: Optional[str] = None) -> str:
    """
    Returns a clean canonical product URL without noisy tracking parameters.
    If product_id is known, generates the standard canonical format:
    https://www.aliexpress.com/item/{product_id}.html
    """
    pid = product_id or extract_product_id_from_url(url)
    if pid:
        return f"https://www.aliexpress.com/item/{pid}.html"

    # Otherwise strip typical tracking query parameters
    try:
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        params_to_remove = {
            "spm", "scm", "algo_pvid", "algo_exp_id", "pdp_npi", "btsid",
            "ws_ab_test", "aff_fcid", "aff_fsk", "aff_platform", "sk",
            "terminal_id", "spreadType", "srcSns", "biz_type", "spread_code"
        }
        filtered_qs = {k: v for k, v in qs.items() if k not in params_to_remove}
        clean_query = urlencode(filtered_qs, doseq=True)

        return urlunparse((
            parsed.scheme or "https",
            parsed.netloc,
            parsed.path,
            parsed.params,
            clean_query,
            ""  # Strip fragment
        ))
    except Exception:
        return url


COMPETITOR_CHANNELS = [
    "ecksdeal", "lodydeals", "zedstoreonline", "aniscoupons", "pcgamingpart",
    "bnddeals", "megaprix", "megaphonna", "coupon4dz", "francecp", "alifrdrop",
    "couponsglobal", "anishays", "ecks", "esk"
]

COMPETITOR_SHORTCODES = [
    "_c38iyTZR",
]

def check_competitor_contamination(caption: str = "", url: str = "") -> Tuple[bool, Optional[str]]:
    """
    STRICT SECURITY RULE:
    Checks if a caption, post text, or affiliate URL is contaminated with any
    competitor channel handle, competitor shortcode, competitor t.me link, or unauthorized bot.
    Returns (is_contaminated: bool, reason: Optional[str]).
    """
    combined = f"{caption or ''} {url or ''}".lower()

    # 1. Competitor shortcodes / links
    for code in COMPETITOR_SHORTCODES:
        if code.lower() in combined:
            return True, f"Competitor affiliate shortcode detected: {code}"

    # 2. Competitor Telegram channels / handles (@channel or t.me/channel)
    for ch in COMPETITOR_CHANNELS:
        if f"@{ch}" in combined or f"t.me/{ch}" in combined or "t.me/joinchat/" in combined:
            return True, f"Competitor channel handle or link detected: {ch}"

    # 3. Unauthorized bots (only @Alilo07BOT is authorized)
    bot_matches = re.findall(r'@([a-zA-Z0-9_]{3,35}bot)\b', combined, re.IGNORECASE)
    for b in bot_matches:
        if b.lower() != "alilo07bot":
            return True, f"Unauthorized external bot detected: @{b}"

    # 4. Check for unauthorized aff_fcid in AliExpress URLs
    if "aff_fcid=" in combined:
        from app.config.settings import settings
        our_tracking = (getattr(settings, "ALIEXPRESS_AFFILIATE_TRACKING_ID", "") or "dzkhvled16").lower()
        m_fcid = re.search(r'aff_fcid=([a-zA-Z0-9_\-]+)', combined)
        if m_fcid and m_fcid.group(1).lower() != our_tracking:
            return True, f"Competitor aff_fcid tracking ID detected: {m_fcid.group(1)}"

    return False, None


def strip_competitor_elements(text: str) -> str:
    """
    Strips competitor channel handles, t.me links, and unauthorized bot links from text.
    """
    if not text:
        return ""
    cleaned = text
    # Strip known competitor handles and links
    for ch in COMPETITOR_CHANNELS:
        cleaned = re.sub(rf'@?https?://t\.me/{ch}\S*', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(rf't\.me/{ch}\S*', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(rf'@{ch}\b', '', cleaned, flags=re.IGNORECASE)

    # Strip unauthorized bots
    for b_match in re.finditer(r'@([a-zA-Z0-9_]{3,35}bot)\b', cleaned, re.IGNORECASE):
        bot_name = b_match.group(1)
        if bot_name.lower() != "alilo07bot":
            cleaned = cleaned.replace(b_match.group(0), '')

    return cleaned.strip()

