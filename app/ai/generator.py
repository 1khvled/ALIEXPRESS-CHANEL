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
        promo_tag: Optional[str] = None,
        is_price_drop: bool = False
    ) -> str:
        """
        Generates authentic Algerian Telegram deal channel hooks.
        Dynamically detects subcategories (Gaming, Audio, Storage/Hardware, Chargers/Power, Wearables)
        and price-drop drops.
        """
        h = int(hashlib.md5(title.encode()).hexdigest(), 16)
        t_lower = title.lower()

        # 1. Price-Drop Arbitrage Hook
        if is_price_drop:
            price_drop_hooks = [
                "💥 <b>نزول إضافي في السعر 🔥📉</b>",
                "⚡ <b>طاح السعر أكثر.. ألحـــــق لافــــــــــــــار! 🔥</b>",
                "🔥 <b>تخفيض إضافي حصري قوي 🔥</b>"
            ]
            return price_drop_hooks[h % len(price_drop_hooks)]

        # 2. Category Detection
        is_gaming = any(k in t_lower for k in [
            "mouse", "keyboard", "headset", "controller", "gamepad", "gaming", "gamer",
            "attack shark", "ajazz", "aula", "vgn", "game", "rgb", "joystick", "switch", "keycap", "fantech"
        ]) or any(k in title for k in ["ماوس", "كيبورد", "جيمنج", "قيمنق", "تحكم", "يدات"])

        is_audio = any(k in t_lower for k in [
            "earphone", "earbuds", "headphone", "tws", "speaker", "soundbar",
            "soundcore", "qcy", "baseus bowie", "lenovo lp", "anc", "bluetooth speaker"
        ]) or any(k in title for k in ["سماعة", "سماعات", "صوت", "مكبر صوت"])

        is_storage = any(k in t_lower for k in [
            "ssd", "nvme", "m.2", "sata", "ddr4", "ddr5", "ram", "micro sd", "sd card",
            "pendrive", "thermal paste", "cooler", "heatsink", "fan hub"
        ]) or any(k in title for k in ["قرص صلب", "تخزين", "هارد", "رامات", "معجون"])

        is_power = any(k in t_lower for k in [
            "gan", "charger", "fast charge", "65w", "100w", "30w", "45w", "powerbank", "power bank",
            "usb-c", "type-c", "cable", "ugreen", "essager", "toocki", "kuulaa"
        ]) or any(k in title for k in ["شاحن", "كابل", "باور بانك", "شحن سريع"])

        is_watch = any(k in t_lower for k in [
            "smartwatch", "smart watch", "smart band", "miband", "mi band", "haylou", "zeblaze", "kieslect", "colmi"
        ]) or any(k in title for k in ["ساعة ذكية", "سوار ذكي"])

        if is_gaming:
            return (
                "🎮 <b>عتـاد قيمنق بسـعر مـمـتاز 🔥🔥</b>" if (h % 2 == 0)
                else "🕹️ <b>لافـار قيمنق متتفـوّتش 🔥⚡</b>"
            )

        if is_audio:
            return (
                "🎧 <b>صـوت نقي وسـعر لافـار 🔥🔥</b>" if (h % 2 == 0)
                else "🔊 <b>تخفيض ممتاز على السـماعات ⚡</b>"
            )

        if is_storage:
            return (
                "💾 <b>لافـار قوية في مساحة التخزين 🔥⚡</b>" if (h % 2 == 0)
                else "⚡ <b>عتـاد كمبيوتر بأقوى سعر 🔥</b>"
            )

        if is_power:
            return (
                "🔌 <b>شواحن وكوابل سريعة بسعر باطل 🔥⚡</b>" if (h % 2 == 0)
                else "⚡ <b>تخفيض قوي على ملحقات الشحن 🔥</b>"
            )

        if is_watch:
            return (
                "⌚ <b>ساعة ذكية بأناقة وسعر خيالي 🔥</b>" if (h % 2 == 0)
                else "⌚ <b>سـعر ممـتاز لسـاعة ذكية ⚡</b>"
            )

        candidates = []

        if has_points_discount:
            candidates.extend([
                "🪙 <b>تخفيض قوي بالعملات 🔥</b>",
                "⚡ <b>ألحـــــق لافــــــــــــــار</b>",
                "🔥 <b>ســـعـــر ممتـــــــــــــــــــــــــاز</b>",
            ])

        if usd_price and usd_price < 25.0:
            candidates.extend([
                "⚡ <b>ألحـــــق لافــــــــــــــار</b>",
                "🔥 <b>ســـعـــر ممتـــــــــــــــــــــــــاز</b>",
                "💥 <b>هبوط قوي في السعر 🔥</b>",
            ])

        if has_coupon:
            candidates.extend([
                "🎟️ <b>تخفيض قوي بالكود 🔥</b>",
                "🔥 <b>ســـعـــر ممتـــــــــــــــــــــــــاز</b>",
            ])

        candidates.extend([
            "🔥 <b>ســـعـــر ممتـــــــــــــــــــــــــاز</b>",
            "⚡ <b>ألحـــــق لافــــــــــــــار</b>",
            "💥 <b>هبوط قوي في السعر 🔥</b>",
        ])

        return candidates[h % len(candidates)]

    def format_coupon_list(
        self,
        coupon_items: List[Dict[str, str]],
        affiliate_url: str,
        promo_name: Optional[str] = "Party Ready Sale"
    ) -> str:
        """
        Builds authentic Algerian coupon bulletin format for multi-coupon lists.
        """
        lines = [
            f"✨📢 <b>ظهور كوبونات جديدة بمناسبة تخفيضات {promo_name} احجزها الآن!</b> 📢✨",
            "",
            "✅ <b>قائمة الكوبونات:</b>",
            ""
        ]

        for item in coupon_items:
            tier = item.get("tier", "").strip()
            code = item.get("code", "").strip()
            if tier and code:
                lines.append(f"🎟️ <b>كوبــــــون {tier} :</b> <code>{code}</code>")
            elif code:
                lines.append(f"🎟️ <b>كوبــــــون :</b> <code>{code}</code>")

        lines.append("")
        lines.append("✅ <b>رابط المناسبة وتفعيل الكوبونات ⬇️</b>")
        lines.append(f"{affiliate_url}")
        lines.append("")
        lines.append("⭐ <i>لا تنسى استخدام بوت العملات للشراء بأقل الأسعار:</i> @Alilo07BOT")
        lines.append("📢 <i>قناة العروض: @DzAliexpress0</i>")

        return "\n".join(lines)

    def format_event_campaign(
        self,
        raw_text: str,
        affiliate_url: str
    ) -> str:
        """
        Formats AliExpress official event / warm-up announcements in authentic Algerian style.
        """
        clean_lines = []
        for line in raw_text.splitlines():
            line_str = line.strip()
            if not line_str or "http://" in line_str or "https://" in line_str or "t.me/" in line_str or "COINBOT" in line_str:
                continue
            clean_lines.append(line_str)

        main_content = "\n".join(clean_lines).strip()
        if not main_content:
            main_content = "✨ <b>تخفيضات وكوبونات حصرية بمناسبة انطلاق العروض الجديدة على AliExpress!</b>"

        lines = [
            f"🎉 <b>{main_content}</b>",
            "",
            "🔗 <b>رابط الدخول وتحصيل الكوبونات ⬇️</b>",
            f"{affiliate_url}",
            "",
            "⭐ <i>لا تنسى استخدام بوت العملات للشراء بأقل الأسعار:</i> @Alilo07BOT",
            "📢 <i>قناة العروض: @DzAliexpress0</i>"
        ]
        return "\n".join(lines)

    def _format_deterministic(
        self,
        title: str,
        usd_price: float,
        eur_price: float,
        affiliate_url: str,
        coupon_code: Optional[str] = None,
        seller_coupon: Optional[str] = None,
        has_points_discount: bool = False,
        country_info: Optional[str] = None,
        promo_tag: Optional[str] = None,
        is_price_drop: bool = False,
        coin_url: Optional[str] = None
    ) -> str:
        lines = []

        # 1. Authentic Algerian Deal Hook
        hook = self._select_smart_hook(
            title=title,
            usd_price=usd_price,
            has_points_discount=has_points_discount,
            has_coupon=bool(coupon_code or seller_coupon),
            promo_tag=None,
            is_price_drop=is_price_drop
        )
        lines.append(hook)

        # 2. Country recommendation (exact Algerian Telegram style)
        if country_info:
            c_str = str(country_info).lower()
            if "كوريا" in country_info or "korea" in c_str or "kr" in c_str:
                lines.append("خلي البلـــد كــــــوريا 🇰🇷")
            elif "كندا" in country_info or "canada" in c_str or "ca" in c_str:
                lines.append("خلي البلـــد كــــــندا 🇨🇦")
            elif "الجزائر" in country_info or "algeria" in c_str or "dz" in c_str:
                lines.append("بلد الحساب <b>الجزائر 🇩🇿</b>")
            elif "فرنسا" in country_info or "france" in c_str or "fr" in c_str:
                lines.append("خلي البلـــد فـــرنسا 🇫🇷")
            elif "إسبانيا" in country_info or "spain" in c_str or "es" in c_str:
                lines.append("خلي البلـــد إسبـــانيا 🇪🇸")

        import html
        safe_title = html.escape(title)

        # Approximate DZD price (1 USD ≈ 249 DZD)
        dzd_approx = int(usd_price * 249) if usd_price else 0

        lines.append("")
        lines.append(f"✅ <b>{safe_title}</b>")

        if usd_price and usd_price > 0:
            dzd_str = f" (~<b>{dzd_approx:,} دج</b>)" if dzd_approx > 0 else ""
            lines.append(f"💰 <b>السعر:</b> <b>${usd_price:.2f}</b>{dzd_str}")
        else:
            lines.append("💰 <b>السعر:</b> <b>سعر خاص ومخفض</b>")

        if seller_coupon:
            lines.append(f"🎫 <b>قسيمة المتجر:</b> <code>{html.escape(seller_coupon)}</code>")

        if coupon_code:
            lines.append(f"🎟️ <b>الكوبون:</b> <code>{html.escape(coupon_code)}</code>")

        if has_points_discount:
            lines.append("🪙 <b>تخفيض العملات:</b> مفعّل عبر الرابط")

        lines.append("")
        if coin_url and coin_url != affiliate_url and "coin-index" not in str(affiliate_url):
            lines.append("📎 <b>رابط الشراء ⬇️</b>")
            lines.append(f"{affiliate_url}")
            lines.append("")
            lines.append("🪙 <b>رابط أقصى تخفيض بالعملات (Coins) ⬇️</b>")
            lines.append(f"{coin_url}")
        else:
            if has_points_discount or "coin-index" in str(affiliate_url):
                lines.append("📎 <b>رابط الشراء بتخفيض العملات ⬇️</b>")
            else:
                lines.append("📎 <b>رابط الشراء المباشر ⬇️</b>")
            lines.append(f"{affiliate_url}")

        lines.append("")
        lines.append("📢 <i>قناة العروض: @DzAliexpress0</i>")

        return "\n".join(lines)

    async def generate(
        self,
        title: str,
        usd_price: Optional[float],
        eur_price: Optional[float],
        affiliate_url: str,
        coupon_code: Optional[str] = None,
        seller_coupon: Optional[str] = None,
        has_points_discount: bool = False,
        country_info: Optional[str] = None,
        coupon_list: Optional[List[Dict[str, str]]] = None,
        promo_tag: Optional[str] = None,
        is_price_drop: bool = False,
        coin_url: Optional[str] = None,
        raw_text: Optional[str] = None
    ) -> str:
        """
        Generates authentic Algerian Telegram channel caption.
        """
        if coupon_list and len(coupon_list) >= 2:
            return self.format_coupon_list(coupon_list, affiliate_url)

        if (not usd_price or usd_price <= 0) and raw_text and any(k in raw_text for k in ["كوبونات", "تحصيل", "رابط المناسبة", "تخفيضات", "عشوائية", "party ready", "choice day"]):
            return self.format_event_campaign(raw_text, affiliate_url)

        usd_val = usd_price or 0.0
        eur_val = eur_price or round(usd_val * (settings.EUR_USD_RATE or 0.92), 2)
        clean_title = title.strip() if title else "منتج مميز من AliExpress"

        return self._format_deterministic(
            title=clean_title,
            usd_price=usd_val,
            eur_price=eur_val,
            affiliate_url=affiliate_url,
            coupon_code=coupon_code,
            seller_coupon=seller_coupon,
            has_points_discount=has_points_discount,
            country_info=country_info,
            promo_tag=promo_tag,
            is_price_drop=is_price_drop,
            coin_url=coin_url
        )

caption_generator = DealCaptionGenerator()
