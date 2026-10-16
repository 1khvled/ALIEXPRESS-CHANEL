import pytest
from app.ai.generator import caption_generator
from app.aliexpress.parser import extract_country_instruction, extract_seller_coupon, detect_deal_type

@pytest.mark.asyncio
async def test_no_auto_canada_on_normal_item():
    """Ensure normal deals NEVER have Auto-Canada added."""
    caption = await caption_generator.generate(
        title="Baseus 65W GaN Charger",
        usd_price=18.50,
        affiliate_url="https://s.click.aliexpress.com/e/_test",
        deal_type="item"
    )
    assert "كندا" not in caption
    assert "🇨🇦" not in caption
    assert "18.50" in caption
    assert not caption.startswith(".50")

@pytest.mark.asyncio
async def test_saudi_arabia_detected_and_formatted():
    """Ensure deals with Saudi instructions keep Saudi Arabia and no Canada."""
    raw = """🔥 سعر ممتاز
ضع البلد السعودية 🇸🇦
Anker 511 Nano Pro 30W
السعر : 14.07$
كوبون: WOAE02"""
    country = extract_country_instruction(raw)
    assert country == "السعودية 🇸🇦"
    caption = await caption_generator.generate(
        title="Anker 511 Nano Pro 30W",
        usd_price=14.07,
        affiliate_url="https://s.click.aliexpress.com/e/_test",
        coupon_code="WOAE02",
        country_info=country,
        raw_text=raw
    )
    assert "السعوديـــــة 🇸🇦" in caption or "السعودية 🇸🇦" in caption
    assert "كندا" not in caption
    assert "14.07" in caption
    assert "WOAE02" in caption

@pytest.mark.asyncio
async def test_seller_coupon_and_regular_coupon_both_present():
    """Ensure seller voucher and promo coupon are both included."""
    raw = """realme 15 5G
السعر: 231.90$
قسيمة البائع 60$ (كود: GCA84Y)
كوبون: WOAE35"""
    caption = await caption_generator.generate(
        title="realme 15 5G",
        usd_price=231.90,
        affiliate_url="https://s.click.aliexpress.com/e/_test",
        coupon_code="WOAE35",
        seller_coupon="60$ (كود: GCA84Y)",
        raw_text=raw
    )
    assert "231.90" in caption
    assert "GCA84Y" in caption
    assert "WOAE35" in caption
    assert "كندا" not in caption
