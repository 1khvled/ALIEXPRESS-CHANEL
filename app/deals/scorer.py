from typing import Optional
from app.config.settings import settings

class DealScorer:
    def __init__(
        self,
        min_score: Optional[int] = None,
        auto_score: Optional[int] = None
    ):
        self.min_score = min_score or settings.MIN_QUALITY_SCORE
        self.auto_score = auto_score or settings.AUTO_PUBLISH_QUALITY_SCORE

    def score(
        self,
        url_valid: bool,
        product_id: Optional[str],
        current_price: Optional[float],
        title: Optional[str],
        image_url: Optional[str],
        has_discount: bool = False,
        coupon_code: Optional[str] = None
    ) -> int:
        """
        Calculates confidence score (0 - 100) based on verified deal attributes.
        """
        total = 0

        # URL validity
        if url_valid:
            total += 20

        # Price availability
        if current_price is not None and current_price > 0:
            total += 20

        # Title recognizable and non-generic
        if title and len(title.strip()) >= 5:
            total += 15

        # Image available
        if image_url:
            total += 15

        # Discount or points information found
        if has_discount:
            total += 10

        # Coupon code present
        if coupon_code:
            total += 10

        # Clean product_id resolved
        if product_id:
            total += 10

        return min(total, 100)

    def is_acceptable(self, score: int) -> bool:
        return score >= self.min_score

    def is_auto_publishable(self, score: int) -> bool:
        return score >= self.auto_score

deal_scorer = DealScorer()
