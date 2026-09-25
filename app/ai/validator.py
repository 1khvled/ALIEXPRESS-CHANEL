from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ValidationResult:
    approved: bool
    errors: List[str]

class DealCaptionValidator:
    SITUATIONAL_HOOKS = [
        "DealScout",
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
        "صيدة ممتازة للقيمرز",
        "العرض مستمر",
        "تخفيض عملات",
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

        # CTA check
        if "@Alilo07BOT" not in caption and "DealScoutDz" not in caption and "البوت" not in caption:
            errors.append("Mandatory bot CTA is missing")

        # Affiliate URL check
        if expected_affiliate_url not in caption:
            errors.append("Affiliate URL is missing from the caption")

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
        if not any(hook in caption for hook in self.SITUATIONAL_HOOKS):
            errors.append("Missing valid situational hook header")


        # 2. Price verification
        if expected_usd_price is not None:
            expected_usd_str = f"{expected_usd_price:.2f}"
            if expected_usd_str not in caption and f"{expected_usd_price:.1f}" not in caption:
                errors.append(f"USD price {expected_usd_price} not found in caption")

        if expected_eur_price is not None:
            expected_eur_str = f"{expected_eur_price:.2f}"
            if expected_eur_str not in caption and f"{expected_eur_price:.1f}" not in caption:
                errors.append(f"EUR price {expected_eur_price} not found in caption")

        # 3. Coupon check
        if expected_coupon:
            if expected_coupon not in caption:
                errors.append(f"Coupon code '{expected_coupon}' missing from caption")
        else:
            if "كوبون" in caption:
                errors.append("Unverified coupon line found in caption")

        # 4. Points discount check
        if expected_points:
            if "خصم النقاط" not in caption:
                errors.append("Verified points discount line missing from caption")
        else:
            if "خصم النقاط" in caption:
                errors.append("Unverified points discount found in caption")

        return ValidationResult(
            approved=len(errors) == 0,
            errors=errors
        )

caption_validator = DealCaptionValidator()
