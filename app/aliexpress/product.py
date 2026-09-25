import asyncio
import re
from dataclasses import dataclass, field
from typing import Optional, List, Dict
import httpx
from bs4 import BeautifulSoup
from app.config.settings import settings
from app.aliexpress.urls import extract_all_urls, is_aliexpress_url, is_potential_shortener
from app.aliexpress.resolver import url_resolver
from app.aliexpress.parser import (
    extract_prices,
    extract_coupon,
    detect_points_discount,
    extract_country_instruction,
    extract_clean_title,
    is_spam_or_non_deal,
    extract_coupon_list
)
from app.utils.logger import logger

@dataclass
class ExtractedProduct:
    product_id: Optional[str]
    original_url: str
    canonical_url: str
    title: Optional[str]
    current_price: Optional[float]
    current_price_eur: Optional[float]
    coupon_code: Optional[str]
    has_points_discount: bool
    image_url: Optional[str]
    is_valid: bool
    raw_text: str
    country_info: Optional[str] = None
    is_coupon_list: bool = False
    coupon_list: List[Dict[str, str]] = field(default_factory=list)

class ProductExtractor:
    def __init__(self):
        self.resolver = url_resolver

    async def extract_from_message(
        self,
        text: str,
        media_path: Optional[str] = None
    ) -> Optional[ExtractedProduct]:
        """
        Parses a Telegram message from source channels.
        Smartly filters out non-deal spam, extracts single AliExpress deals or full coupon lists.
        """
        if not text:
            return None

        # 1. Smart spam & non-deal filtering
        is_spam, reason = is_spam_or_non_deal(text)
        if is_spam:
            logger.debug(f"Filtered non-deal message: {reason}")
            return None

        # 2. Find AliExpress URL(s)
        urls = extract_all_urls(text)
        ali_url = None
        for u in urls:
            if is_aliexpress_url(u) or is_potential_shortener(u):
                ali_url = u
                break

        # Check if this is a Full Coupon List bulletin (must have 3+ coupons and NO single product price)
        coupon_items = extract_coupon_list(text)
        usd_price, eur_price = extract_prices(text)

        if len(coupon_items) >= 3 and usd_price is None and ali_url:
            resolved = await self.resolver.resolve(ali_url)
            import hashlib
            codes_sig = ",".join(sorted(c["code"] for c in coupon_items))
            coupon_hash = hashlib.sha256(codes_sig.encode()).hexdigest()[:12]

            # Scrape official AliExpress promo banner image from campaign landing page / CDN
            from app.aliexpress.promos import promo_tracker
            promo_banner = await promo_tracker.scrape_aliexpress_promo_banner(resolved.canonical_url or ali_url)

            return ExtractedProduct(
                product_id=f"COUPONS_{coupon_hash}",
                original_url=ali_url,
                canonical_url=resolved.canonical_url or ali_url,
                title="أحدث كوبونات وتخفيضات AliExpress",
                current_price=None,
                current_price_eur=None,
                coupon_code=None,
                has_points_discount=False,
                image_url=promo_banner,
                is_valid=True,
                raw_text=text,
                country_info=None,
                is_coupon_list=True,
                coupon_list=coupon_items
            )

        if not ali_url:
            return None

        # 3. Resolve single deal URL
        resolved = await self.resolver.resolve(ali_url)
        if not resolved.is_valid:
            logger.info(f"Could not validate AliExpress link: {ali_url}")
            return None

        # 4. Extract single deal fields
        coupon_code = extract_coupon(text)
        has_points = detect_points_discount(text)
        title = extract_clean_title(text)
        country_info = extract_country_instruction(text, url=ali_url or "", title=title or "")

        # 5. Fetch official HD studio image & details via AliExpress Open Platform API
        image_url = None
        if resolved.product_id and settings.ALIEXPRESS_AFFILIATE_APP_KEY and settings.ALIEXPRESS_AFFILIATE_APP_SECRET:
            try:
                from aliexpress_api import AliexpressApi, models
                api = AliexpressApi(
                    settings.ALIEXPRESS_AFFILIATE_APP_KEY,
                    settings.ALIEXPRESS_AFFILIATE_APP_SECRET,
                    models.Language.EN,
                    models.Currency.USD,
                    settings.ALIEXPRESS_AFFILIATE_TRACKING_ID or "default"
                )
                details = None
                for attempt in range(3):
                    try:
                        details = await asyncio.to_thread(api.get_products_details, [resolved.product_id])
                        break
                    except Exception as err:
                        if "ApiCallLimit" in str(err) or "frequency exceeds" in str(err) or "exceeds" in str(err):
                            await asyncio.sleep(1.5)
                        else:
                            logger.debug(f"API details error on attempt {attempt+1}: {err}")
                            break

                if details and len(details) > 0:
                    prod_info = details[0]
                    if getattr(prod_info, 'product_main_image_url', None):
                        image_url = prod_info.product_main_image_url
                    api_title = getattr(prod_info, 'product_title', None)
                    if api_title:
                        clean_api_title = self._clean_official_title(api_title)
                        # Replace title if current title is missing, too short, or suspicious description
                        if not title or len(title) < 15 or self._is_suspicious_title(title):
                            title = clean_api_title
            except Exception as e:
                logger.debug(f"API product details fetch skipped: {e}")

        # Fallback to page metadata if image/title still missing
        if not image_url or not title or len(title) < 10 or self._is_suspicious_title(title):
            page_meta = (await self._fetch_page_metadata(resolved.canonical_url)) or {}
            if not title or len(title) < 10 or self._is_suspicious_title(title):
                if page_meta.get("title"):
                    meta_t = page_meta["title"]
                    meta_t = re.sub(r'(\s*-\s*AliExpress.*$|\s*\|\s*AliExpress.*$)', '', meta_t).strip()
                    if len(meta_t) >= 4:
                        title = self._clean_official_title(meta_t)
            if not image_url and page_meta.get("image"):
                image_url = page_meta["image"]

        is_valid = bool(resolved.product_id and (usd_price or eur_price) and title and image_url)

        return ExtractedProduct(
            product_id=resolved.product_id,
            original_url=ali_url,
            canonical_url=resolved.canonical_url,
            title=title or "منتج مميز من AliExpress",
            current_price=usd_price,
            current_price_eur=eur_price,
            coupon_code=coupon_code,
            has_points_discount=has_points,
            image_url=image_url,
            is_valid=is_valid,
            raw_text=text,
            country_info=country_info,
            is_coupon_list=False,
            coupon_list=[]
        )

    async def _fetch_page_metadata(self, url: str) -> dict:
        meta = {}
        try:
            async with httpx.AsyncClient(timeout=8.0, follow_redirects=True, verify=False) as client:
                res = await client.get(
                    url,
                    headers={
                        "User-Agent": (
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/124.0.0.0 Safari/537.36"
                        )
                    }
                )
                if res.status_code == 200:
                    soup = BeautifulSoup(res.text, "html.parser")
                    og_title = soup.find("meta", property="og:title")
                    if og_title and og_title.get("content"):
                        meta["title"] = og_title["content"].strip()

                    og_img = soup.find("meta", property="og:image")
                    if og_img and og_img.get("content"):
                        meta["image"] = og_img["content"].strip()
        except Exception as e:
            logger.debug(f"Metadata fetch skipped for {url}: {e}")
        return meta

    def _clean_official_title(self, raw_title: str) -> str:
        """Removes SEO junk words from AliExpress official catalog titles."""
        if not raw_title:
            return ""
        # Strip common AliExpress SEO fluff
        patterns_to_remove = [
            r'\b(?:original|global\s+version|wholesale|hot\s+sale|free\s+shipping|brand\s+new|top\s+quality)\b',
            r'\b(?:new\s+202[0-9]|202[0-9]\s+new|202[0-9])\b',
            r'\b(?:for\s+men|for\s+women|for\s+kids|for\s+adults)\b',
            r'\b(?:high\s+quality|drop\s+shipping|in\s+stock)\b',
            r'[\$€£].*$',
            r'[\(\[\{][^\)\]\}]*(?:shipping|original|version|sale)[^\)\]\}]*[\)\]\}]',
        ]
        cleaned = raw_title
        for pat in patterns_to_remove:
            cleaned = re.sub(pat, '', cleaned, flags=re.IGNORECASE)
        # Clean extra spaces and punctuation
        cleaned = re.sub(r'[\s\-|,/]{2,}', ' ', cleaned).strip(' -|,/')
        # Return first 75 characters if it's too long
        if len(cleaned) > 80:
            words = cleaned.split()
            result = []
            cur_len = 0
            for w in words:
                if cur_len + len(w) + 1 > 75:
                    break
                result.append(w)
                cur_len += len(w) + 1
            cleaned = ' '.join(result)
        return cleaned or raw_title[:75]

    def _is_suspicious_title(self, title: str) -> bool:
        """Detects if a title looks like a description, accessories list, or non-product phrase."""
        if not title:
            return True
        t_low = title.lower()
        # Words indicating package descriptions or accessories
        suspicious_words = [
            "يلحقك", "معاها", "يأتي مع", "معها", "ملحقات", "الهدايا",
            "محتويات", "العلبة", "بوشات", "كيتمان", "قلم كتابة", "انكسابل",
            "طريقة", "كيفية", "شرح", "تخفيض لـ", "تخفيض الآن", "عرض خاص",
            "جدول", "اكواد", "أكواد", "قسيمة البائع", "قسيمة", "كوبون"
        ]
        for w in suspicious_words:
            if w in t_low:
                return True
        # If it has 2+ slashes, it's an accessories list
        if title.count('/') >= 2 or title.count('+') >= 3:
            return True
        return False

product_extractor = ProductExtractor()
