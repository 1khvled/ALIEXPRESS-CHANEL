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
                "💥 <b>هبوط قوي في السعر.. ألحـــــق لافــــــــــــــار! 📉🔥</b>",
                "⚡ <b>طاح السعر أكثر.. تخفيض إضافي ناااار 🔥</b>",
                "🔥 <b>نزول إضافي في السعر صيدة اليوم متتراطاش 🔥</b>"
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
                "🎮 <b>لافاااااار قيمنق متتفوتش عتاد بأقوى سعر 🔥🕹️</b>" if (h % 2 == 0)
                else "🕹️ <b>صيدة قيمنق خيالية بسعر باطل 🔥⚡</b>"
            )

        if is_audio:
            return (
                "🎧 <b>صوت نقي وسعر لافار هبال متتراطاش 🔥🎧</b>" if (h % 2 == 0)
                else "🔊 <b>تخفيض ممتاز على السماعات صيدة نااار ⚡</b>"
            )

        if is_storage:
            return (
                "💾 <b>صيدة اليوم في التخزين والكمبيوتر هبال 🔥⚡</b>" if (h % 2 == 0)
                else "⚡ <b>عتاد كمبيوتر وتخزين بأقوى سعر 🔥</b>"
            )

        if is_power:
            return (
                "🔌 <b>شواحن وكوابل سريعة بسعر باطل هبال 🔥⚡</b>" if (h % 2 == 0)
                else "⚡ <b>تخفيض قوي على ملحقات الشحن الأصلية 🔥</b>"
            )

        if is_watch:
            return (
                "⌚ <b>ساعة ذكية بأناقة وسعر خيالي لافار 🔥</b>" if (h % 2 == 0)
                else "⌚ <b>سعر ممتاز لساعة ذكية ألحق الصيدة ⚡</b>"
            )

        candidates = [
            "🔥 <b>لافـــــــــــــــــــــــار هباااال 🔥</b>",
            "🔥 <b>الحححححق عودة لافاااار ناااار 💥</b>",
            "⚡ <b>ألحـــــق لافــــــــــــــار بأقوى سعر 🔥</b>",
            "💥 <b>سعرها خيالي متتفوتش هبال 🔥</b>",
            "🪙 <b>تخفيض قوي بالعملات (Coins) صيدة اليوم 🔥🪙</b>",
            "🎯 <b>صيدة ناااار بأفضل سعر ممكن 🔥</b>",
            "🚨 <b>العـــــرض مستمـــــر صيدة اليوم ⚡</b>"
        ]

        if has_points_discount:
            candidates.append("🪙 <b>تخفيض قوي بالعملات (Coins) صيدة اليوم 🔥🪙</b>")

        return candidates[h % len(candidates)]

    def format_coupon_list(
        self,
        coupon_items: List[Dict[str, str]],
        affiliate_url: str,
        promo_name: Optional[str] = "Party Ready Sale"
    ) -> str:
        """
        Builds authentic Algerian coupon bulletin format matching ZedStore & Lody.
        """
        lines = [
            f"📣 <b>كوبونات خاصة بتخفيضات {promo_name} لشهر أكتوبر! 🚨</b>",
            "⏰ <b>تنبيه هام:</b> الكوبونات تبدأ العمل وتتفعل غداً 01 أكتوبر على <b>الساعة 08:00 صباحاً</b> بتوقيت الجزائر 🇩🇿",
            "🔴 <b>احجزوا الكوبونات وطبقوها على الساعة 08:00 صباحاً بالضبط:</b>",
            "الكميات محدودة جداً وتنفد في الدقائق الأولى.. جهز نفسك واغتنم الفرصة! 🏃💨",
            "",
            "✅ <b>قـائمة الكوبونـات المعتمدة:</b>",
            ""
        ]

        for item in coupon_items:
            tier = item.get("tier", "").strip()
            code = item.get("code", "").strip()
            if tier and code:
                lines.append(f"🙏 <b>كـوبون {tier}$ :</b> ⏺ <code>{code}</code>")
            elif code:
                lines.append(f"🙏 <b>كـوبون :</b> ⏺ <code>{code}</code>")

        lines.append("")
        lines.append("⭕️ <b>طريقة حجز الكوبونات وتثبيتها في حسابك (طبقوها غداً على 08:00 صباحاً 🔥👌🏽):</b>")
        lines.append("⚠️ <b>ابدأ دائماً بالكوبونات الكبيرة ($55 ثم $42...)</b> ثم البقية واحداً تلو الآخر باه يبقاو في حسابك طيلة التخفيضات وما يهربلكش الستوك ✅")
        lines.append("🔹 <b>طبقوا الآن كامل الكوبونات على هذا المنتج باه تبقالكم في الحساب (كل الكوبونات مقبولة عليه) ⤵️</b>")
        lines.append("https://s.click.aliexpress.com/e/_c3d8Osgp")
        lines.append("")
        lines.append("😊 <b>بوت مطور للشراء بأفضل سعر وتخفيض العملات :</b>")
        lines.append("👉 t.me/Alilo07BOT")
        lines.append("📢 <b>قناة الصيدات اليومية:</b> @DzAliexpress0")

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
            "😊 <b>بوت مطور للشراء بأفضل سعر وتخفيض العملات :</b>",
            "👉 t.me/Alilo07BOT",
            "📢 <b>قناة الصيدات والصفقات:</b> @DzAliexpress0"
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
                lines.append("📍 خلي البلـــد <b>كــــــوريا 🇰🇷</b>")
            elif "كندا" in country_info or "canada" in c_str or "ca" in c_str:
                lines.append("📍 خلي البلـــد <b>كــــــندا 🇨🇦</b>")
            elif "الجزائر" in country_info or "algeria" in c_str or "dz" in c_str:
                lines.append("📍 بلد الحساب <b>الجزائر 🇩🇿</b>")

        import html
        safe_title = html.escape(title)

        lines.append("")
        lines.append(f"⭐️ <b>{safe_title}</b>")

        if usd_price and usd_price > 0:
            if eur_price and eur_price > 0:
                lines.append(f"💵 <b>السعر :</b> <b>${usd_price:.2f} ({eur_price:.2f}€)</b> 🔥")
            else:
                lines.append(f"💵 <b>السعر :</b> <b>${usd_price:.2f}</b> 🔥")
        else:
            lines.append("💵 <b>السعر :</b> <b>سعر خاص ومخفض</b> 🔥")

        if seller_coupon:
            lines.append(f"🌷 <b>احجــز قسيمــة البــائع :</b> <code>{html.escape(seller_coupon)}</code>")

        if coupon_code:
            lines.append(f"🙏 <b>كـوبون الخصم :</b> ⏺ <code>{html.escape(coupon_code)}</code>")

        if has_points_discount:
            lines.append("🪙 <b>تخفيض العملات مفعّل عبر الرابط</b>")

        lines.append("")
        lines.append(f"🔗 <b>رابـــــط المنتـــج :</b>\n{affiliate_url}")

        lines.append("")
        lines.append("😊 <b>بوت مطور للشراء بأفضل سعر وتخفيض العملات :</b>")
        lines.append("👉 t.me/Alilo07BOT")
        lines.append("📢 <b>قناة الصيدات والصفقات:</b> @DzAliexpress0")

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
