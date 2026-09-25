import re
import hashlib
from typing import Optional, List, Dict
from app.config.settings import settings
from app.utils.logger import logger

class DealCaptionGenerator:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.model = model or settings.AI_MODEL

    def _select_smart_hook(
        self,
        title: str,
        usd_price: float,
        has_points_discount: bool,
        has_coupon: bool,
        promo_tag: Optional[str] = None
    ) -> str:
        """
        Generates varied, smart, situation-aware Arabic hooks:
        - Keeps 'العرض مستمر 🚨' in the rotation.
        - Coins situation: 'تخفيض عملات خرافي 🪙🔥', 'استغل رصيد العملات واشترِ بأقل سعر 🪙💰'
        - Gaming situation: 'صيدة ممتازة للقيمرز 🎮🔥', 'عتاد قيمنق بأفضل قيمة مقابل سعر 🎧🖱️'
        - Price drops: 'نزول قوي في السعر 🔥📉', 'سعر ممتاز جداً لا يُفوّت 💥', 'أفضل سعر متوفر حالياً 🚨'
        - Flash/limited: 'الكمية محدودة سارع بالطلب ⏳🚨', 'تخفيض حصري لفترة محدودة ⚡'
        """
        h = int(hashlib.md5(title.encode()).hexdigest(), 16)
        t_lower = title.lower()

        is_gaming = any(k in t_lower for k in [
            "mouse", "keyboard", "headset", "earphone", "controller", "gamepad",
            "gaming", "gamer", "attack shark", "ajazz", "aula", "vgn", "game", "rgb"
        ]) or any(k in title for k in ["ماوس", "كيبورد", "سماعة", "جيمنج", "قيمنق", "تحكم"])

        candidates = []

        # 1. Situation: Coins / Points
        if has_points_discount:
            candidates.extend([
                "تخفيض عملات خرافي 🪙🔥",
                "استغل رصيد العملات واشترِ بأقل سعر 🪙💰",
                "خصم إضافي قوي بالعملات لا تضيعه 🪙⚡",
            ])

        # 2. Situation: Gaming & Tech
        if is_gaming:
            candidates.extend([
                "صيدة ممتازة للقيمرز 🎮🔥",
                "عتاد قيمنق بأفضل قيمة مقابل سعر 🎧🖱️",
                "عرض ناري لعشاق الجيمنج 🕹️💥",
            ])

        # 3. Situation: Low price / Hot deal (<$25)
        if usd_price and usd_price < 25.0:
            candidates.extend([
                "نزول قوي في السعر 🔥📉",
                "سعر ممتاز جداً لا يُفوّت 💥",
                "أفضل سعر متوفر حالياً 🚨",
                "عرض نااار بسعر استثنائي 🔥",
            ])

        # 4. Situation: Coupon code present
        if has_coupon:
            candidates.extend([
                "تخفيض مباشر مع كود الخصم 🎟️🔥",
                "سعر مميز بعد تطبيق الكوبون 🏷️⚡",
            ])

        # 5. Core urgent & ongoing hooks (always in rotation)
        candidates.extend([
            "العرض مستمر 🚨",
            "الكمية محدودة سارع بالطلب ⏳🚨",
            "تخفيض حصري لفترة محدودة ⚡",
            "سعر ممتاز متوفر الآن 🚨",
        ])

        return candidates[h % len(candidates)]

    def format_coupon_list(
        self,
        coupon_items: List[Dict[str, str]],
        affiliate_url: str
    ) -> str:
        """
        Builds the clean Arabic coupon bulletin format when a channel posts a full list of coupons.
        """
        lines = [
            "أحدث كودات التخفيض من AliExpress 🎟️🔥",
            "━━━━━━━━━━━━━━━━━"
        ]

        for item in coupon_items:
            tier = item.get("tier", "").strip()
            code = item.get("code", "").strip()
            if tier and code:
                lines.append(f"▫️ خصم {tier} | الكود: <code>{code}</code>")
            elif code:
                lines.append(f"▫️ كود: <code>{code}</code>")

        lines.append("━━━━━━━━━━━━━━━━━")
        lines.append("🔗 رابط صفحة الكوبونات والتخفيضات:")
        lines.append(f"{affiliate_url}")
        lines.append("")
        lines.append("🪙 استخدم بوت DealScoutDz للشراء بأقل سعر: @Alilo07BOT")

        return "\n".join(lines)

    def _format_deterministic(
        self,
        title: str,
        usd_price: float,
        eur_price: float,
        affiliate_url: str,
        coupon_code: Optional[str] = None,
        has_points_discount: bool = False,
        country_info: Optional[str] = None,
        promo_tag: Optional[str] = None
    ) -> str:
        """
        Builds the dynamic post format with situational hooks and country instructions:
        [إشعار الحملة الترويجية إن وجد]
        [إشعار الدولة إن وجد - مثلاً: لا تنسى تحويل دولة التطبيق إلى كوريا 🇰🇷 📍]
        {SMART_SITUATIONAL_HOOK}
        تخفيض لـ {PRODUCT_TITLE}
        السعر : {USD_PRICE}$ ({EUR_PRICE}€)🔥
        رابط {AFFILIATE_URL}
        كوبون : {COUPON} (إن وجد)
        خصم النقاط (إن وجد)

        🪙 استخدم بوت DealScoutDz للشراء بأقل سعر: @Alilo07BOT
        """
        lines = []

        if promo_tag:
            lines.append(f"{promo_tag} 🛍️")

        if country_info:
            c_str = str(country_info).lower()
            if "كوريا" in country_info or "korea" in c_str or "kr" in c_str:
                lines.append("لا تنسى تحويل دولة التطبيق إلى كوريا 🇰🇷 📍")
            elif "فرنسا" in country_info or "france" in c_str or "fr" in c_str:
                lines.append("لا تنسى تحويل دولة التطبيق إلى فرنسا 🇫🇷 📍")
            elif "كندا" in country_info or "canada" in c_str or "ca" in c_str:
                lines.append("لا تنسى تحويل دولة التطبيق إلى كندا 🇨🇦 📍")
            elif "إسبانيا" in country_info or "spain" in c_str or "es" in c_str:
                lines.append("لا تنسى تحويل دولة التطبيق إلى إسبانيا 🇪🇸 📍")
            else:
                lines.append(f"لا تنسى تحويل دولة التطبيق إلى {country_info} 📍")

        # Select smart situational hook
        hook = self._select_smart_hook(
            title=title,
            usd_price=usd_price,
            has_points_discount=has_points_discount,
            has_coupon=bool(coupon_code),
            promo_tag=promo_tag
        )
        lines.append(hook)

        lines.append(f"تخفيض لـ {title}")
        lines.append(f"السعر : {usd_price:.2f}$ ({eur_price:.2f}€)🔥")
        lines.append(f"رابط {affiliate_url}")

        if coupon_code:
            lines.append(f"كوبون : <code>{coupon_code}</code>")

        if has_points_discount:
            lines.append("خصم النقاط (العملات)")

        lines.append("")
        lines.append("🪙 استخدم بوت DealScoutDz للشراء بأقل سعر: @Alilo07BOT")

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
        coupon_list: Optional[List[Dict[str, str]]] = None,
        promo_tag: Optional[str] = None
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
            country_info=country_info,
            promo_tag=promo_tag
        )

caption_generator = DealCaptionGenerator()
