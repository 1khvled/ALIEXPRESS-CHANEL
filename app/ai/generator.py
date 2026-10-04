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
        is_price_drop: bool = False,
        is_restock: bool = False
    ) -> str:
        """
        Generates authentic Algerian Telegram deal channel hooks.
        Dynamically detects restocks/returns, subcategories (Gaming, Audio, Storage, Power, Wearables),
        and price-drop drops.
        """
        h = int(hashlib.md5(title.encode()).hexdigest(), 16)

        # 1. Restock / Return Repost Hook
        if is_restock:
            restock_hooks = [
                "⚡ <b>العرض رجع توفر من جديد.. حبات قلال سارعوا! 🚨🔥</b>",
                "🔥 <b>رجوع التوفر بسعر لافار ممتاز متفوتوهش 🏃‍♂️⚡</b>",
                "🚨 <b>رجع توفر بكمية محدودة بسعر باطل متتراطاش! 🔥</b>",
                "⚡ <b>الحق توفر من جديد قبل نفاذ الكمية 🔥🏃‍♂️</b>"
            ]
            return restock_hooks[h % len(restock_hooks)]

        # 2. Price-Drop Arbitrage Hook
        if is_price_drop:
            price_drop_hooks = [
                "📉 <b>نزول إضافي في السعر.. لافار ممتازة استغلوها! 🔥</b>",
                "⚡ <b>السعر زاد طاح.. تخفيض إضافي بأقوى سعر 🔥</b>",
                "💥 <b>هبوط قوي في السعر.. سعر باطل لافار 📉🔥</b>"
            ]
            return price_drop_hooks[h % len(price_drop_hooks)]

        # 3. High-Impact Deal Candidates (Versatile, authentic Algerian deal phrasing)
        # Keeps the fire and batel energy toned down without shouting or random category hallucinations
        candidates = [
            "🔥 <b>لافار ممتازة بأقوى سعر 🔥</b>",
            "⚡ <b>تخفيض قوي بسعر باطل متتراطاش 🔥</b>",
            "🔥 <b>سعر ممتاز لافار نهار اليوم 🔥⚡</b>",
            "🌟 <b>تخفيض قوي بأفضل سعر متاح 🔥</b>",
            "⚡ <b>أقوى تخفيض نهار اليوم باطل 🔥</b>",
            "🔥 <b>لافار حقيقية وتخفيض ممتاز 🔥⚡</b>",
            "💥 <b>تخفيض استثنائي بسعر ممتاز متتراطاش 🔥</b>",
            "⚡ <b>عرض اليوم بسعر باطل لافار 🔥</b>",
            "🔥 <b>سعر خيالي لافار متتفوتش نهار اليوم 🔥⚡</b>",
            "🌟 <b>سعر لافار ممتاز استغلوه الآن 🔥</b>",
            "⚡ <b>مواصفات قوية وسعر لافار ممتاز متتراطاش 🔥⚡</b>"
        ]

        if has_points_discount:
            candidates.append("🪙 <b>تخفيض قوي بالعملات (Coins) بسعر باطل 🔥🪙</b>")
            candidates.append("🪙 <b>لافار ممتازة بتخفيض العملات متتراطاش 🔥⚡</b>")

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
        lines.append(affiliate_url)
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
        is_restock: bool = False,
        coin_url: Optional[str] = None,
        deal_type: str = "coin",
        raw_text: Optional[str] = None
    ) -> str:
        lines = []

        # 1. Authentic Algerian Deal Hook
        if deal_type == "bundle":
            h = int(hashlib.md5(title.encode()).hexdigest(), 16)
            if is_restock:
                hook = "⚡ <b>عروض الحزم رجعت توفرت.. حبات قلال متتراطاش! 🔥📦</b>"
            else:
                bundle_hooks = [
                    "🔥 <b>عروض الحزم Bundle Deals بسعر ممتاز متتراطاش 🔥📦</b>",
                    "🛍️ <b>لافاار عروض الحزم 3 قطع بسعر باطل 🔥⚡</b>",
                    "⚡ <b>تخفيض قوي في عروض الحزم 3 قطع بأقوى سعر 🔥</b>",
                    "📦 <b>عروض الحزم (Choice Bundle) لافار ممتازة باطل 🔥⚡</b>"
                ]
                hook = bundle_hooks[h % len(bundle_hooks)]
        else:
            hook = self._select_smart_hook(
                title=title,
                usd_price=usd_price,
                has_points_discount=has_points_discount,
                has_coupon=bool(coupon_code or seller_coupon),
                promo_tag=None,
                is_price_drop=is_price_drop,
                is_restock=is_restock
            )
        lines.append(f"<blockquote>{hook}</blockquote>")

        if deal_type == "bundle":
            lines.append("<blockquote>📦 <b>تنبيه عروض الحزم:</b> يجب إضافة 3 قطع إلى السلة للاستفادة من هذا السعر والشحن المجاني! 🛍️</blockquote>")

        if is_restock:
            lines.append("<blockquote>⚡ <b>تنبيه:</b> العرض رجع توفر بكمية محدودة.. سارع قبل النفاذ! 🏃‍♂️💨</blockquote>")

        if is_price_drop:
            lines.append("<blockquote>📉 <b>انخفاض السعر:</b> السعر نزل أكثر من قبل، لافار حقيقية استغلها الآن! 🔥</blockquote>")

        # 2. Country recommendation (exact Algerian Telegram style in blockquote)
        if country_info:
            c_str = str(country_info).lower()
            if "كوريا" in country_info or "korea" in c_str or "kr" in c_str:
                lines.append("<blockquote>📍 خلي البلـــد <b>كــــــوريا 🇰🇷</b></blockquote>")
            elif "كندا" in country_info or "canada" in c_str or "ca" in c_str:
                lines.append("<blockquote>📍 خلي البلـــد <b>كــــــندا 🇨🇦</b></blockquote>")
            elif "أوكرانيا" in country_info or "اوكرانيا" in country_info or "ukraine" in c_str or "ua" in c_str:
                lines.append("<blockquote>📍 خلي البلـــد <b>أوكرانيـــــا 🇺🇦</b></blockquote>")
            elif "استراليا" in country_info or "أستراليا" in country_info or "australia" in c_str or "au" in c_str:
                lines.append("<blockquote>📍 خلي البلـــد <b>أستراليـــــا 🇦🇺</b></blockquote>")
            elif "الجزائر" in country_info or "algeria" in c_str or "dz" in c_str:
                lines.append("<blockquote>📍 بلد الحساب <b>الجزائر 🇩🇿</b></blockquote>")
            else:
                lines.append(f"<blockquote>📍 خلي البلـــد <b>{html.escape(str(country_info))}</b></blockquote>")
        elif deal_type == "bundle":
            # Bundle deals can be Algeria or Canada depending on source
            is_dz = False
            if raw_text and any(k in raw_text.lower() for k in ["الجزائر", "algeria", "dz", "ديرو الجزائر", "بلاد الجزائر", "حساب جزائري"]):
                is_dz = True
            if is_dz:
                lines.append("<blockquote>📍 بلد الحساب <b>الجزائر 🇩🇿</b></blockquote>")
            else:
                lines.append("<blockquote>📍 خلي البلـــد <b>كــــــندا 🇨🇦</b></blockquote>")
        elif deal_type == "coin":
            # Coin deals in Algerian community default to Canada for 50-70%+ coin discounts
            lines.append("<blockquote>📍 خلي البلـــد <b>كــــــندا 🇨🇦</b></blockquote>")

        import html

        # 2.5 Local price comparison quote if mentioned in source
        if raw_text:
            clean_raw = re.sub(r'[\u064B-\u065F\u0640]', '', raw_text)
            p_quote = re.search(r'(?:سعرو|سعرها|سعره)\s*(?:حاليا|هنا|فالبلاد|في البلاد)\s*(?:في البلاد|فالبلاد)?\s*فوق\s*([0-9\s\.,]+(?:دج|مليون|ألف|الف|سنتيم)?)', clean_raw)
            if p_quote:
                matched_quote = p_quote.group(0).strip()
                lines.append(f"<blockquote>🏷️ <b>سعر السوق المحلي:</b> {html.escape(matched_quote)} 🛒</blockquote>")
        safe_title = html.escape(title)

        lines.append("")
        lines.append(f"✅ <b>{safe_title}</b>")
        lines.append("")

        if usd_price and usd_price > 0:
            lines.append(f"💰 <b>السعر :</b> <b>${usd_price:.2f}</b> 🔥")
        else:
            lines.append("💰 <b>السعر :</b> <b>سعر خاص ومخفض</b> 🔥")

        if seller_coupon and str(seller_coupon).strip() not in {"0", "0$", "$0", "None", ""}:
            s_clean = str(seller_coupon).strip()
            if s_clean.isdigit():
                s_clean = f"{s_clean}$"
            lines.append(f"🌷 <b>قسيمــة البــائع :</b> <code>{html.escape(s_clean)}</code>")

        if coupon_code:
            lines.append(f"🎟️ <b>كـوبون الخصم :</b> <code>{html.escape(coupon_code)}</code>")

        if deal_type == "bundle":
            lines.append("📦 <b>عروض الحزم (Choice Bundle) — يجب إضافة 3 قطع</b>")
        elif has_points_discount:
            lines.append("🪙 <b>تخفيض العملات مفعّل عبر الرابط</b>")

        lines.append("")
        if deal_type == "bundle":
            lines.append("🛒 <b>رابط الباندل (Bundle Deals) ⤵️</b>")
        else:
            lines.append("🛒 <b>رابط الشراء ⤵️</b>")
        lines.append(affiliate_url)

        lines.append("")
        lines.append("📢 @DzAliexpress0")

        return "\n".join(lines)

    async def generate(
        self,
        title: str = "",
        usd_price: Optional[float] = None,
        eur_price: Optional[float] = None,
        affiliate_url: str = "",
        coupon_code: Optional[str] = None,
        seller_coupon: Optional[str] = None,
        has_points_discount: bool = False,
        country_info: Optional[str] = None,
        coupon_list: Optional[List[Dict[str, str]]] = None,
        promo_tag: Optional[str] = None,
        is_price_drop: bool = False,
        is_restock: bool = False,
        coin_url: Optional[str] = None,
        raw_text: Optional[str] = None,
        deal_type: str = "coin"
    ) -> str:
        """
        Generates authentic Algerian Telegram channel caption.
        """
        if not is_restock and raw_text:
            from app.aliexpress.parser import detect_restock_deal
            is_restock = detect_restock_deal(raw_text)

        if not is_price_drop and raw_text:
            from app.aliexpress.parser import detect_price_drop_deal
            is_price_drop = detect_price_drop_deal(raw_text)

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
            is_restock=is_restock,
            coin_url=coin_url,
            deal_type=deal_type,
            raw_text=raw_text
        )

caption_generator = DealCaptionGenerator()
