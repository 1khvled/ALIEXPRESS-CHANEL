import asyncio
import re
from abc import ABC, abstractmethod
from typing import Optional
from urllib.parse import urlencode, quote
from app.config.settings import settings
from app.utils.logger import logger

class AffiliateProvider(ABC):
    @abstractmethod
    async def generate_link(self, product_url: str, product_id: Optional[str] = None, deal_type: str = "coin") -> str:
        """Takes a clean canonical product URL and returns an affiliate URL."""
        pass

class DirectAffiliateProvider(AffiliateProvider):
    """
    Direct AliExpress link with official affiliate tracking ID.
    Produces clean, direct aliexpress.com URLs with aff_fcid tracking parameter.
    For coin deals (90%+): returns coin index link.
    For bundle deals: returns Choice/bundle link with sourceType=562.
    """
    def __init__(self, tracking_id: Optional[str] = None):
        self.tracking_id = tracking_id or settings.ALIEXPRESS_AFFILIATE_TRACKING_ID or "dzkhvled16"

    async def generate_link(self, product_url: str, product_id: Optional[str] = None, deal_type: str = "coin") -> str:
        pid = product_id
        if not pid:
            m = re.search(r'/item/(\d+)\.html', product_url)
            if m:
                pid = m.group(1)
            else:
                m_pid = re.search(r'productIds?=(\d+)', product_url)
                if m_pid:
                    pid = m_pid.group(1)

        if pid:
            if deal_type == "bundle":
                return f"https://www.aliexpress.com/ssr/300000512/BundleDeals2?disableNav=YES&pha_manifest=ssr&_immersiveMode=true&productIds={pid}&aff_fcid={self.tracking_id}"
            elif deal_type == "super":
                return f"https://www.aliexpress.com/item/{pid}.html?sourceType=561&channel=superdeal&aff_fcid={self.tracking_id}"
            elif deal_type == "item":
                return f"https://www.aliexpress.com/item/{pid}.html?aff_fcid={self.tracking_id}"
            else:
                return f"https://m.aliexpress.com/p/coin-index/index.html?_immersiveMode=true&tabname=configTab_1926001&productIds={pid}&aff_fcid={self.tracking_id}"

        # Clean campaign URLs to strip noisy tracking parameters
        clean_url = product_url.split("?")[0] if ("aliexpress.com" in product_url and "?" in product_url) else product_url
        if deal_type == "bundle":
            return f"https://www.aliexpress.com/ssr/300000512/BundleDeals2?disableNav=YES&pha_manifest=ssr&_immersiveMode=true&aff_fcid={self.tracking_id}"
        elif deal_type == "super":
            return f"{clean_url}?sourceType=561&channel=superdeal&aff_fcid={self.tracking_id}"
        separator = "&" if "?" in clean_url else "?"
        return f"{clean_url}{separator}aff_fcid={self.tracking_id}"

class CustomNetworkAffiliateProvider(AffiliateProvider):
    def __init__(self, prefix: str):
        self.prefix = prefix

    async def generate_link(self, product_url: str, product_id: Optional[str] = None, deal_type: str = "coin") -> str:
        if not self.prefix:
            return product_url
        sep = "&ulp=" if "?" in self.prefix else "?ulp="
        return f"{self.prefix}{sep}{quote(product_url, safe='')}"

_PORTALS_API_LOCK = asyncio.Lock()
_LAST_PORTALS_CALL_TIME = 0.0

