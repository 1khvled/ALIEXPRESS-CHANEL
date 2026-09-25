import re
from typing import List, Optional
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

# Regex for URLs in text
URL_REGEX = re.compile(
    r'(https?://[^\s<>"\',;]+)',
    re.IGNORECASE
)

# Product ID regex patterns
ITEM_HTML_PATTERN = re.compile(r'/item/(\d+)\.html', re.IGNORECASE)
ITEM_ID_PATTERN = re.compile(r'/item/(\d+)', re.IGNORECASE)

def extract_all_urls(text: str) -> List[str]:
    """Extracts all HTTP/HTTPS URLs from raw text."""
    if not text:
        return []
    urls = URL_REGEX.findall(text)
    # Clean trailing punctuation often attached to URLs in text
    cleaned_urls = []
    for u in urls:
        cleaned = u.rstrip(".,;!?:)]}\"'>")
        if cleaned.startswith("http://") or cleaned.startswith("https://"):
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
    """
    if not url:
        return None

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
        for key in ["productIds", "productId", "product_id", "id", "itemId", "item_id", "productIdList"]:
            if key in qs and qs[key]:
                val = qs[key][0].split(',')[0].strip()
                if val.isdigit():
                    return val
        # Also check regex for productIds=100500... in raw string if query parsing missed it
        m = re.search(r'productIds?=(\d+)', url, re.IGNORECASE)
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
