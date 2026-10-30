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
                "البيع يوم", "البيع يبدأ", "العرض يعمل يوم", "نهار التخفيضات", "تسخينات", "OTD11"
            ]
            if any(k in clean_raw for k in warmup_keywords):
                m_date = re.search(r'(\d+\s*نوفمبر|\d+\s*أكتوبر|\d+\s*ديسمبر)', clean_raw)
                if m_date:
                    date_str = m_date.group(1).strip()
                elif "الأحد" in clean_raw:
                    date_str = "1 نوفمبر"
                else:
                    date_str = "1 نوفمبر"
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
                hook = "⚡ عودة توفر العرض بكمية محدودة 🔥"
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
            m_code_s = re.search(r'([A-Za-z0-9_\$]{3,20})\s*$', s_val)
            if m_code_s:
                code = m_code_s.group(1)
                prefix = s_val[:m_code_s.start(1)]
                lines.append(f"{prefix}<code>{code}</code>")
            elif "قسيمة" in s_val:
                lines.append(s_val)
            else:
                lines.append(f"قسيمة البائع <code>{s_val}</code>")

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
