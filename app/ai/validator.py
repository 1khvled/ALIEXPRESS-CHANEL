from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ValidationResult:
    approved: bool
    errors: List[str]

class DealCaptionValidator:
    REQUIRED_HEADER = "العرض مستمر 🚨"
    REQUIRED_CTA = "لا تنسى استخدام البوت للشراء بأقل الأسعار"

    def validate(
        self,
        caption: str,
        expected_title: str,
        expected_usd_price: float,
        expected_eur_price: float,
        expected_affiliate_url: str,
        expected_coupon: Optional[str] = None,
        expected_points: bool = False
    ) -> ValidationResult:
        """
        Validates the generated caption against verified deal fields.
        Flags hallucinations, price discrepancies, or missing structural elements.
        """
        errors = []

        if not caption:
            return ValidationResult(approved=False, errors=["Caption is empty"])

        # 1. Header check
        if self.REQUIRED_HEADER not in caption:
            errors.append(f"Missing required header '{self.REQUIRED_HEADER}'")

        # 2. Price verification
        expected_usd_str = f"{expected_usd_price:.2f}"
        if expected_usd_str not in caption and f"{expected_usd_price:.1f}" not in caption:
            errors.append(f"USD price {expected_usd_price} not found in caption")

        expected_eur_str = f"{expected_eur_price:.2f}"
        if expected_eur_str not in caption and f"{expected_eur_price:.1f}" not in caption:
            errors.append(f"EUR price {expected_eur_price} not found in caption")

        # 3. Affiliate URL check
        if expected_affiliate_url not in caption:
            errors.append("Affiliate URL is missing from the caption")

        # 4. Coupon check
        if expected_coupon:
            if expected_coupon not in caption:
                errors.append(f"Coupon code '{expected_coupon}' missing from caption")
        else:
            if "كوبون" in caption:
                errors.append("Unverified coupon line found in caption")

        # 5. Points discount check
        if expected_points:
            if "خصم النقاط" not in caption:
                errors.append("Verified points discount line missing from caption")
        else:
            if "خصم النقاط" in caption:
                errors.append("Unverified points discount found in caption")

        # 6. CTA check
        if self.REQUIRED_CTA not in caption:
            errors.append(f"Mandatory CTA '{self.REQUIRED_CTA}' is missing")

        return ValidationResult(
            approved=len(errors) == 0,
            errors=errors
        )

caption_validator = DealCaptionValidator()
