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
        t_lower = title.lower()

        # 1. Restock / Return Repost Hook (Highest urgency: "الححق عودة العرض حبات قلال")
        if is_restock:
            restock_hooks = [
                "🚨 <b>الحححححق عودة العرض.. حبات قلال فقط! 🔥🏃‍♂️</b>",
                "⚡ <b>الحقوووو رجع توفر من جديد.. حبات قلال ويسالي! 🚨🔥</b>",
                "🔥 <b>عرض ممتاز رجع توفر بسعر باطل.. كمية محدودة جداً سارع! ⚡</b>",
                "🏃‍♂️💨 <b>الحق عودة العرض لافااار.. بقاو حبات قلال متتراطاش! 🔥</b>",
                "🚨 <b>الححححق توفر من جديد.. الكمية طير في دقائق! 🔥⚡</b>"
            ]
            return restock_hooks[h % len(restock_hooks)]

        # 2. Price-Drop Arbitrage Hook
        if is_price_drop:
            price_drop_hooks = [
                "💥 <b>هبوط قوي في السعر.. ألحـــــق لافــــــــــــــار! 📉🔥</b>",
                "⚡ <b>طاح السعر أكثر.. تخفيض إضافي ناااار 🔥</b>",
                "🔥 <b>نزول إضافي في السعر لافار اليوم متتراطاش 🔥</b>"
            ]
            return price_drop_hooks[h % len(price_drop_hooks)]

        # 2. Category Detection
        is_audio = any(k in t_lower for k in [
            "earphone", "earphones", "earbuds", "earbud", "headphone", "headphones", "headset",
            "tws", "speaker", "soundbar", "soundcore", "qcy", "baseus bowie", "lenovo lp", "anc",
            "bluetooth speaker", "haylou s", "haylou w", "haylou gt", "haylou x", "edifier",
            "earfun", "tronsmart", "fiil", "moondrop", "iem", "kz ", "s30"
        ]) or any(k in title for k in ["سماعة", "سماعات", "صوت", "مكبر صوت", "ايربودز", "سماعه", "كاسك"])

        is_gaming = any(k in t_lower for k in [
            "mouse", "keyboard", "controller", "gamepad", "gaming", "gamer",
            "attack shark", "ajazz", "aula", "vgn", "game", "rgb", "joystick", "switch", "keycap", "fantech"
        ]) or any(k in title for k in ["ماوس", "كيبورد", "جيمنج", "قيمنق", "تحكم", "يدات"])

        is_storage = any(k in t_lower for k in [
            "ssd", "nvme", "m.2", "sata", "ddr4", "ddr5", "ram", "micro sd", "sd card",
            "pendrive", "thermal paste", "cooler", "heatsink", "fan hub"
        ]) or any(k in title for k in ["قرص صلب", "تخزين", "هارد", "رامات", "معجون"])

        is_power = any(k in t_lower for k in [
            "gan", "charger", "fast charge", "65w", "100w", "30w", "45w", "powerbank", "power bank",
            "usb-c", "type-c", "cable", "ugreen", "essager", "toocki", "kuulaa"
        ]) or any(k in title for k in ["شاحن", "كابل", "باور بانك", "شحن سريع"])

        is_watch = (not is_audio) and (any(k in t_lower for k in [
            "smartwatch", "smart watch", "smart band", "miband", "mi band", "band 8", "band 9",
            "zeblaze", "kieslect", "colmi", "amazfit", "haylou watch", "haylou solar", "haylou rs"
        ]) or any(k in title for k in ["ساعة ذكية", "سوار ذكي", "ساعة يد ذكية"]))

        is_phone = any(k in t_lower for k in [
            "phone", "smartphone", "mobile", "redmi", "poco", "xiaomi", "realme", "oneplus",
            "oppo", "vivo", "honor", "infinix", "tecno", "samsung galaxy", "iphone", "pixel",
            "global version", "5g", "snapdragon", "dimensity", "pad", "tablet"
        ]) or any(k in title for k in [
            "هاتف", "موبايل", "جوال", "تابلت", "شاومي", "ريدمي", "بوكو", "ريلمي", "هونر", "سامسونج"
        ])

        if is_phone:
            phone_hooks = [
                "📱 <b>لافاااار جننننح في الهواتف الذكية بسعر ممتاز 🔥📱</b>",
                "⚡ <b>هاتف بمواصفات قوية وسعر لافار متتراطاش 🔥📱</b>",
                "🔥 <b>أجرررررري لافــــــــــار نسخة عالمية أصلية نااار 📱⚡</b>",
                "🌟 <b>عودة العرض بسعر خيالي ممتاز متتراطاش 🔥📱</b>",
                "📱 <b>عرض اليوم في الهواتف بسعر باطل هبال 🔥⚡</b>"
            ]
            return phone_hooks[h % len(phone_hooks)]

        if is_audio:
            audio_hooks = [
                "🎧 <b>صوت نقي وباس قوي وسعر لافار متتراطاش 🔥🎧</b>",
                "🔊 <b>تخفيض ممتاز على السماعات الأصلية جودة صوت هايلة 🔥⚡</b>",
                "🎧 <b>سماعات ممتازة بعزل صوت قوي وسعر باطل 🔥🎧</b>"
            ]
            return audio_hooks[h % len(audio_hooks)]

        if is_gaming:
            return (
                "🎮 <b>لافاااااار قيمنق متتفوتش عتاد بأقوى سعر 🔥🕹️</b>" if (h % 2 == 0)
                else "🕹️ <b>عتاد قيمنق ممتاز بأقوى تخفيض متفوتوش 🔥⚡</b>"
            )

        if is_storage:
            return (
                "💾 <b>تخفيض ممتاز في التخزين والكمبيوتر هبال 🔥⚡</b>" if (h % 2 == 0)
                else "⚡ <b>عتاد كمبيوتر وتخزين بأقوى سعر متتراطاش 🔥</b>"
            )

        if is_power:
            return (
                "🔌 <b>شواحن وكوابل سريعة بسعر باطل هبال 🔥⚡</b>" if (h % 2 == 0)
                else "⚡ <b>تخفيض قوي على ملحقات الشحن الأصلية 🔥</b>"
            )

        if is_watch:
            return (
                "⌚ <b>ساعة ذكية بأناقة ومواصفات قوية وسعر خيالي لافار 🔥</b>" if (h % 2 == 0)
                else "⌚ <b>سعر ممتاز ومواصفات ممتازة لساعة ذكية أنيقة ⚡</b>"
            )

        candidates = [
            "🔥 <b>لافـــــــــــــــــــــــار 🔥</b>",
            "🔥 <b>لافاااار هباااال ناااار 🔥</b>",
            "🔥 <b>الحححححق عودة لافاااار 🔥</b>",
            "⚡ <b>الحححححق باااآآاطل عرض اليوم ⚡</b>",
            "🔥 <b>عرض اليوم بأقوى تخفيض متتراطاش 🔥⚡</b>",
            "🔥 <b>اجججججججري سعـــــر ممتــــــــــــاز 🔥</b>",
            "🚨 <b>الحححححححححق تخفيض نااار ⚡</b>",
            "😍 <b>نسخـة عالميــــــــة بسعر باطل هبال 🔥</b>"
        ]

        if has_points_discount:
            candidates.append("🪙 <b>تخفيض قوي بالعملات (Coins) متتراطاش 🔥🪙</b>")

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
                hook = "🚨 <b>الحححححق عودة عروض Bundle Deals.. حبات قلال فقط! 🔥📦</b>"
            else:
                bundle_hooks = [
                    "🔥 <b>الححححححححق عروض bundle deals متتراطاش 🔥</b>",
                    "📦 <b>عروض الحزم (Choice Bundle) لافار هبااال ناااار 🔥⚡</b>",
                    "⚡ <b>تخفيض ممتاز في عروض الحزم 3 قطع بأقوى سعر 🔥</b>",
                    "🛍️ <b>لافـــــــــــــار عروض الحزم bundle deals باطل 🔥</b>"
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
        if deal_type == "coin":
            # Coin deals in Algerian community are always Canada for 50-70%+ coin discounts
            lines.append("<blockquote>📍 خلي البلـــد <b>كــــــندا 🇨🇦</b></blockquote>")
        elif deal_type == "bundle":
            # Bundle deals can be Algeria or Canada depending on source
            is_dz = False
            if country_info and any(k in str(country_info).lower() for k in ["الجزائر", "algeria", "dz"]):
                is_dz = True
            if raw_text and any(k in raw_text.lower() for k in ["الجزائر", "algeria", "dz", "ديرو الجزائر", "بلاد الجزائر", "حساب جزائري"]):
                is_dz = True
            if is_dz:
                lines.append("<blockquote>📍 بلد الحساب <b>الجزائر 🇩🇿</b></blockquote>")
            else:
                lines.append("<blockquote>📍 خلي البلـــد <b>كــــــندا 🇨🇦</b></blockquote>")
        elif country_info:
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
            if eur_price and eur_price > 0:
                lines.append(f"💰 <b>السعر :</b> <b>${usd_price:.2f} ({eur_price:.2f}€)</b> 🔥")
            else:
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
