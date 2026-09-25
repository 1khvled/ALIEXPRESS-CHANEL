import pytest
from app.aliexpress.parser import extract_coupon_list, is_spam_or_non_deal
from app.ai.generator import caption_generator
from app.ai.validator import caption_validator

def test_extract_coupon_list():
    sample_text = """
    🎫 الحححححححححححححححق كوبونات متوفرة للجمع
    ✅ حجز الكوبونات اهم من العروووض 😁
    🎟️ كوبـــون 4/35$ : BDQT04
    🎟️ كوبـــون 6/59$ : BDQT06
    🎟️ كوبـــون 10/99$ : BDQT10
    🎟️ كوبـــون 15/139$ : BDQT15 
    🎟️ كوبـــون 30/269$ : BDQT30 
    طريقة حجز الكوبونات هي بالدخول لرابط المنتج 
    🔗 https://s.click.aliexpress.com/e/_c3CD2Ixn
    """
    coupons = extract_coupon_list(sample_text)
    assert len(coupons) == 5
    assert coupons[0]["code"] == "BDQT04"
    assert coupons[0]["tier"] == "4/35$"
    assert coupons[4]["code"] == "BDQT30"
    assert coupons[4]["tier"] == "30/269$"

@pytest.mark.asyncio
async def test_format_and_validate_coupon_list():
    coupons = [
        {"tier": "4/35$", "code": "BDQT04"},
        {"tier": "6/59$", "code": "BDQT06"},
        {"tier": "10/99$", "code": "BDQT10"}
    ]
    aff_url = "https://s.click.aliexpress.com/e/_testpromo"

    caption = await caption_generator.generate(
        title="أحدث كوبونات وتخفيضات AliExpress",
        usd_price=None,
        eur_price=None,
        affiliate_url=aff_url,
        coupon_list=coupons
    )

    assert ("كوبونات" in caption or "كودات التخفيض" in caption)
    assert "BDQT04" in caption
    assert "BDQT06" in caption
    assert "BDQT10" in caption
    assert aff_url in caption
    assert "DealScoutDz" in caption


    val = caption_validator.validate(
        caption=caption,
        expected_title="أحدث كوبونات وتخفيضات AliExpress",
        expected_usd_price=None,
        expected_eur_price=None,
        expected_affiliate_url=aff_url,
        is_coupon_list=True
    )
    assert val.approved

def test_smart_spam_filtering():
    # TEMU post must be filtered
    temu_post = "❗️ عرض موقع تيمو TEMU للحسابات الجديدة كيبورد مغناطيسي"
    is_spam, reason = is_spam_or_non_deal(temu_post)
    assert is_spam is True
    assert "temu" in reason.lower()

    # Short reaction spam must be filtered
    reaction_post = "😭😭"
    is_spam, reason = is_spam_or_non_deal(reaction_post)
    assert is_spam is True

    # Pinned photo announcement without deal
    meta_post = "BND DEALS pinned a photo"
    is_spam, reason = is_spam_or_non_deal(meta_post)
    assert is_spam is True
