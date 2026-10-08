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
    extract_seller_coupon,
    detect_points_discount,
    extract_country_instruction,
    extract_clean_title,
    is_spam_or_non_deal,
    extract_coupon_list,
    detect_deal_type,
    compute_title_compatibility
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
    seller_coupon: Optional[str] = None
    has_points_discount: bool = False
    image_url: Optional[str] = None
    is_valid: bool = False
    raw_text: str = ""
    country_info: Optional[str] = None
    is_coupon_list: bool = False
    coupon_list: List[Dict[str, str]] = field(default_factory=list)
    final_url: Optional[str] = None
    deal_type: str = "coin"


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
        ali_urls = [u for u in urls if is_aliexpress_url(u) or is_potential_shortener(u)]
        if not ali_urls:
            return None

        # Prioritize URLs that are labeled "مباشر" or "direct" in source text
        def _url_priority(u: str) -> int:
            idx = text.find(u)
            if idx > 0:
                prefix = text[max(0, idx - 45):idx].lower()
                if any(k in prefix for k in ["مباشر", "direct", "رابط مباشر", "عادي"]):
                    return 0
            return 1

        ali_urls.sort(key=_url_priority)

        # Check if this is a Full Coupon List bulletin (must have 3+ coupons and NO single product price)
        coupon_items = extract_coupon_list(text)
        usd_price, eur_price = extract_prices(text)

        if len(coupon_items) >= 3 and usd_price is None and ali_urls:
            ali_url = ali_urls[0]
            resolved = await self.resolver.resolve(ali_url)
            import hashlib
            codes_sig = ",".join(sorted(c["code"] for c in coupon_items))
            coupon_hash = hashlib.sha256(codes_sig.encode()).hexdigest()[:12]

            # Clean URL: strip all tracking query parameters to ensure clean, short affiliate links
            raw_target = resolved.canonical_url or ali_url
            clean_campaign_url = raw_target.split("?")[0] if ("aliexpress.com" in raw_target and not resolved.product_id) else raw_target

            return ExtractedProduct(
                product_id=f"COUPONS_{coupon_hash}",
                original_url=ali_url,
                canonical_url=clean_campaign_url,
                title="أحدث كوبونات وتخفيضات AliExpress",
                current_price=None,
                current_price_eur=None,
                coupon_code=None,
                has_points_discount=False,
                image_url=None,
                is_valid=True,
                raw_text=text,
                country_info=None,
                is_coupon_list=True,
                coupon_list=coupon_items
            )

        # 3. Extract single deal fields from text first
        title = extract_clean_title(text)

        # 4. Resolve candidate URLs and find the best matching product
        api = None
        if settings.ALIEXPRESS_AFFILIATE_APP_KEY and settings.ALIEXPRESS_AFFILIATE_APP_SECRET:
            try:
                from aliexpress_api import AliexpressApi, models
                api = AliexpressApi(
                    settings.ALIEXPRESS_AFFILIATE_APP_KEY,
                    settings.ALIEXPRESS_AFFILIATE_APP_SECRET,
                    models.Language.EN,
                    models.Currency.USD,
                    settings.ALIEXPRESS_AFFILIATE_TRACKING_ID or "default"
                )
            except Exception as e:
                logger.debug(f"AliExpress API client init skipped: {e}")

        best_cand = None
        best_cand_score = -1.0

        for cand_url in ali_urls:
            res = await self.resolver.resolve(cand_url)
            if not res.is_valid or not res.product_id:
                continue

            cand_api_title = None
            cand_image_url = None
            prod_info = None

            if api:
                for attempt in range(2):
                    try:
                        details = await asyncio.wait_for(
                            asyncio.to_thread(api.get_products_details, [res.product_id]),
                            timeout=5.0
                        )
                        if details and len(details) > 0:
                            prod_info = details[0]
                            cand_image_url = getattr(prod_info, 'product_main_image_url', None)
                            cand_api_title = getattr(prod_info, 'product_title', None)
                        break
                    except Exception as err:
                        logger.debug(f"API details fetch for {res.product_id} attempt {attempt+1}/2: {err}")
                        if attempt < 1:
                            await asyncio.sleep(1.0)

            # Compute compatibility score between post title and API title
            score = compute_title_compatibility(title or "", cand_api_title or "")
            if score > best_cand_score:
                best_cand_score = score
                best_cand = (cand_url, res, prod_info, cand_api_title, cand_image_url)

            # High confidence match (score >= 0.3): use immediately
            if score >= 0.3:
                break

        if not best_cand:
            return None

        ali_url, resolved, prod_info, api_title, image_url = best_cand

        # CRITICAL SANITY CHECK: If the message text has a specific deal title (e.g. ATTACK SHARK headset),
        # but the resolved product title has ZERO keyword/category overlap (e.g. POCO smartphone),
        # reject the deal to prevent mismatched/frankenstein posts!
        if api_title and best_cand_score == 0.0 and title:
            clean_tokens = [w for w in re.findall(r'[a-zA-Z0-9\u0600-\u06FF]{3,}', title.lower()) if w not in {"deal", "aliexpress", "sale", "global", "version", "original", "تخفيض", "سعر", "ممتاز", "عرض"}]
            if len(clean_tokens) >= 2:
                logger.warning(f"Rejecting contaminated deal: post title '{title}' completely conflicts with resolved product '{api_title}' (score: 0.0).")
                return None

        # Clean official title and update if needed
        if api_title:
            clean_api_title = self._clean_official_title(api_title)
            if not title or len(title) < 15 or self._is_suspicious_title(title):
                title = clean_api_title

        coupon_code = extract_coupon(text)
        seller_coupon = extract_seller_coupon(text)
        has_points = detect_points_discount(text)
        combined_deal_url = f"{ali_url or ''} {resolved.final_url or ''} {resolved.canonical_url or ''}"
        country_info = extract_country_instruction(text, url=combined_deal_url, title=title or "")
        deal_type = detect_deal_type(text, combined_deal_url)

        # Fallback to direct AliExpress studio image or page metadata if image still missing
        if not image_url and resolved.product_id:
            image_url = await self._fetch_clean_aliexpress_image(resolved.product_id)

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

        # NEVER fall back to competitor media_path for product deals to prevent competitor logos / watermarks!
        is_valid = bool(resolved.product_id and (usd_price or eur_price) and title and image_url)

        return ExtractedProduct(
            product_id=resolved.product_id,
            original_url=ali_url,
            canonical_url=resolved.canonical_url,
            title=title or "منتج مميز من AliExpress",
            current_price=usd_price,
            current_price_eur=eur_price,
            coupon_code=coupon_code,
            seller_coupon=seller_coupon,
            has_points_discount=has_points,
            image_url=image_url,
            is_valid=is_valid,
            raw_text=text,
            country_info=country_info,
            is_coupon_list=False,
            coupon_list=[],
            final_url=resolved.final_url,
            deal_type=deal_type
        )

    async def _fetch_page_metadata(self, url: str) -> dict:
        meta = {}
        urls_to_try = []
        if "/item/" in url:
            pid_m = re.search(r'/item/(\d+)\.html', url)
            if pid_m:
                urls_to_try.append(f"https://ar.aliexpress.com/item/{pid_m.group(1)}.html")
        urls_to_try.append(url)

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        }
        try:
            async with httpx.AsyncClient(timeout=6.0, follow_redirects=True, verify=False) as client:
                for target_url in urls_to_try:
                    try:
                        res = await client.get(target_url, headers=headers)
                        if res.status_code == 200:
                            soup = BeautifulSoup(res.text, "html.parser")
                            og_title = soup.find("meta", property="og:title")
                            if og_title and og_title.get("content"):
                                meta["title"] = og_title["content"].strip()

                            og_img = soup.find("meta", property="og:image")
                            if og_img and og_img.get("content"):
                                meta["image"] = og_img["content"].strip()

                            if meta.get("image") or meta.get("title"):
                                return meta
                    except Exception:
                        continue
        except Exception as e:
            logger.debug(f"Metadata fetch skipped for {url}: {e}")
        return meta

    async def _fetch_clean_aliexpress_image(self, pid: str) -> Optional[str]:
        """Fetches the official clean AliExpress studio image directly without any competitor watermarks."""
        if not pid:
            return None
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }
        # ar.aliexpress.com resolves fast and reliably without gatewayAdapt hang
        urls = [
            f"https://ar.aliexpress.com/item/{pid}.html",
            f"https://www.aliexpress.com/item/{pid}.html",
        ]
        try:
            async with httpx.AsyncClient(headers=headers, follow_redirects=True, timeout=5.0) as client:
                for url in urls:
                    try:
                        res = await client.get(url)
                        if res.status_code == 200:
                            text = res.text
                            soup = BeautifulSoup(text, "html.parser")
                            og_img = soup.find("meta", property="og:image")
                            if og_img and og_img.get("content") and "aliexpress" in og_img["content"]:
                                return og_img["content"].strip()
                            m = re.search(r'https://ae-pic-a1\.aliexpress-media\.com/kf/[A-Za-z0-9_]+\.(?:jpg|png)', text)
                            if m:
                                return m.group(0)
                            m2 = re.search(r'https://ae01\.alicdn\.com/kf/[A-Za-z0-9_]+\.(?:jpg|png)', text)
                            if m2:
                                return m2.group(0)
                    except Exception:
                        continue
        except Exception as e:
            logger.debug(f"Direct clean image fetch skipped for {pid}: {e}")
        return None

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