class PortalsApiAffiliateProvider(AffiliateProvider):
    """
    Official AliExpress Open Platform Portals API provider.
    Uses 'python-aliexpress-api' (aliexpress.affiliate.link.generate) to generate
    official https://s.click.aliexpress.com/e/_... short links.
    Generates genuine Coin links (90%+) or Bundle links directly.
    """
    def __init__(self, app_key: Optional[str] = None, app_secret: Optional[str] = None, tracking_id: Optional[str] = None):
        self.app_key = app_key or settings.ALIEXPRESS_AFFILIATE_APP_KEY
        self.app_secret = app_secret or settings.ALIEXPRESS_AFFILIATE_APP_SECRET
        self.tracking_id = tracking_id or settings.ALIEXPRESS_AFFILIATE_TRACKING_ID or "dzkhvled16"
        self.fallback = DirectAffiliateProvider(self.tracking_id)
        self.api = None

        if self.app_key and self.app_secret:
            try:
                from aliexpress_api import AliexpressApi, models
                self.api = AliexpressApi(
                    self.app_key,
                    self.app_secret,
                    models.Language.EN,
                    models.Currency.USD,
                    self.tracking_id or "default"
                )
                logger.info("AliExpress Portals API initialized successfully.")
            except Exception as e:
                logger.error(f"Failed to initialize AliexpressApi: {e}")

    async def generate_link(self, product_url: str, product_id: Optional[str] = None, deal_type: str = "coin") -> str:
        pid = product_id
        if not pid:
            m = re.search(r'/item/(\d+)\.html', product_url)
            if m:
                pid = m.group(1)
            else:
                m_pid = re.search(r'productIds?=(\d+)', product_url)
                if m_pid:
                    pid = m_pid.group(1)

        # Target URL determination based on deal_type
        if pid:
            if deal_type == "bundle":
                target_url = f"https://www.aliexpress.com/ssr/300000512/BundleDeals2?disableNav=YES&pha_manifest=ssr&_immersiveMode=true&productIds={pid}"
            elif deal_type == "super":
                target_url = f"https://www.aliexpress.com/item/{pid}.html?sourceType=561&channel=superdeal"
            elif deal_type == "item":
                target_url = f"https://www.aliexpress.com/item/{pid}.html"
            else:
                target_url = f"https://m.aliexpress.com/p/coin-index/index.html?_immersiveMode=true&tabname=configTab_1926001&productIds={pid}"
        else:
            if deal_type == "bundle":
                target_url = "https://www.aliexpress.com/ssr/300000512/BundleDeals2?disableNav=YES&pha_manifest=ssr&_immersiveMode=true"
            elif deal_type == "super":
                sep = "&" if "?" in product_url else "?"
                target_url = f"{product_url}{sep}sourceType=561&channel=superdeal"
            else:
                target_url = product_url

        if self.api:
            global _LAST_PORTALS_CALL_TIME
            async with _PORTALS_API_LOCK:
                import time
                elapsed = time.time() - _LAST_PORTALS_CALL_TIME
                if elapsed < 1.1:
                    await asyncio.sleep(1.1 - elapsed)
                _LAST_PORTALS_CALL_TIME = time.time()

                for attempt in range(1, 3):
                    try:
                        aff_links = await asyncio.to_thread(self.api.get_affiliate_links, target_url)
                        if aff_links and len(aff_links) > 0:
                            link = getattr(aff_links[0], "promotion_link", None) or getattr(aff_links[0], "promotion_url", None)
                            if link:
                                return link
                        # If API responded cleanly but target_url has no promotion link (e.g. raw /item/ URL),
                        # retry with coin index URL which reliably produces official /e/ shortlinks in Portals API!
                        if pid:
                            coin_target = f"https://m.aliexpress.com/p/coin-index/index.html?_immersiveMode=true&tabname=configTab_1926001&productIds={pid}"
                            if target_url != coin_target:
                                try:
                                    coin_aff_links = await asyncio.to_thread(self.api.get_affiliate_links, coin_target)
                                    if coin_aff_links and len(coin_aff_links) > 0:
                                        c_link = getattr(coin_aff_links[0], "promotion_link", None) or getattr(coin_aff_links[0], "promotion_url", None)
                                        if c_link:
                                            return c_link
                                except Exception as e2:
                                    logger.warning(f"Portals API coin fallback failed: {e2}")
                        break
                    except Exception as e:
                        logger.warning(f"AliExpress Portals API attempt {attempt}/2 failed: {e}")
                        if attempt < 2:
                            await asyncio.sleep(1.5)
                            _LAST_PORTALS_CALL_TIME = time.time()
                            continue
        return await self.fallback.generate_link(product_url, product_id, deal_type=deal_type)

class AffiliateService:
    def __init__(self):
        # Automatically use Portals API if keys are configured, otherwise Direct
        if settings.ALIEXPRESS_AFFILIATE_APP_KEY and settings.ALIEXPRESS_AFFILIATE_APP_SECRET:
            self.provider: AffiliateProvider = PortalsApiAffiliateProvider(
                settings.ALIEXPRESS_AFFILIATE_APP_KEY,
                settings.ALIEXPRESS_AFFILIATE_APP_SECRET,
                settings.ALIEXPRESS_AFFILIATE_TRACKING_ID
            )
        elif settings.ALIEXPRESS_AFFILIATE_PROVIDER == "custom" and settings.ALIEXPRESS_CUSTOM_AFFILIATE_PREFIX:
            self.provider = CustomNetworkAffiliateProvider(
                settings.ALIEXPRESS_CUSTOM_AFFILIATE_PREFIX
            )
        else:
            self.provider = DirectAffiliateProvider(
                settings.ALIEXPRESS_AFFILIATE_TRACKING_ID
            )

    async def create_affiliate_link(self, product_url: str, product_id: Optional[str] = None, deal_type: str = "coin") -> str:
        """Converts raw/canonical AliExpress URL to our verified affiliate URL on aliexpress.com domain."""
        return await self.provider.generate_link(product_url, product_id, deal_type=deal_type)

affiliate_service = AffiliateService()
