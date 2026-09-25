import pytest
from app.deals.scorer import deal_scorer

def test_full_confidence_deal_scoring():
    score = deal_scorer.score(
        url_valid=True,
        product_id="1005001234567890",
        current_price=29.99,
        title="Wireless Gaming Mouse",
        image_url="https://ae01.alicdn.com/kf/S12345.jpg",
        has_discount=True,
        coupon_code="GAMER5"
    )
    # 20 + 20 + 15 + 15 + 10 + 10 + 10 = 100
    assert score == 100
    assert deal_scorer.is_auto_publishable(score)

def test_partial_deal_scoring():
    # Deal with url, price, title, but no image, coupon, or points
    score = deal_scorer.score(
        url_valid=True,
        product_id="1005001234567890",
        current_price=12.50,
        title="USB C Hub Multiport",
        image_url=None,
        has_discount=False,
        coupon_code=None
    )
    # 20 (url) + 20 (price) + 15 (title) + 10 (product_id) = 65
    assert score == 65
    assert deal_scorer.is_acceptable(score)
    assert not deal_scorer.is_auto_publishable(score)
