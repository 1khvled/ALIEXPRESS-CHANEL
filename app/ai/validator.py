import re
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ValidationResult:
    approved: bool
    errors: List[str]

class DealCaptionValidator:
    SITUATIONAL_HOOKS = [
        "DealScout",
        "سعر ممتاز",
        "ســـعـــر ممت",
        "عرض نااار",
        "ألحق لافار",
        "لافار",
        "نزول قوي في السعر",
        "نـزول قـوي",
        "سعر خيالي",
        "سـعـر خيـالي",
        "عتاد قيمنق",
        "عتـاد قيمنق",
        "تخفيض قوي بالعملات",
        "تخفيض قوي بالكوبون",
        "صفقة اليوم المعتمدة",
        "صفقة قيمنق مختارة",
        "عتاد قيمنق عالي الأداء",
        "توفير فائق بالعملات",
        "أقصى خصم بالعملات",
        "أفضل قيمة مقابل سعر",
        "هبوط قوي في السعر",
        "صفقة كود الخصم",
        "تخفيض مباشر بالكوبون",
        "منتج مختار بعناية",
        "صفقة ممتازة للقيمرز",
        "صفقة قيمنق",
        "صفقة اليوم",
        "صفقة مميزة",
        "لافاااااار",
        "لافاار",
        "لافـــــــــــــــــــــــار",
        "لافـــــــــــــار",
        "الحححححق",
        "الححححححححق",
        "اجججججججري",
        "باطل",
        "bundle deals",
        "عروض الحزم",
        "العرض مستمر",
        "تخفيض عملات",
        "الهواتف",
        "هاتف بمواصفات",
        "مواصفات قوية",
        "سعر باطل",
        "تخفيض إضافي",
        "زاد طاح",
        "عالم الهواتف",
        "أقوى تخفيض",
        "تخفيض قوي",
        "تخفيض استثنائي",
        "سماعات",
        "عالم السماعات",
        "ساعة ذكية",
        "الساعات الذكية",
        "التابلت",
        "أجهزة التابلت",
        "القيمرز",
        "الكوينز",
        "سلعة مليحة",
        "سلعة شابة",
        "براتيك",
        "سومة قهوة",
        "همزة",
        "البيز",
    ]

    def validate(
        self,
        caption: str,
        expected_title: str,
        expected_usd_price: Optional[float],
        expected_eur_price: Optional[float],
        expected_affiliate_url: str,
        expected_coupon: Optional[str] = None,
        expected_points: bool = False,
        is_coupon_list: bool = False
    ) -> ValidationResult:
        """
        Validates the generated caption against verified deal fields.
        Flags hallucinations, price discrepancies, or missing structural elements.
        """
        errors = []

        if not caption:
            return ValidationResult(approved=False, errors=["Caption is empty"])

        # 0. STRICT CORE RULE: Zero tolerance for competitor links, handles, or unauthorized bots!
        from app.aliexpress.urls import check_competitor_contamination
        is_contam, contam_reason = check_competitor_contamination(caption, expected_affiliate_url or "")
        if is_contam:
            errors.append(f"VIOLATION OF CORE RULE: {contam_reason}")

        # 0.1 Competitor affiliate-exclusive deal firewall
        from app.aliexpress.parser import is_affiliate_exclusive_deal
        is_aff, aff_reason = is_affiliate_exclusive_deal(caption)
        if is_aff:
            errors.append(f"VIOLATION OF CORE RULE: {aff_reason}")

        # CTA check
        if "@Alilo07BOT" not in caption and "DealScout" not in caption and "البوت" not in caption and "@DzAliexpress0" not in caption:
            errors.append("Mandatory channel/bot CTA is missing")

        # Affiliate URL check
        if expected_affiliate_url not in caption:
            errors.append("Affiliate URL is missing from the caption")

        # Zero-tolerance: Never post raw unmonetized homepage or naked links
        if "https://www.aliexpress.com" in caption or "http://www.aliexpress.com" in caption:
            errors.append("VIOLATION OF CORE RULE: Raw unmonetized AliExpress homepage link in caption")

        # Specific checks for Coupon List posts
        if is_coupon_list:
            if "كودات" not in caption and "كوبونات" not in caption:
                errors.append("Missing coupon list header")
            return ValidationResult(
                approved=len(errors) == 0,
                errors=errors
            )

        # Specific checks for Single Product Deals
        # 1. Header / Hook check
        # If a situational hook block exists in caption, verify it matches our recognized hooks.
        # When source deals lack hype hooks, generator cleanly omits them per workspace rule.
        first_lines = "\n".join(caption.splitlines()[:3])
        clean_first_lines = re.sub(r'[\u0640]', '', first_lines)
        country_or_meta = [
            "كندا", "كوريا", "أوكرانيا", "اوكرانيا", "الجزائر", "فرنسا", "أستراليا", "استراليا",
            "سعر السوق المحلي", "خلي البلد", "بلد الحساب", "تنبيه"
        ]
        if "<blockquote>" in clean_first_lines and not any(k in clean_first_lines for k in country_or_meta):
            if not any(hook in clean_first_lines for hook in self.SITUATIONAL_HOOKS):
                errors.append("Missing valid situational hook header")

        # 2. Price verification
        if expected_usd_price is not None:
            expected_usd_str = f"{expected_usd_price:.2f}"
            if expected_usd_str not in caption and f"{expected_usd_price:.1f}" not in caption:
                errors.append(f"USD price {expected_usd_price} not found in caption")

        if expected_eur_price is not None and ("€" in caption or "EUR" in caption):
            expected_eur_str = f"{expected_eur_price:.2f}"
            if expected_eur_str not in caption and f"{expected_eur_price:.1f}" not in caption:
                errors.append(f"EUR price {expected_eur_price} not found in caption")

        # 3. Coupon check
        if expected_coupon:
            if expected_coupon not in caption:
                errors.append(f"Coupon code '{expected_coupon}' missing from caption")
        else:
            if "كوبون :" in caption or "كود الخصم:" in caption:
                errors.append("Unverified coupon line found in caption")

        # 4. Points discount check
        if expected_points:
            if "خصم النقاط" not in caption and "تخفيض العملات" not in caption:
                errors.append("Verified points discount line missing from caption")
        else:
            # Check for unverified points discount claimed for the deal itself,
            # excluding the bot promotion CTA (e.g. "@Alilo07BOT", "بوت تخفيض العملات")
            non_bot_lines = [
                l for l in caption.splitlines()
                if "@Alilo07BOT" not in l and "بوت" not in l and "Alilo" not in l
            ]
            non_bot_text = "\n".join(non_bot_lines)
            if "خصم النقاط" in non_bot_text or "تخفيض العملات مفعّل" in non_bot_text or "تخفيض العملات:" in non_bot_text:
                errors.append("Unverified points discount found in caption")

        # 4.5 Multi-coupon sanity check (Single deals must NEVER have 3+ tiered coupon codes)
        coupon_matches = re.findall(r'(?:كوبون|كود|code)[^:\n]*:[^\S\r\n]*([A-Za-z0-9_-]{4,20})', caption, re.IGNORECASE)
        if len(coupon_matches) >= 3:
            errors.append(f"Single deal cannot stack {len(coupon_matches)} coupon codes. Must be a coupon bulletin.")

        # 4.6 Realistic Price Firewall (Flagship smartphones/electronics can never cost < $35)
        if expected_usd_price is not None:
            t_low = (expected_title or "").lower()
            flagship_keywords = [
                "oppo find", "xiaomi 14", "xiaomi 13", "galaxy s", "iphone", "dimensity 9",
                "snapdragon 8", "redmi k", "poco f", "oneplus 1", "oneplus 2", "iqoo 1"
            ]
            if any(k in t_low for k in flagship_keywords) and expected_usd_price < 35.0:
                errors.append(f"Unrealistic dummy/booking price (${expected_usd_price}) for flagship smartphone '{expected_title}'")

        # 5. Category Consistency check (Firewall: non-phones must never be labeled as smartphones)
        from app.ai.category_firewall import is_genuine_smartphone
        if not is_genuine_smartphone(expected_title):
            phone_claims = ["هاتف بمواصفات", "صفقة قوية في الهواتف", "عالم الهواتف"]
            if any(claim in caption for claim in phone_claims):
                errors.append(f"Category mismatch: Caption claims product is a smartphone, but title is not a phone: '{expected_title}'")

        return ValidationResult(
            approved=len(errors) == 0,
            errors=errors
        )

caption_validator = DealCaptionValidator()
