import re
from typing import Optional, List, Dict
from app.config.settings import settings
from app.utils.logger import logger

class DealCaptionGenerator:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.model = model or settings.AI_MODEL

    def format_coupon_list(
        self,
        coupon_items: List[Dict[str, str]],
        affiliate_url: str
    ) -> str:
        """
        Builds the clean Arabic coupon bulletin format when a channel posts a full list of coupons.
        """
        lines = [
            "أحدث كوبونات وتخفيضات AliExpress 🚨🔥",
            ""
        ]

        for item in coupon_items:
            tier = item.get("tier", "").strip()
            code = item.get("code", "").strip()
            lines.append(f"🎟️ كوبون {tier} : {code}")

        lines.append("")
        lines.append("رابط صفحة الكوبونات والتخفيضات:")
        lines.append(f"🔗 {affiliate_url}")
        lines.append("")
        lines.append("لا تنسى استخدام البوت للشراء بأقل الأسعار")

        return "\n".join(lines)

    def _format_deterministic(
        self,
        title: str,
        usd_price: float,
        eur_price: float,
        affiliate_url: str,
        coupon_code: Optional[str] = None,
        has_points_discount: bool = False,
        country_info: Optional[str] = None
    ) -> str:
        """
        Builds the exact post format matching top Algerian channels:
        [إشعار الدولة إن وجد]
        العرض مستمر 🚨
        تخفيض لـ {PRODUCT_TITLE}
        السعر : {USD_PRICE}$ ({EUR_PRICE}€)🔥
        رابط {AFFILIATE_URL}
        كوبون : {COUPON} (إن وجد)
        خصم النقاط (إن وجد)

        لا تنسى استخدام البوت للشراء بأقل الأسعار
        """
        lines = []
        if country_info:
            lines.append(f"لا تنسى تحويل دولة التطبيق إلى {country_info} 📍")
        lines.append("العرض مستمر 🚨")
        lines.append(f"تخفيض لـ {title}")
        lines.append(f"السعر : {usd_price:.2f}$ ({eur_price:.2f}€)🔥")
        lines.append(f"رابط {affiliate_url}")

        if coupon_code:
            lines.append(f"كوبون : {coupon_code}")

        if has_points_discount:
            lines.append("خصم النقاط")

        lines.append("")
        lines.append("لا تنسى استخدام البوت للشراء بأقل الأسعار")

        return "\n".join(lines)

    async def generate(
        self,
        title: str,
        usd_price: Optional[float],
        eur_price: Optional[float],
        affiliate_url: str,
        coupon_code: Optional[str] = None,
        has_points_discount: bool = False,
        country_info: Optional[str] = None,
        coupon_list: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Generates clean Arabic Telegram caption matching project requirements.
        """
        if coupon_list and len(coupon_list) >= 2:
            return self.format_coupon_list(coupon_list, affiliate_url)

        usd_val = usd_price or 0.0
        eur_val = eur_price or round(usd_val * (settings.EUR_USD_RATE or 0.92), 2)
        clean_title = title.strip() if title else "منتج مميز من AliExpress"

        return self._format_deterministic(
            title=clean_title,
            usd_price=usd_val,
            eur_price=eur_val,
            affiliate_url=affiliate_url,
            coupon_code=coupon_code,
            has_points_discount=has_points_discount,
            country_info=country_info
        )

caption_generator = DealCaptionGenerator()
