import re
from dataclasses import dataclass
from typing import Optional
import httpx
from bs4 import BeautifulSoup
from app.aliexpress.urls import extract_all_urls, is_aliexpress_url, is_potential_shortener
from app.aliexpress.resolver import url_resolver
from app.aliexpress.parser import (
    extract_prices,
    extract_coupon,
    detect_points_discount,
    extract_clean_title
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

class ProductExtractor:
    def __init__(self):
        self.resolver = url_resolver

    async def extract_from_message(
        self,
        text: str,
        media_path: Optional[str] = None
    ) -> Optional[ExtractedProduct]:
        """
        Parses a Telegram message to find AliExpress URLs and extract deal information.
        Returns None if no AliExpress link or valid shortlink is found.
        """
        if not text:
            return None

        # 1. Find all URLs
        urls = extract_all_urls(text)
        ali_url = None

        for u in urls:
            if is_aliexpress_url(u) or is_potential_shortener(u):
                ali_url = u
                break

        if not ali_url:
            return None

        # 2. Resolve URL
        resolved = await self.resolver.resolve(ali_url)
        if not resolved.is_valid:
            logger.info(f"Could not validate AliExpress link: {ali_url}")
            return None

        # 3. Extract deal fields from text
        usd_price, eur_price = extract_prices(text)
        coupon_code = extract_coupon(text)
        has_points = detect_points_discount(text)
        title = extract_clean_title(text)

        # 4. If title or image not in text, try product page metadata
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
            raw_text=text
        )

    async def _fetch_page_metadata(self, url: str) -> dict:
        """Fetches OpenGraph title and image from the product page when needed."""
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
