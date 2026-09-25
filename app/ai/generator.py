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
        Generates premium, distinct DealScout badges.
        Strictly avoids competitor cliches (no 'الحق', 'سارع بالطلب', or 'لافار').
        """
        h = int(hashlib.md5(title.encode()).hexdigest(), 16)
        t_lower = title.lower()

        is_gaming = any(k in t_lower for k in [
            "mouse", "keyboard", "headset", "earphone", "controller", "gamepad",
            "gaming", "gamer", "attack shark", "ajazz", "aula", "vgn", "game", "rgb"
        ]) or any(k in title for k in ["ماوس", "كيبورد", "سماعة", "جيمنج", "قيمنق", "تحكم"])

        candidates = []

        if is_gaming:
            candidates.extend([
                "🎮 <b>صفقة قيمنق مختارة | DealScout Gaming Pick</b>",
                "🎯 <b>عتاد قيمنق عالي الأداء | Pro Hardware Pick</b>",
            ])

        if has_points_discount:
            candidates.extend([
                "🪙 <b>توفير فائق بالعملات | DealScout Coins Pick</b>",
                "⚡ <b>أقصى خصم بالعملات | Max Coins Value</b>",
            ])

        if usd_price and usd_price < 25.0:
            candidates.extend([
                "💎 <b>أفضل قيمة مقابل سعر | DealScout Value Pick</b>",
                "📉 <b>هبوط قوي في السعر | Price Drop Alert</b>",
            ])

        if has_coupon:
            candidates.extend([
                "🎟️ <b>صفقة كود الخصم | Verified Promo Code</b>",
                "🏷️ <b>تخفيض مباشر بالكوبون | Instant Coupon Deal</b>",
            ])

        candidates.extend([
            "🎯 <b>صفقة اليوم المعتمدة | DealScout Verified Deal</b>",
            "✨ <b>منتج مختار بعناية | Curated DealScout Pick</b>",
        ])

        return candidates[h % len(candidates)]

    def format_coupon_list(
        self,
        coupon_items: List[Dict[str, str]],
        affiliate_url: str
    ) -> str:
        """
        Builds clean, branded coupon bulletin format for multi-coupon lists.
        """
        lines = [
            "🎟️ <b>دليل كوبونات وقسائم التخفيض المعتمدة | DealScout</b>",
            "━━━━━━━━━━━━━━━━━"
        ]

        for item in coupon_items:
            tier = item.get("tier", "").strip()
            code = item.get("code", "").strip()
            if tier and code:
                lines.append(f"▫️ خصم <b>{tier}</b> ⬅️ الكود: <code>{code}</code>")
            elif code:
                lines.append(f"▫️ الكود: <code>{code}</code>")

        lines.append("━━━━━━━━━━━━━━━━━")
        lines.append("🔗 <b>رابط صفحة تفعيل الكوبونات:</b>")
        lines.append(f"{affiliate_url}")
        lines.append("━━━━━━━━━━━━━━━━━")
        lines.append("🪙 استخدم بوت DealScoutDz لزيادة خصم العملات: @Alilo07BOT")
        lines.append("📢 قناة العروض الحصرية: @DzAliexpress0")

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
        Builds the DealScout signature post format:
        [إشعار الحملة الترويجية إن وجد]
        🎯 صفقة اليوم المعتمدة | DealScout Verified Deal
        🌐 دولة العرض: كندا 🇨🇦 (لأقصى تخفيض بالعملات)
        
        📦 PRODUCT_TITLE
        ━━━━━━━━━━━━━━━━━
        💰 السعر: $XX.XX (~XXXX دج | XX.XX€)
        🎟️ كود الخصم: CODE
        🪙 تخفيض العملات: مفعّل تلقائياً
        
        🔗 رابط الطلب المباشر:
        AFFILIATE_URL
        ━━━━━━━━━━━━━━━━━
        💡 افتح الرابط عبر تطبيق AliExpress لتطبيق كامل الخصم.
        📢 قناة العروض المعتمدة: @DzAliexpress0
        """
        lines = []

        if promo_tag:
            lines.append(f"📅 <b>{promo_tag}</b>")

        # 1. Smart situational hook badge
        hook = self._select_smart_hook(
            title=title,
            usd_price=usd_price,
            has_points_discount=has_points_discount,
            has_coupon=bool(coupon_code),
            promo_tag=promo_tag
        )
        lines.append(hook)

        # 2. Country recommendation
        if country_info:
            c_str = str(country_info).lower()
            if "كوريا" in country_info or "korea" in c_str or "kr" in c_str:
                lines.append("🌐 دولة العرض: <b>كوريا 🇰🇷</b> (تخفيض عملات أقصى)")
            elif "كندا" in country_info or "canada" in c_str or "ca" in c_str:
                lines.append("🌐 دولة العرض: <b>كندا 🇨🇦</b> (تخفيض عملات أقصى)")
            elif "فرنسا" in country_info or "france" in c_str or "fr" in c_str:
                lines.append("🌐 دولة العرض: <b>فرنسا 🇫🇷</b>")
            elif "إسبانيا" in country_info or "spain" in c_str or "es" in c_str:
                lines.append("🌐 دولة العرض: <b>إسبانيا 🇪🇸</b>")
            else:
                lines.append(f"🌐 دولة العرض: <b>{country_info}</b>")

        import html
        safe_title = html.escape(title)

        # Approximate DZD price (1 USD ≈ 249 DZD)
        dzd_approx = int(usd_price * 249) if usd_price else 0

        lines.append("")
        lines.append(f"📦 <b>{safe_title}</b>")
        lines.append("━━━━━━━━━━━━━━━━━")

        if usd_price and usd_price > 0:
            dzd_str = f" (~<b>{dzd_approx:,} دج</b>)" if dzd_approx > 0 else ""
            lines.append(f"💰 <b>السعر:</b> <b>${usd_price:.2f}</b>{dzd_str} | <i>{eur_price:.2f}€</i>")
        else:
            lines.append("💰 <b>السعر:</b> <b>سعر خاص ومخفض</b>")

        if coupon_code:
            lines.append(f"🎟️ <b>كود الخصم:</b> <code>{html.escape(coupon_code)}</code>")

        if has_points_discount:
            lines.append("🪙 <b>تخفيض العملات:</b> مفعّل تلقائياً عبر الرابط")

        lines.append("")
        lines.append("🔗 <b>رابط الطلب المباشر:</b>")
        lines.append(f"{affiliate_url}")
        lines.append("━━━━━━━━━━━━━━━━━")
        lines.append("💡 <i>افتح الرابط عبر تطبيق AliExpress لتطبيق كامل الخصم.</i>")
        lines.append("📢 قناة العروض المعتمدة: @DzAliexpress0")

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
