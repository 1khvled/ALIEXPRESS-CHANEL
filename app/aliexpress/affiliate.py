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
        self.tracking_id = tracking_id or settings.ALIEXPRESS_AFFILIATE_TRACKING_ID

    async def generate_link(self, product_url: str, product_id: Optional[str] = None, deal_type: str = "coin") -> str:
        if not self.tracking_id:
            return product_url

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
                return f"https://aliexpress.com/item/{pid}.html?sourceType=562&aff_fcid={self.tracking_id}"
            else:
                return f"https://m.aliexpress.com/p/coin-index/index.html?productIds={pid}&aff_fcid={self.tracking_id}"

        separator = "&" if "?" in product_url else "?"
        return f"{product_url}{separator}aff_fcid={self.tracking_id}"

class CustomNetworkAffiliateProvider(AffiliateProvider):
    def __init__(self, prefix: str):
        self.prefix = prefix

    async def generate_link(self, product_url: str, product_id: Optional[str] = None, deal_type: str = "coin") -> str:
        if not self.prefix:
            return product_url
        sep = "&ulp=" if "?" in self.prefix else "?ulp="
        return f"{self.prefix}{sep}{quote(product_url, safe='')}"

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
        self.tracking_id = tracking_id or settings.ALIEXPRESS_AFFILIATE_TRACKING_ID
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

        # 90%+ of channel deals are coin deals! Bundle deals in rare cases.
        if pid:
            if deal_type == "bundle":
                target_url = f"https://www.aliexpress.com/item/{pid}.html?sourceType=562"
            else:
                target_url = f"https://m.aliexpress.com/p/coin-index/index.html?productIds={pid}"
        else:
            target_url = product_url

        if self.api:
            for attempt in range(3):
                try:
                    aff_links = await asyncio.to_thread(self.api.get_affiliate_links, target_url)
                    if aff_links and len(aff_links) > 0 and aff_links[0].promotion_link:
                        return aff_links[0].promotion_link
                except Exception as e:
                    err_msg = str(e).lower()
                    if "frequency exceeds" in err_msg or "ban will last" in err_msg or "limit" in err_msg:
                        logger.info("AliExpress API rate limited, waiting 1.5s before retry...")
                        await asyncio.sleep(1.5)
                        continue
                    logger.warning(f"AliExpress Portals API call failed: {e}. Falling back to direct URL.")
                    break
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
