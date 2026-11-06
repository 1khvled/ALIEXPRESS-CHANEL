import html
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
        is_restock: bool = False,
        raw_text: Optional[str] = None
    ) -> str:
        """
        Generates authentic Algerian Telegram deal channel hooks tailored strictly to the product type.
        Uses natural Algerian expressions matching top deal hunters (ZedStore, Lody, BND) with zero AI cringe.
        """
        h = int(hashlib.md5(title.encode()).hexdigest(), 16)

        # 1. Restock / Return Repost Hook
        if is_restock:
            restock_hooks = [
                "🚨 <b>لي كانو يستناو فيه.. العرض رجع توفر وبنفس السعر الشاب! 🏃‍♂️⚡</b>",
                "⚡ <b>راه رجع توفر بحبات قلال.. اجري قبل ما يخلص الستوك! 🚨🔥</b>",
                "🔥 <b>رجوع التوفر بسعر لافار ممتاز متفوتوهش 🏃‍♂️⚡</b>",
                "⚡ <b>العرض رجع توفر من جديد بكمية محدودة سارعوا! 🚨🔥</b>"
            ]
            return restock_hooks[h % len(restock_hooks)]

        # 2. Price-Drop Arbitrage Hook
        if is_price_drop:
            price_drop_hooks = [
                "📉 <b>السعر زاد طاح كثر من قبل.. همزة حقيقية استغلوها درك! 📉🔥</b>",
                "⚡ <b>هبوط إضافي في السعر.. راهي لافار كثر من المرة لي فاتت! 📉⚡</b>",
                "📉 <b>نزول قوي في السعر.. لافار ممتازة استغلوها قبل ما يرجع السعر! 🔥</b>"
            ]
            return price_drop_hooks[h % len(price_drop_hooks)]

        # 3. Subcategory hooks using category firewall
        from app.ai.category_firewall import (
            is_audio_product,
            is_wearable_product,
            is_tablet_product,
            is_gaming_or_pc_product,
            is_genuine_smartphone,
            is_accessory_product
        )

        # 3.1 Accessories, cables, chargers, stands (Zero 'مواصفات قوية')
        if is_accessory_product(title):
            if usd_price and usd_price < 3.0:
                cheap_hooks = [
                    "⚡ <b>سعر باطل أقل من سومة قهوة.. لافار ممتازة استغلوها 🔥☕</b>",
                    "🔥 <b>سلعة مليحة وبسعر رمزي خاوة متتراطاش 🔥👌</b>",
                    "⚡ <b>لافار ممتازة وسعر باطل نهار اليوم 🔥📦</b>"
                ]
                return cheap_hooks[h % len(cheap_hooks)]
            accessory_hooks = [
                "⚡ <b>سلعة براتيك ومفيدة وسعر باطل نهار اليوم 🔥📦</b>",
                "🔥 <b>همزة مليحة بزاف وسعر رمزي استغلوها 🔥⚡</b>",
                "🌟 <b>تخفيض قوي بسعر باطل متتراطاش 🔥</b>",
                "⚡ <b>عرض اليوم بسعر باطل لافار حقيقية 🔥</b>"
            ]
            return accessory_hooks[h % len(accessory_hooks)]

        # 3.2 Audio, Earphones, IEMs
        if is_audio_product(title):
            audio_hooks = [
                "🎧 <b>عشاق الصوت النقي والبيز.. لافار شابة بزاف 🔥🎧</b>",
                "⚡ <b>سماعات بجودة صوت ممتازة وعزل شباب وسعر باطل 🔥⚡</b>",
                "🔥 <b>تخفيض قوي في عالم السماعات.. صوت نقي بسعر لافار 🎧👌</b>"
            ]
            return audio_hooks[h % len(audio_hooks)]

        # 3.3 Smartwatches
        if is_wearable_product(title):
            watch_hooks = [
                "⌚ <b>عشاق الساعات الذكية.. صفقة شابة ومواصفات ممتازة 🔥⌚</b>",
                "⚡ <b>ساعة ذكية بشاشة نقية وبطارية تشد مليح وبسعر لافار 🔥⚡</b>",
                "🔥 <b>تخفيض قوي في الساعات الذكية بأقوى سعر متاح ⌚👌</b>"
            ]
            return watch_hooks[h % len(watch_hooks)]

        # 3.4 Tablets
        if is_tablet_product(title):
            tablet_hooks = [
                "📱 <b>تابلت عملية للقراية والخدمة بسعر لافار ممتاز 🔥⚡</b>",
                "⚡ <b>تخفيض قوي في أجهزة التابلت بأقوى سعر متاح 🔥📱</b>"
            ]
            return tablet_hooks[h % len(tablet_hooks)]

        # 3.5 Gaming gear & PC Components
        if is_gaming_or_pc_product(title):
            gaming_hooks = [
                "🎮 <b>القيمرز وين راكم.. صفقة قوية في هاد العتاد متتفوتش 🔥⚡</b>",
                "⚡ <b>عتاد قيمنق محترم وسعر لافار أقل من السوق بزااف 🔥🎮</b>",
                "🔥 <b>تخفيض قوي للقيمرز.. أداء ممتاز وسعر باطل 🎮👌</b>"
            ]
            return gaming_hooks[h % len(gaming_hooks)]

        # 3.6 Genuine Smartphones
        if is_genuine_smartphone(title):
            phone_hooks = [
                "📱 <b>صفقة قوية في الهواتف.. مواصفات محترمة وسعر لافار 🔥📱</b>",
                "🔥 <b>هاتف بمواصفات قوية وسعر طايح بزاف مقارنة بسوق البلاد 📱🇩🇿</b>",
                "⚡ <b>عرض لافار ممتاز لعشاق الهواتف متتراطاش 🔥📱</b>"
            ]
            return phone_hooks[h % len(phone_hooks)]

        # 3.7 High-Coin Discount Deals
        if has_points_discount:
            coin_hooks = [
                "🪙 <b>الكوينز دايرين حالة في هاد العرض.. هبوط قوي في السعر 🪙🔥</b>",
                "🪙 <b>تخفيض عملات خارق عبر الرابط.. سعر باطل استغلوه 🪙⚡</b>",
                "🪙 <b>سعر هبال بتخفيض العملات.. لافار حقيقية متتراطاش 🪙👌</b>"
            ]
            return coin_hooks[h % len(coin_hooks)]

        # 4. Realistic Fallback for Miscellaneous Deals
        candidates = [
            "🔥 <b>سلعة شابة وبسعر لافار استغلوها نهار اليوم 🔥⚡</b>",
            "⚡ <b>تخفيض قوي وسعر باطل متتراطاش 🔥</b>",
            "🌟 <b>همزة ممتازة بأفضل سعر متاح حالياً 🔥👌</b>",
            "⚡ <b>عرض اليوم بسعر باطل لافار حقيقية 🔥</b>",
            "🔥 <b>سعر ممتاز لافار نهار اليوم متفوتوهاش 🔥⚡</b>"
        ]
        return candidates[h % len(candidates)]

    def format_coupon_list(
        self,
        coupon_items: List[Dict[str, str]],
        affiliate_url: str,
        promo_name: Optional[str] = None,
        is_restricted_event: bool = False
    ) -> str:
        """
        Builds authentic Algerian coupon bulletin format matching ZedStore & Lody.
        Intelligently differentiates between:
        - Special Restricted Promo Events (Brand Day / eligible landing page only).
        - General Site-Wide Promo Events (Choice Day / 11.11 site-wide booking tutorial).
        """
        is_live = False
        start_day_str = "12 أكتوبر"
        try:
            from app.aliexpress.promos import promo_tracker
            active_promo = promo_tracker.get_active_promo()
            if active_promo:
                is_live = True
                if not promo_name or promo_name == "Party Ready Sale":
                    promo_name = active_promo.name_ar or active_promo.name
            else:
                next_p = promo_tracker.get_next_promo()
                if next_p and next_p[0]:
                    target_promo = next_p[0]
                    if not promo_name or promo_name == "Party Ready Sale":
                        promo_name = target_promo.name_ar or target_promo.name
                    months_ar = {1: "جانفي", 2: "فيفري", 3: "مارس", 4: "أفريل", 5: "ماي", 6: "جوان", 7: "جويلية", 8: "أوت", 9: "سبتمبر", 10: "أكتوبر", 11: "نوفمبر", 12: "ديسمبر"}
                    month_name = months_ar.get(target_promo.start_date.month, "نوفمبر")
                    start_day_str = f"{target_promo.start_date.day} {month_name}"
                else:
                    if not promo_name or promo_name == "Party Ready Sale":
                        promo_name = "تخفيضات AliExpress"
        except Exception:
            if not promo_name or promo_name == "Party Ready Sale":
                promo_name = "تخفيضات AliExpress"

        if not is_restricted_event and promo_name and "brand" in promo_name.lower():
            is_restricted_event = True

        if is_restricted_event:
            lines = [
                f"🚨 <b>كوبونات حدث {promo_name}! 🛍️</b>",
                "⏰ <b>تنبيه:</b> الكوبونات شغالة والكميات محدودة.. استغلوا التخفيضات قبل نفادها! 🏃💨",
                "",
                "✅ <b>قـائمة الكوبونـات المعتمدة:</b>",
                ""
            ]
        elif is_live:
            lines = [
                f"📣 <b>كوبونات خاصة بتخفيضات {promo_name}! 🚨🔥</b>",
                "⏰ <b>تنبيه:</b> التخفيضات نشطة الآن والكميات محدودة.. استغلوا الكوبونات قبل نفادها! 🏃💨",
                "",
                "✅ <b>قـائمة الكوبونـات المعتمدة:</b>",
                ""
            ]
        else:
            lines = [
                f"📣 <b>تسريب وحجز كوبونات {promo_name} القادمة! 🚨🔥</b>",
                f"⏰ <b>تنبيه هام:</b> الكوبونات تبدأ العمل وتتفعّل رسمياً يوم <b>{start_day_str} على الساعة 08:00 صباحاً</b> بتوقيت الجزائر 🇩🇿",
                "",
                "✅ <b>قـائمة الكوبونـات المعتمدة:</b>",
                ""
            ]

        for item in coupon_items:
            tier = item.get("tier", "").strip()
            code = item.get("code", "").strip()
            if tier and code:
                tier_clean = tier.replace("$", "").strip()
                lines.append(f"🎟️ <b>كوبون {tier_clean}$ :</b> ⏺ <code>{code}</code>")
            elif code:
                lines.append(f"🎟️ <b>كوبون :</b> ⏺ <code>{code}</code>")

        if is_restricted_event:
            lines.extend([
                "",
                "⚠️ <b>الكوبونات تعمل في بعض المنتجات فقط الموجودة في هذه الصفحة :</b>",
                f"{affiliate_url}",
                "",
                "🪙 <b>بوت مضاعفة تخفيض العملات:</b> @Alilo07BOT",
                "🌐 <b>موقع الصفقات والكوبونات:</b> https://dealscoutgreen.vercel.app/",
                "━━━━━━━━━━━━━━━━━",
                "📢 <b>قناة الصفقات الرسمية:</b> @DzAliexpress0"
            ])
        elif is_live:
            lines.extend([
                "",
                "⭕️ <b>طريقة التطبيق:</b> انسخ الكوبون وطبقه مباشرة في صفحة الدفع للاستفادة من التخفيض ✅",
                "🔹 <b>رابط الشراء وتطبيق الكوبونات ⤵️</b>",
                f"{affiliate_url}",
                "",
                "😊 <b>بوت مطور للشراء بأفضل سعر وتخفيض العملات:</b>",
                "👉 t.me/Alilo07BOT",
                "🌐 <b>موقع الصفقات والكوبونات:</b> https://dealscoutgreen.vercel.app/",
                "📢 <b>قناة الصفقات الرسمية:</b> @DzAliexpress0"
            ])
        else:
            lines.extend([
                "",
                "⭕️ <b>طريقة حجز الكوبونات وتثبيتها في حسابك (طبقوها على 08:00 صباحاً 🔥👌🏽):</b>",
                "⚠️ <b>ابدأ دائماً بالكوبونات الكبيرة ($55 ثم $42...)</b> ثم البقية واحداً تلو الآخر باه يبقاو في حسابك طيلة التخفيضات وما يهربلكش الستوك ✅",
                "",
                "🔹 <b>طبقوا الآن كامل الكوبونات على هذا المنتج باه تبقالكم في الحساب ⤵️</b>",
                f"{affiliate_url}",
                "",
                "😊 <b>بوت مطور للشراء بأفضل سعر وتخفيض العملات:</b>",
                "👉 t.me/Alilo07BOT",
                "🌐 <b>موقع الصفقات والكوبونات:</b> https://dealscoutgreen.vercel.app/",
                "📢 <b>قناة الصفقات الرسمية:</b> @DzAliexpress0"
            ])

        caption = "\n".join(lines)
        if len(caption) > 1020:
            caption = caption[:1015].rstrip() + "..."
        return caption

    def format_event_campaign(
        self,
        raw_text: str,
        affiliate_url: str
    ) -> str:
        """
        Formats AliExpress official event / warm-up announcements in authentic Algerian style.
        Enforces strict <= 1024 char limit for Telegram photo captions.
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
        elif len(main_content) > 550:
            main_content = main_content[:545].rstrip() + "..."

        lines = [
            f"🎉 <b>{main_content}</b>",
            "",
            "🔗 <b>رابط الدخول وتحصيل الكوبونات ⬇️</b>",
            f"{affiliate_url}",
            "",
            "😊 <b>بوت مطور للشراء بأفضل سعر وتخفيض العملات :</b>",
            "👉 t.me/Alilo07BOT",
            "🌐 <b>موقع الصفقات والكوبونات:</b> https://dealscoutgreen.vercel.app/",
            "📢 <b>قناة الصفقات الرسمية:</b> @DzAliexpress0"
        ]
        caption = "\n".join(lines)
        if len(caption) > 1020:
            caption = caption[:1015].rstrip() + "..."
        return caption

    def adapt_source_caption(
        self,
        raw_text: str,
        affiliate_url: str,
        bot_username: str = "Alilo07BOT"
    ) -> str:
        """
        Adapts source channel writing (matching @lodydeals) directly, keeping the exact
        language, structure, and tone while safely replacing the affiliate link and competitor bot.
        """
        lines = raw_text.splitlines()
        cleaned_lines = []
        link_replaced = False
        bot_replaced = False

        channel_patterns = [
            r'@lodydeals', r'@zedstoreonline', r'@aniscoupons', r'@megaphonna',
            r'@bnddeals', r'@ecksdeal', r'@pcgamingpart', r'@couponsglobal',
            r't\.me/lodydeals', r't\.me/zedstoreonline', r't\.me/aniscoupons',
            r't\.me/megaphonna', r't\.me/bnddeals'
        ]

        import re
        for line in lines:
            stripped = line.strip()

            # Skip lines that are solely competitor channel advertisements
            if any(re.search(pat, stripped, re.IGNORECASE) for pat in channel_patterns) and not ("s.click" in stripped or "aliexpress" in stripped):
                continue

            # Replace AliExpress product/affiliate link
            if ("s.click.aliexpress.com" in stripped or "aliexpress.com" in stripped) and not link_replaced:
                new_line = re.sub(r'https?://[^\s]+|s\.click\.aliexpress\.com/[^\s]+', affiliate_url, stripped)
                cleaned_lines.append(new_line)
                link_replaced = True
                continue
            elif ("s.click.aliexpress.com" in stripped or "aliexpress.com" in stripped) and link_replaced:
                continue

            # Replace competitor coin bot CTA
            if any(w in stripped.lower() for w in ["bot", "lodycouponsbot", "megasoldebot", "zedcoinsbot"]):
                new_line = re.sub(r'(?:https?://)?t\.me/[A-Za-z0-9_]+bot|@[A-Za-z0-9_]+bot', f"t.me/{bot_username}", stripped, flags=re.IGNORECASE)
                cleaned_lines.append(new_line)
                bot_replaced = True
                continue

            cleaned_lines.append(line)

        # Remove trailing empty lines
        while cleaned_lines and not cleaned_lines[-1].strip():
            cleaned_lines.pop()

        # Make coupon codes copyable with <code> tags (tap-to-copy in Telegram)
        final_lines = []
        for line in cleaned_lines:
            stripped = line.strip()
            if any(w in stripped for w in ["كوبون", "قسيمة", "كود", "قسيمـة", "قسيمــة", "code", "Code"]):
                if "<code>" not in stripped and "`" not in stripped:
                    m = re.search(r'([A-Za-z0-9_-]{4,20})\s*([🔥⚡🎉🚨\.\s]*)$', stripped)
                    if m:
                        code = m.group(1)
                        trailing = m.group(2)
                        if any(c.isalpha() for c in code) or len(code) >= 6:
                            prefix = stripped[:m.start(1)]
                            final_lines.append(f"{prefix}<code>{code}</code>{trailing}")
                            continue
            final_lines.append(line)
        cleaned_lines = final_lines

        result = "\n".join(cleaned_lines).strip()

        # If link wasn't found in text, append it
        if not link_replaced:
            result += f"\nالرابط: {affiliate_url}"

        # If bot CTA wasn't present, append standard Lody CTA
        if not bot_replaced:
            result += f"\n\nلا تنسى استخدام البوت للشراء بأقل الأسعار :\nt.me/{bot_username}"

        return result

    def _format_deterministic(
        self,
        title: str,
        usd_price: float,
        eur_price: float,
        affiliate_url: str,
        coupon_code: str = None,
        seller_coupon: str = None,
        has_points_discount: bool = False,
        country_info: str = None,
        promo_tag: str = None,
        is_price_drop: bool = False,
        is_restock: bool = False,
        coin_url: str = None,
        deal_type: str = "item",
        raw_text: str = None
    ) -> str:
        clean_title = title.strip() if title else ""
        clean_title = re.sub(r'^(?:✅|🔥|⚡|📦|🛒|⭐️|📌|Ⓜ|📎|🌷|💵|📱|✔️)\s*', '', clean_title).strip()

        # If title is generic or incomplete, try finding the actual model line in raw_text
        if raw_text and (len(clean_title) < 15 or any(w in clean_title for w in ["الوحش", "نسخة", "هاتف", "جديد", "سعر", "باطل", "لافار"])):
            clean_raw_lines = [re.sub(r'ـ', '', l).strip() for l in raw_text.splitlines() if l.strip()]
            for l in clean_raw_lines:
                l_clean = re.sub(r'^(?:✅|🔥|⚡|📦|🛒|⭐️|📌|Ⓜ|📎|🌷|💵|📱|✔️)\s*', '', l).strip()
                if any(b in l.upper() for b in ['REALME', 'REDMI', 'POCO', 'XIAOMI', 'HONOR', 'VIVO', 'ONEPLUS', 'SAMSUNG', 'IQOO', 'INFINIX', 'TECNO', 'ANKER', 'BASEUS', 'UGREEN', 'LENOVO']):
                    clean_title = l_clean
                    break

        # Taskhinat (Warm-up / Add to cart) header detection matching Lody
        taskhinat_header = None
        if raw_text:
            clean_raw = re.sub(r'ـ', '', raw_text)
            warmup_keywords = [
                "أضف للسلة", "اضف للسلة", "أضف إلى السلة", "اضف إلى السلة", "أضف الى السلة", "اضف الى السلة",
                "دير في السلة", "أضف في السلة", "اضف في السلة", "إحفظ المنشور", "احفظ المنشور",
                "البيع يوم", "البيع يبدأ", "العرض يعمل يوم", "نهار التخفيضات", "تسخينات"
            ]
            if any(k in clean_raw for k in warmup_keywords):
                m_date = re.search(r'(\d+\s*نوفمبر|\d+\s*أكتوبر|\d+\s*ديسمبر)', clean_raw)
                if m_date:
                    date_str = m_date.group(1).strip()
                elif "الأحد" in clean_raw:
                    date_str = "1 نوفمبر"
                else:
                    date_str = "1 نوفمبر"
                # If date is 1 November or past, the sale is actively selling today!
                if date_str != "1 نوفمبر" and "1 نوفمبر" not in date_str:
                    taskhinat_header = f"<blockquote>🛒 أضف للسلة البيع {date_str}</blockquote>"

        lines = []

        if taskhinat_header:
            lines.append(taskhinat_header)
            lines.append("")

        # 1. Clean Lody-style hook
        hook = ""
        if raw_text:
            clean_raw_lines = [re.sub(r'ـ', '', l).strip() for l in raw_text.splitlines() if l.strip()]
            for l in clean_raw_lines:
                if any(w in l for w in ["ممتاز", "مواصفات", "باطل", "لافار", "بطارية", "شاشة", "معالج", "متوافق", "FPS", "PUBG"]):
                    if not any(comp in l.lower() for comp in ["zed", "anis", "mega", "bnd", "ecks", "نصاب"]):
                        if not any(w in l for w in ["أضف", "اضف", "السلة", "البيع"]):
                            hook = l
                            break
        if not hook and not taskhinat_header:
            if is_restock:
                hook = "⚡ عودة العرض توفر من جديد بكمية محدودة (حبات قلال) 🔥"
            elif is_price_drop:
                hook = "📉 انخفاض ممتاز في السعر 🔥"
            elif usd_price and usd_price < 5.0:
                hook = "سعر ممتاز 🔥"
            elif promo_tag:
                hook = f"تخفيضات {promo_tag} 🔥"

        if hook:
            lines.append(hook)
            lines.append("")

        # 2. Product Title (Lody format: تخفيض لـ ...)
        lines.append(f"تخفيض لـ {clean_title}")

        # 3. Price line (Lody format: السعر : X$ (Y€) 🔥)
        if usd_price and usd_price > 0:
            if eur_price and eur_price > 0:
                lines.append(f"السعر : {usd_price:.2f}$ ({eur_price:.2f}€) 🔥")
            else:
                lines.append(f"السعر : {usd_price:.2f}$ 🔥")

        # 4. Link line (Lody format: رابط ...)
        lines.append(f"رابط {affiliate_url}")

        # Points discount (Lody format: خصم النقاط 🪙)
        if has_points_discount or deal_type == "coin" or (raw_text and any(w in raw_text for w in ["نقاط", "العملات", "عملات", "coins", "coin"])):
            lines.append("خصم النقاط 🪙")

        # 5. Extract and format coupons & vouchers (Strictly copyable <code> tags)
        found_coupon = coupon_code
        found_seller = seller_coupon
        if raw_text:
            clean_raw = re.sub(r'ـ', '', raw_text)
            m_seller = re.search(r'(?:قسيمة البائع|كوبون المتجر|من المتجر)[^\n:]*[:\s]+([A-Za-z0-9_\$]+)', clean_raw)
            if m_seller and not found_seller:
                found_seller = m_seller.group(0).strip()
            m_code = re.search(r'(?:كوبون|كود)[^\n:]*[:\s]+([A-Za-z0-9_-]{4,15})', clean_raw)
            if m_code and not found_coupon:
                found_coupon = m_code.group(1).strip()

        if found_seller and str(found_seller).strip() not in {"0", "0$", "$0", "None", ""}:
            s_val = str(found_seller).strip()
            m_code_s = re.search(r'([A-Za-z0-9_\$]{1,20})\s*$', s_val)
            if m_code_s:
                code = m_code_s.group(1)
                prefix = s_val[:m_code_s.start(1)].strip()
                if not prefix or not any(k in prefix for k in ["قسيمة", "كوبون"]):
                    lines.append(f"كوبون المتجر : <code>{code}</code>")
                else:
                    lines.append(f"{prefix} : <code>{code}</code>" if not prefix.endswith(":") else f"{prefix} <code>{code}</code>")
            elif "قسيمة" in s_val:
                lines.append(s_val)
            else:
                lines.append(f"كوبون المتجر : <code>{s_val}</code>")

        if found_coupon and found_coupon != found_seller:
            clean_code = str(found_coupon).strip()
            lines.append(f"كوبون : <code>{clean_code}</code>")

        # 6. Country setting (Lody format: ضع البلد ... من الإعدادات ...)
        if not country_info and raw_text:
            clean_raw = re.sub(r'ـ', '', raw_text)
            m_country = re.search(r'(?:ضع البلد|خلي البلد|بلد الحساب|أختر بلد)[^\n]+', clean_raw)
            if m_country:
                lines.append(m_country.group(0).strip())
        elif country_info:
            c_str = str(country_info).lower()
            flag = "🇦🇺" if any(k in c_str for k in ["aust", "استراليا", "أستراليا"]) else ("🇨🇦" if any(k in c_str for k in ["can", "كندا"]) else ("🇫🇷" if any(k in c_str for k in ["fr", "فرنسا"]) else "🌍"))
            lines.append(f"ضع البلد {country_info} من الإعدادات {flag}")

        # 7. Authentic Lody Footer
        lines.append("")
        lines.append("لا تنسى استخدام البوت للشراء بأقل الأسعار :")
        lines.append("t.me/Alilo07BOT")

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
        deal_type: str = "item"
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
            is_restricted = False
            if raw_text:
                from app.aliexpress.parser import detect_coupon_event_type
                ev_info = detect_coupon_event_type(raw_text, promo_name=promo_tag)
                is_restricted = ev_info.get("is_restricted", False)
            elif promo_tag and "brand" in promo_tag.lower():
                is_restricted = True
            return self.format_coupon_list(coupon_list, affiliate_url, promo_name=promo_tag, is_restricted_event=is_restricted)

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


ALIEXPRESS_URL_RE = re.compile(
    r"(?:https?://)?(?:[a-zA-Z0-9_\-]+\.)*aliexpress\.com/\S+",
    re.IGNORECASE
)


def is_symbol_only(line: str) -> bool:
    """Returns True if the line contains NO Arabic letters, Latin letters, or digits."""
    return not bool(re.search(r'[\u0600-\u06FFa-zA-Z0-9]', line))


def normalize_deal_price_line(line: str) -> str:
    """
    Normalizes price lines with USD and optional EUR:
    - Handles 'السعر : 37.05$ (33.08€)'
    - Handles 'السعر : (36.97€) $41.56'
    - Handles 'السعر: $41.56 (36.97€)'
    - Handles 'السعر : 41.56$ (€36.97)'
    - Injects \u200e before euro parentheses so Telegram BiDi RTL never flips the parentheses!
    """
    m_usd = re.search(r'\$[ \t]*(\d+(?:\.\d+)?)|(\d+(?:\.\d+)?)[ \t]*\$', line)
    usd = (m_usd.group(1) or m_usd.group(2)) if m_usd else ""
    m_eur = re.search(r'(\d+(?:\.\d+)?)[ \t]*€|€[ \t]*(\d+(?:\.\d+)?)', line)
    eur = (m_eur.group(1) or m_eur.group(2)) if m_eur else ""

    if usd and eur:
        return f"السعر : {usd}$ \u200e({eur}€) 🔥"
    elif usd:
        return f"السعر : {usd}$ 🔥"
    return line


def modify_deal_hooks_and_phrasing(caption: str) -> str:
    """
    Subtly modifies competitor hooks and phrasing so posts are not obvious identical clones:
    - Adapts local Algerian market comparisons.
    - Rephrases stock and urgency hooks into engaging Algerian shopping dialect.
    - Turns personal review lines into clean bullet points.
    - Refreshes deal title prefixes.
    """
    caption = re.sub(r'سعرو\s*فالبلاد\s*حوالي\s*(\d+)\s*دج', r'سعره في السوق المحلي حوالي \1 دج', caption)
    caption = re.sub(r'سعرو\s*فالسوق\s*حوالي\s*(\d+)\s*دج', r'في محلاتنا راه يدير حوالي \1 دج', caption)
    caption = re.sub(r'الحح+ق\s*المفقود\s*راه\s*هنا', r'فرصة ذهبية قبل نفاد الكمية', caption)
    caption = re.sub(r'راه\s*يـ+ليكيـ+دي', r'تصفية ستوك وتخفيض جنوني', caption)
    caption = re.sub(r'اجـ+ري', r'سارع قبل نهاية العرض والكمية', caption)
    caption = re.sub(r'أقوى\s*هبوط\s*في\s*السعر', r'هبوط تاريخي وممتاز في السعر', caption)
    caption = re.sub(r'الكاسك\s*راه\s*عندي\s*منذ\s*[^\n]+', r'▫️ منتج مجرب ومضمون 100% ✨', caption)
    caption = re.sub(r'جودة\s*صوت\s*ممتازة', r'▫️ نقاوة صوت وجودة عالية 🎵', caption)
    caption = re.sub(r'عزل\s*الضوضاء\s*بشكل\s*احترافي', r'▫️ عزل ضوضاء احترافي فعال ⚡', caption)
    caption = re.sub(r'^تخفيض\s*لـ\s*', r'تخفيض ممتاز لـ ', caption, flags=re.MULTILINE)
    return caption


def merge_floating_emoji_lines(lines: List[str]) -> List[str]:
    """
    Merges any standalone symbol/emoji lines so they never sit alone on empty lines.
    - Bullets (◀️, ▶️, ▫️, ▪️, 🔹, etc.) prepend to the NEXT text line.
    - Emotion/trailing emojis (🔥, 🚨, 💥, etc.) append to the PREVIOUS text line.
    """
    merged = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            if merged and merged[-1] != "":
                merged.append("")
            i += 1
            continue

        if is_symbol_only(line):
            if any(b in line for b in ["◀️", "▶️", "▫️", "▪️", "🔹", "🔸", "🔴", "📌", "✅", "🏷️", "📦"]):
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines) and lines[j].strip():
                    lines[j] = f"{line} {lines[j].strip()}"
                    i = j
                    continue
                else:
                    i += 1
                    continue
            else:
                k = len(merged) - 1
                while k >= 0 and merged[k] == "":
                    k -= 1
                if k >= 0:
                    if line not in merged[k]:
                        merged[k] = f"{merged[k]} {line}"
                    i += 1
                    continue
                else:
                    j = i + 1
                    while j < len(lines) and not lines[j].strip():
                        j += 1
                    if j < len(lines) and lines[j].strip():
                        lines[j] = f"{lines[j].strip()} {line}"
                        i = j
                        continue

        merged.append(line)
        i += 1
    return merged


def format_lodydeals_caption_1to1(
    raw_text: str,
    affiliate_url: str,
    coupon_code: Optional[str] = None,
    link_mapping: Optional[Dict[str, str]] = None
) -> str:
    """
    Polished formatter for @lodydeals:
    - Retains Algerian deal layout and high-converting structure.
    - Modifies hooks subtly so it's not an obvious clone ("dont cop their caption").
    - Replaces competitor affiliate links with our verified monetized link(s).
    - Strips duplicate/secondary direct links ('مباشر' or naked URLs).
    - Injects \u200e before euro parentheses so Telegram BiDi RTL never flips parentheses.
    - Merges isolated/floating emojis onto proper text lines.
    - Replaces competitor bots with our points bot @Alilo07BOT.
    - Replaces competitor channel mentions with @DzAliexpress0.
    - Normalizes store coupons and wraps promo coupon codes in <code> tags.
    """
    raw_lines = [l.strip() for l in raw_text.splitlines()]
    clean_lines = []
    has_aff = False

    for line in raw_lines:
        if not line:
            clean_lines.append("")
            continue

        # Skip direct competitor channel review links, channel mentions & promo referrals
        competitor_channel_keywords = [
            "lodydeals", "ecksdeal", "zedstoreonline", "aniscoupons", "bnddeals",
            "pcgamingpart", "bnd_deals", "ecks_deal", "anis_coupons", "zed_store"
        ]
        if any(b in line.lower() for b in competitor_channel_keywords) and any(kw in line.lower() for kw in ["t.me/", "@", "قناة", "خاص", "متابعين", "متابعي"]):
            continue

        # Skip secondary link line 'مباشر' and its accompanying url
        if line == "مباشر" or (any(kw in line for kw in ["مباشر", "رابط آخر", "رابط بديل", "بديل", "متجر"]) and ALIEXPRESS_URL_RE.search(line)):
            continue

        # Replace competitor bot mentions with DealScout points bot @Alilo07BOT
        competitor_bot_keywords = [
            "lodycouponsbot", "ecksdealsbot", "zedstoresve_bot", "zedstorebot", "coinsdiscountbot",
            "anisbot", "bndbot", "pcgamingbot", "couponsbot", "ecksbot", "lodybot", "zedbot",
            "dzgamingcoinbot"
        ]
        if any(b in line.lower() for b in competitor_bot_keywords):
            clean_lines.append("t.me/Alilo07BOT")
            continue

        # Skip competitor warning / scam disclaimer slop
        if any(w in line.lower() for w in ["ابلوكيه", "نصاب", "zed store", "zedstore"]):
            continue

        # Replace competitor affiliate links
        if ALIEXPRESS_URL_RE.search(line):
            if link_mapping:
                for orig_url, aff in link_mapping.items():
                    if orig_url in line:
                        line = line.replace(orig_url, aff)
                clean_lines.append(line)
                has_aff = True
            elif not has_aff:
                aff_line = ALIEXPRESS_URL_RE.sub(affiliate_url, line)
                if not aff_line.startswith("رابط") and not aff_line.startswith("الرابط"):
                    aff_line = f"رابط {aff_line}"
                clean_lines.append(aff_line)
                has_aff = True
            else:
                # We already placed the primary affiliate link; skip duplicate / secondary link lines
                continue
            continue

        # Skip orphaned "مباشر" or "الرابط:"
        if has_aff and (line in ["مباشر", "رابط آخر", "رابط بديل", "بديل", "الرابط", "رابط"] or re.match(r"^(?:الرابط|رابط|مباشر)\s*:?$", line)):
            continue

        # Normalize price line with BiDi isolation and clean format
        if any(kw in line for kw in ["السعر", "السعـر", "السعــــر", "Prix"]) and ("$" in line or "€" in line):
            line = normalize_deal_price_line(line)

        clean_lines.append(line)

    # Merge floating emojis onto text lines
    merged_lines = merge_floating_emoji_lines(clean_lines)

    caption = "\n".join(merged_lines).strip()
    caption = re.sub(r'\n{3,}', '\n\n', caption)

    # Subtly modify Algerian hooks so it is not an exact clone
    caption = modify_deal_hooks_and_phrasing(caption)

    # Fix coupon tier ratio: "$4/25" -> "4/25$"
    caption = re.sub(r'\$(\d+/\d+)', r'\1$', caption)

    # Normalize store coupon line
    caption = re.sub(r'(?<!🎫[ \t])(?:احجز|اجمع|إحجز|حصّل|حصل)\s*(?:قسيمة\s*(?:البائع|المتجر))\s*:?\s*\$?\s*(\d+(?:\.\d+)?)\s*\$?', r'🎫 احجز قسيمة البائع: \1$', caption)

    # Normalize promo coupon line
    caption = re.sub(r'(?<!🎟️[ \t])(?:كوبون|كود)[ \t]*(\d+/\d+\$?)[ \t]*:[ \t]*([A-Za-z0-9_-]+)', r'🎟️ كوبون \1 : <code>\2</code>', caption)

    # Wrap promo coupon codes in <code> tags (Strict: must start with prefix AND contain at least one digit)
    code_matches = re.findall(r"\b([A-Z0-9]{4,12})\b", caption)
    for c in code_matches:
        if any(c.startswith(prefix) for prefix in ["OTD", "AE", "AL", "DZ", "FR", "SUN", "ESD", "IFP", "BEST"]) and any(ch.isdigit() for ch in c):
            caption = re.sub(rf"(?<!<code>)\b{c}\b(?!</code>)", f"<code>{c}</code>", caption)

    if coupon_code and coupon_code not in caption:
        caption = re.sub(rf"(?<!<code>)\b{coupon_code}\b(?!</code>)", f"<code>{coupon_code}</code>", caption)

    # Fix truncated model name if ends with broken suffix
    if "USB/XL" in caption and "USB/XLR" not in caption:
        caption = caption.replace("USB/XL", "USB/XLR")

    if affiliate_url not in caption and (not link_mapping or not any(aff in caption for aff in link_mapping.values())):
        caption += f"\nالرابط: {affiliate_url}"

    if "Alilo07BOT" not in caption:
        caption += "\n\n🤖 بوت تخفيض النقاط: @Alilo07BOT\nhttps://t.me/Alilo07BOT"

    if "@DzAliexpress0" not in caption and "DzAliexpress0" not in caption:
        caption += "\n\nقناة التيليغرام للمزيد من العروض : @DzAliexpress0\nhttps://t.me/DzAliexpress0"

    caption = re.sub(r"\n+\s*الرابط\s*:?\s*$", "", caption)

    # Deduplicate repeated emojis on the same line (e.g. 🔥 🔥 -> 🔥)
    for em in ["🔥", "🚨", "💥", "✨", "⚡"]:
        caption = re.sub(rf"(?:{em}[ \t]*)+{em}", em, caption)

    return caption.strip()


def format_multi_deal_tajmi3at_1to1(raw_text: str, link_mapping: Dict[str, str]) -> str:
    """
    Polished Multi-Deal / Tajmi3at Formatter:
    - Merges isolated/floating bullet & emotion emojis onto proper text lines.
    - Fixes BiDi / RTL parentheses and price order inversion.
    - Modifies roundup headers slightly with engaging emojis so it is not an exact copy.
    - Replaces ALL competitor AliExpress URLs with our monetized links from link_mapping.
    - Strips competitor channels & replaces competitor bots with @Alilo07BOT.
    - Wraps coupon codes in <code> tags and formats coupon tiers cleanly.
    - Appends official bot and channel attribution.
    """
    raw_lines = [l.strip() for l in raw_text.splitlines()]
    clean_lines = []

    # 1. Filter competitor mentions and substitute monetized URLs
    for line in raw_lines:
        if not line:
            clean_lines.append("")
            continue

        # Skip direct competitor channel links & scam disclaimers
        if any(b in line.lower() for b in ["t.me/lodydeals", "t.me/ecksdeal", "t.me/zedstoreonline", "t.me/aniscoupons", "t.me/bnddeals"]):
            continue
        if any(w in line.lower() for w in ["ابلوكيه", "نصاب", "zed store", "zedstore"]):
            continue

        # Rewrite competitor channel mentions
        line = re.sub(r'@(?:lodydeals|ECKSDEAL|zedstoreonline|aniscoupons|bnddeals)', '@DzAliexpress0', line, flags=re.IGNORECASE)

        # Replace competitor bot mentions
        competitor_bot_keywords = [
            "lodycouponsbot", "ecksdealsbot", "zedstoresve_bot", "zedstorebot", "coinsdiscountbot",
            "anisbot", "bndbot", "pcgamingbot", "couponsbot", "ecksbot", "lodybot", "zedbot",
            "dzgamingcoinbot", "bnd_hot_deals_coins_bot"
        ]
        if any(b in line.lower() for b in competitor_bot_keywords):
            clean_lines.append("t.me/Alilo07BOT")
            continue

        # Replace AliExpress URLs with verified monetized links
        urls = ALIEXPRESS_URL_RE.findall(line)
        if urls:
            for u in urls:
                clean_u = u.rstrip('.,;)"\'')
                new_u = link_mapping.get(clean_u, link_mapping.get(u, u))
                line = line.replace(u, new_u)

        clean_lines.append(line)

    # 2. Merge floating/isolated emojis so they never sit alone on empty lines
    merged_lines = merge_floating_emoji_lines(clean_lines)

    caption = "\n".join(merged_lines)

    # 3. Clean up version prices (e.g. 'بـ : $43.7' -> 'بسعر: 43.7$ 🔥')
    caption = re.sub(r'بـ[ \t]*:[ \t]*\$[ \t]*(\d+(?:\.\d+)?)', r'بسعر: \1$ 🔥', caption)
    caption = re.sub(r'بـ[ \t]*:[ \t]*(\d+(?:\.\d+)?)[ \t]*\$', r'بسعر: \1$ 🔥', caption)

    # 4. Fix BiDi inverted price parentheses: 'السعر : (36.97€) $41.56' -> 'السعر : 41.56$ \u200e(36.97€) 🔥'
    caption = re.sub(r'السعر[ \t]*:[^\n]+', lambda m: normalize_deal_price_line(m.group(0)), caption)

    # 5. Fix coupon format and wrap in code tags
    caption = re.sub(r'\$(\d+/\d+)', r'\1$', caption)
    caption = re.sub(r'(?<!🎟️[ \t])كوبون[ \t]*(\d+/\d+\$?)[ \t]*:[ \t]*([A-Za-z0-9_-]+)', r'🎟️ كوبون \1 : <code>\2</code>', caption)
    code_matches = re.findall(r"\b([A-Z0-9]{4,12})\b", caption)
    for c in code_matches:
        if any(c.startswith(prefix) for prefix in ["OTD", "AE", "AL", "DZ", "FR", "SUN", "ESD", "IFP", "BEST"]) and any(ch.isdigit() for ch in c):
            caption = re.sub(rf"(?<!<code>)\b{c}\b(?!</code>)", f"<code>{c}</code>", caption)

    # 6. Fix store coupon format
    caption = re.sub(r'(?<!🎫[ \t])(?:احجز|اجمع|إحجز|حصّل|حصل)\s*(?:قسيمة\s*(?:البائع|المتجر))\s*:?\s*\$?\s*(\d+(?:\.\d+)?)\s*\$?', r'🎫 احجز قسيمة البائع: \1$', caption)

    # 7. Modify generic roundup header slightly with engaging styling
    caption = re.sub(r'^(?:أفضل|افضل)\s+العروض\s+في\s+التخزين\s+SSD.*', r'🔥 أقوى عروض وحدات التخزين SSD 💥\n', caption, flags=re.MULTILINE)
    caption = re.sub(r'^(?:أفضل|افضل)\s+العروض\s+في\s+(.*)', r'🔥 أقوى عروض \1 💥\n', caption, flags=re.MULTILINE)

    # 8. Separate product blocks with a blank line before ◀️
    caption = re.sub(r'([^\n])\n(◀️[^\n]+)', r'\1\n\n\2', caption)

    # 9. Ensure official footer attribution
    if "Alilo07BOT" not in caption:
        caption += "\n\n🤖 بوت تخفيض النقاط: @Alilo07BOT\nhttps://t.me/Alilo07BOT"
    if "@DzAliexpress0" not in caption and "DzAliexpress0" not in caption:
        caption += "\n\nقناة التيليغرام للمزيد من العروض : @DzAliexpress0\nhttps://t.me/DzAliexpress0"

    # Deduplicate repeated emojis on the same line (e.g. 🔥 🔥 -> 🔥)
    for em in ["🔥", "🚨", "💥", "✨", "⚡"]:
        caption = re.sub(rf"(?:{em}[ \t]*)+{em}", em, caption)

    caption = re.sub(r'\n{3,}', '\n\n', caption)
    return caption.strip()


def format_competitor_to_lody_1to1(raw_text: str, affiliate_url: str, coupon_code: Optional[str] = None, extracted_title: Optional[str] = None) -> str:
    """
    Transforms incoming posts from ANY competitor channel (ECKSDEAL, ZedStore, AnisCoupons, BNDDeals)
    into Lody's clean, standard, high-converting deal format:
      تخفيض ممتاز لـ [Title]
      السعر : [Price]$ \u200e([EUR]€) 🔥
      رابط [Affiliate URL]
      🎫 احجز قسيمة البائع: [Store Coupon]$
      🎟️ كوبون [Tier]$ : <code>[Code]</code>
      ضع البلد [Country] من الإعدادات [Flag]
      خصم النقاط 🪙

      لا تنسى استخدام البوت للشراء بأقل الأسعار :
      https://t.me/Alilo07BOT

      قناة التيليغرام للمزيد من العروض : @DzAliexpress0
      https://t.me/DzAliexpress0
    """
    clean_raw = re.sub(r'ـ', '', raw_text)

    # 1. Title Extraction
    title = extracted_title or ""
    if not title:
        for l in clean_raw.splitlines():
            l_str = l.strip()
            if any(w in l_str for w in ["تخفيض ل", "عرض ل", "تخفيض لـ", "تخفيض ممتاز لـ", "تخفيض قوي لـ"]):
                title = re.sub(r'.*(?:تخفيض|خفيض|عرض)\s*(?:ممتاز|قوي|خاص)?\s*لـ*[\s:]*', '', l_str).strip()
                break
    if not title:
        for l in clean_raw.splitlines():
            l_str = l.strip()
            if re.search(r'[A-Za-z0-9]', l_str) and not any(kw in l_str.lower() for kw in ["https", "t.me", "السعر", "كوبون", "كود", "قسيمة", "الرابط", "البوت", "قناة", "اعدادات", "إعدادات", "بلد"]):
                cleaned = re.sub(r'^[🚨🔥⚡⭐⭐️✅💎🎫🎟️📎🔗🔸▪️🔹❗️😮😍🙏🌷\-\s:]+', '', l_str).strip()
                cleaned = re.sub(r'(?:💰|💵|السعر|prix|price|[\$€]).*$', '', cleaned).strip()
                if len(cleaned) >= 3:
                    title = cleaned
                    break
    if not title:
        title = "AliExpress Deal"

    title = re.sub(r'^[🚨🔥⚡⭐⭐️✅💎🎫🎟️📎🔗🔸▪️🔹❗️😮😍🙏🌷\-\s:]+', '', title).strip()

    # 2. Price Extraction (USD & EUR with BiDi isolation)
    m_usd = re.search(r'(?:السعر|السعــــر|السعـر|Prix|💰|💵)\s*💲?\s*:?\s*\$?\s*(\d+(?:\.\d+)?)\s*\$?', clean_raw, re.I)
    if not m_usd:
        m_usd = re.search(r'(\d+(?:\.\d+)?)\s*\$', clean_raw)
    price_str = m_usd.group(1) if m_usd else ""

    m_eur = re.search(r'(\d+(?:\.\d+)?)[ \t]*€|€[ \t]*(\d+(?:\.\d+)?)', clean_raw)
    eur_str = (m_eur.group(1) or m_eur.group(2)) if m_eur else ""

    price_line = ""
    if price_str and eur_str:
        price_line = f"السعر : {price_str}$ \u200e({eur_str}€) 🔥"
    elif price_str:
        price_line = f"السعر : {price_str}$ 🔥"

    # 3. Store Coupon (قسيمة البائع)
    store_coupon = ""
    m_store = re.search(r'(?:قسيمة\s*البائع|قسيمــة\s*البــائع|قسيمة\s*المتجر|قسيمة\s*بائع)[^\n\d]*(\$?\d+(?:\.\d+)?\$?)', clean_raw)
    if m_store:
        sc_val = re.sub(r'[\$ ]', '', m_store.group(1).strip())
        store_coupon = f"🎫 احجز قسيمة البائع: {sc_val}$"

    # 4. Promo Coupon
    code = coupon_code or ""
    if not code:
        m_code = re.search(r'(?:كوبون|كود)[^\n:]*[:\s]+([A-Za-z0-9_-]{4,15})', clean_raw)
        if m_code:
            cand = m_code.group(1).strip()
            if any(cand.startswith(p) for p in ["OTD", "AE", "AL", "DZ", "FR", "SUN", "ESD", "IFP", "BEST"]):
                code = cand

    tier_m = re.search(r'(?:كوبون|كود|قسيمة)\s*(\$?\d+\s*/\s*\$?\d+\$?|\d+\$\s*/\s*\d+\$?)', clean_raw)
    tier_str = ""
    if tier_m:
        raw_tier = re.sub(r'[\$ ]', '', tier_m.group(1).strip())
        tier_str = f" {raw_tier}$"

    # 5. Country Setting
    country = ""
    if any(k in clean_raw for k in ["كندا", "canada"]):
        country = "ضع البلد كندا من الإعدادات 🇨🇦"
    elif any(k in clean_raw for k in ["استراليا", "أستراليا", "australia"]):
        country = "ضع البلد استراليا من الإعدادات 🇦🇺"
    elif any(k in clean_raw for k in ["فرنسا", "france"]):
        country = "ضع البلد فرنسا من الإعدادات 🇫🇷"
    elif any(k in clean_raw for k in ["كوريا", "korea"]):
        country = "ضع البلد كوريا من الإعدادات 🇰🇷"

    # 6. Coins
    has_coins = bool(re.search(r'(?:العملات|عملات|نقاط|coins)', clean_raw, re.I))

    lines = []
    lines.append(f"تخفيض ممتاز لـ {title}")
    if price_line:
        lines.append(price_line)
    lines.append(f"رابط {affiliate_url}")
    if store_coupon:
        lines.append(store_coupon)
    if code:
        lines.append(f"🎟️ كوبون{tier_str} : <code>{code}</code>")
    if country:
        lines.append(country)
    if has_coins:
        lines.append("خصم النقاط 🪙")

    lines.append("")
    lines.append("لا تنسى استخدام البوت للشراء بأقل الأسعار :")
    lines.append("https://t.me/Alilo07BOT")
    lines.append("")
    lines.append("قناة التيليغرام للمزيد من العروض : @DzAliexpress0")
    lines.append("https://t.me/DzAliexpress0")

    return "\n".join(lines).strip()


def format_ecksdeal_caption_1to1(raw_text: str, affiliate_url: str, coupon_code: Optional[str] = None) -> str:
    """Compatibility wrapper for @ECKSDEAL posts using standard Lody layout."""
    return format_competitor_to_lody_1to1(raw_text=raw_text, affiliate_url=affiliate_url, coupon_code=coupon_code)
