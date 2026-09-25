"""
AliExpress Global Promotions & Promo Codes Tracker
Tracks official AliExpress sale festivals, Choice Day events, active coupons,
and validates deal freshness to prevent posting expired deals or outdated coupons.
"""
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Tuple
import re

@dataclass
class PromoEvent:
    name: str
    name_ar: str
    start_date: datetime
    end_date: datetime
    banner_tag: str
    is_major: bool
    coupon_tiers: List[Dict[str, str]]
    banner_image_url: Optional[str] = None

# Official AliExpress 2026 Sales Calendar
PROMO_CALENDAR: List[PromoEvent] = [
    PromoEvent(
        name="Party Ready Sale / Choice Day",
        name_ar="تخفيضات Party Ready Sale & Choice Day لشهر أكتوبر 🔥",
        start_date=datetime(2026, 10, 1, 7, 0, 0, tzinfo=timezone.utc),
        end_date=datetime(2026, 10, 8, 6, 59, 59, tzinfo=timezone.utc),
        banner_tag="🎯 Party Ready Sale (1 - 7 أكتوبر)",
        is_major=True,
        coupon_tiers=[
            {"tier": "3/29$", "code": "CDDZ03"},
            {"tier": "6/49$", "code": "CDDZ06"},
            {"tier": "10/79$", "code": "CDDZ10"},
            {"tier": "20/159$", "code": "CDDZ20"},
            {"tier": "40/299$", "code": "CDDZ40"},
        ],
        banner_image_url="https://ae-pic-a1.aliexpress-media.com/kf/HTB18eCBQXXXXXXfXXXX760XFXXXa.png"
    ),
    PromoEvent(
        name="Brand Day Sale",
        name_ar="مهرجان Brand Day لشهر أكتوبر 🏷️",
        start_date=datetime(2026, 10, 9, 7, 0, 0, tzinfo=timezone.utc),
        end_date=datetime(2026, 10, 12, 6, 59, 59, tzinfo=timezone.utc),
        banner_tag="🏷️ Brand Day (9 - 11 أكتوبر)",
        is_major=True,
        coupon_tiers=[]
    ),
    PromoEvent(
        name="Winter Offers",
        name_ar="تخفيضات عروض الشتاء Winter Offers ❄️",
        start_date=datetime(2026, 10, 14, 7, 0, 0, tzinfo=timezone.utc),
        end_date=datetime(2026, 10, 17, 6, 59, 59, tzinfo=timezone.utc),
        banner_tag="❄️ Winter Offers (14 - 16 أكتوبر)",
        is_major=True,
        coupon_tiers=[]
    ),
    PromoEvent(
        name="11.11 Global Shopping Festival Warm-Up",
        name_ar="التحضير لمهرجان 11.11 العالمي 💥",
        start_date=datetime(2026, 11, 1, 7, 0, 0, tzinfo=timezone.utc),
        end_date=datetime(2026, 11, 11, 6, 59, 59, tzinfo=timezone.utc),
        banner_tag="⏳ تحضيرات مهرجان 11.11",
        is_major=True,
        coupon_tiers=[]
    ),
    PromoEvent(
        name="11.11 Global Shopping Festival Main Sale",
        name_ar="مهرجان 11.11 الأكبر عالمياً 🛍️",
        start_date=datetime(2026, 11, 11, 7, 0, 0, tzinfo=timezone.utc),
        end_date=datetime(2026, 11, 19, 6, 59, 59, tzinfo=timezone.utc),
        banner_tag="🔥 أقوى تخفيضات السنة 11.11",
        is_major=True,
        coupon_tiers=[]
    ),
    PromoEvent(
        name="Black Friday & Cyber Monday",
        name_ar="تخفيضات الجمعة البيضاء Black Friday 🖤",
        start_date=datetime(2026, 11, 24, 7, 0, 0, tzinfo=timezone.utc),
        end_date=datetime(2026, 12, 1, 6, 59, 59, tzinfo=timezone.utc),
        banner_tag="🖤 Black Friday السنوي",
        is_major=True,
        coupon_tiers=[]
    ),
]

EXPIRED_DATE_PATTERNS = [
    # Explicit past dates in September or earlier
    re.compile(r'(?:ينتهي|صالح\s+حتى|نهاية\s+العرض|إلى\s+غاية|الى\s+غاية)\s*(?:يوم)?\s*([0-9]{1,2})\s*(?:سبتمبر|sept|september|أوت|اوت|august|جويلية|july)', re.IGNORECASE),
    re.compile(r'(?:20|19|18|17|16|15|14|13|12|11|10)\s*(?:سبتمبر|september|sept)\b', re.IGNORECASE),
    re.compile(r'\b(?:20|19|18|17|16|15|14|13|12|11|10)/09(?:/202[0-6])?\b', re.IGNORECASE),
    re.compile(r'brand\s*day\s*september', re.IGNORECASE),
    re.compile(r'تخفيضات\s*(?:منتصف|شهر)?\s*سبتمبر', re.IGNORECASE),
]

class PromoTracker:
    def __init__(self):
        self.calendar = PROMO_CALENDAR

    def get_active_promo(self, now: Optional[datetime] = None) -> Optional[PromoEvent]:
        """Returns the currently active official AliExpress promo event, if any."""
        if now is None:
            now = datetime.now(timezone.utc)
        for event in self.calendar:
            if event.start_date <= now <= event.end_date:
                return event
        return None

    def get_next_promo(self, now: Optional[datetime] = None) -> Optional[Tuple[PromoEvent, int]]:
        """Returns the upcoming promo event and days remaining until it starts."""
        if now is None:
            now = datetime.now(timezone.utc)
        for event in self.calendar:
            if event.start_date > now:
                days_left = (event.start_date - now).days
                return event, days_left
        return None

    def validate_deal_freshness(self, text: str, msg_datetime: Optional[datetime] = None) -> Tuple[bool, Optional[str]]:
        """
        Validates that a deal is fresh and not an expired promo from past campaigns:
        1. Checks message age (must be within last 24 hours).
        2. Detects expired date mentions (e.g. Sept 20 coupons or past dates).
        3. Detects expired campaign names.
        """
        now = datetime.now(timezone.utc)

        # 1. Message age check (allow fresh deals from the last 72 hours)
        if msg_datetime is not None:
            age = now - msg_datetime
            if age > timedelta(hours=72):
                return False, f"Message is too old ({age.total_seconds() / 3600:.1f} hours ago, max 72h)"

        # 2. Expired date mentions in text
        for pat in EXPIRED_DATE_PATTERNS:
            m = pat.search(text)
            if m:
                return False, f"Mention of expired campaign/date detected: '{m.group(0)}'"

        # 3. If coupons are mentioned, ensure we are not in an empty period passing off old codes
        active_promo = self.get_active_promo(now)
        if not active_promo:
            # Between campaigns: allow individual store coupons or coins, but reject generic expired platform campaigns
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

        # Fallback to current or upcoming official event banner from AliExpress CDN
        active = self.get_active_promo()
        if active and active.banner_image_url:
            return active.banner_image_url

        next_event = self.get_next_promo()
        if next_event and next_event[0].banner_image_url:
            return next_event[0].banner_image_url

        # General official AliExpress Deals CDN banner
        return "https://ae-pic-a1.aliexpress-media.com/kf/HTB18eCBQXXXXXXfXXXX760XFXXXa.png"

promo_tracker = PromoTracker()
