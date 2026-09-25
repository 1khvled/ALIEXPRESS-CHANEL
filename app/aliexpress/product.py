import re
from dataclasses import dataclass, field
from typing import Optional, List, Dict
import httpx
from bs4 import BeautifulSoup
from app.aliexpress.urls import extract_all_urls, is_aliexpress_url, is_potential_shortener
from app.aliexpress.resolver import url_resolver
from app.aliexpress.parser import (
    extract_prices,
    extract_coupon,
    detect_points_discount,
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

        # Check if this is a Full Coupon List bulletin
        coupon_items = extract_coupon_list(text)
        if len(coupon_items) >= 2 and ali_url:
            resolved = await self.resolver.resolve(ali_url)
            import hashlib
            codes_sig = ",".join(sorted(c["code"] for c in coupon_items))
            coupon_hash = hashlib.sha256(codes_sig.encode()).hexdigest()[:12]

            return ExtractedProduct(
                product_id=f"COUPONS_{coupon_hash}",
                original_url=ali_url,
                canonical_url=resolved.canonical_url or ali_url,
                title="أحدث كوبونات وتخفيضات AliExpress",
                current_price=None,
                current_price_eur=None,
                coupon_code=None,
                has_points_discount=False,
                image_url=None,
                is_valid=True,
                raw_text=text,
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
        usd_price, eur_price = extract_prices(text)
        coupon_code = extract_coupon(text)
        has_points = detect_points_discount(text)
        title = extract_clean_title(text)

        # 5. Fetch page metadata if needed
        image_url = None
        if not title or not image_url:
            page_meta = await self._fetch_page_metadata(resolved.canonical_url)
            if not title and page_meta.get("title"):
                title = page_meta["title"]
            if page_meta.get("image"):
                image_url = page_meta["image"]

        is_valid = bool(resolved.product_id and (usd_price or eur_price or title))

        return ExtractedProduct(
            product_id=resolved.product_id,
            original_url=ali_url,
            canonical_url=resolved.canonical_url,
            title=title or "AliExpress Deal",
            current_price=usd_price,
            current_price_eur=eur_price,
            coupon_code=coupon_code,
            has_points_discount=has_points,
            image_url=image_url,
            is_valid=is_valid,
            raw_text=text,
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

product_extractor = ProductExtractor()
