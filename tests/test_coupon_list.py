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
    assert ("DealScoutDz" in caption or "بوت" in caption or "@Alilo07BOT" in caption)


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

def test_coupon_bulletin_deduplication():
    from app.publisher.state_tracker import is_coupon_bulletin_already_published, record_coupon_bulletin_published

    test_coupons = [
        {"tier": "4/35$", "code": "TEST04"},
        {"tier": "6/59$", "code": "TEST06"}
    ]
    # Record test bulletin
    record_coupon_bulletin_published(
        promo_name="Test Event 2026",
        coupon_list=test_coupons,
        channel_msg_id=9999
    )

    # Check that subsequent duplicate bulletin is blocked
    is_dup, reason = is_coupon_bulletin_already_published(
        coupon_list=test_coupons,
        promo_name="Test Event 2026"
    )
    assert is_dup is True
    assert "already published" in reason

def test_detect_coupon_event_type_restricted():
    from app.aliexpress.parser import detect_coupon_event_type

    sample_post = """
    🚨 كوبونات حدث Brand Day! 🛍️
    تنطلق غداً 09/10 وتستمر إلى غاية 13/10/2026 🗓️

    🎟️ كوبون 4/35$ : BDQT04
    🎟️ كوبون 6/59$ : BDQT06
    🎟️ كوبون 10/99$ : BDQT10
    🎟️ كوبون 15/139$ : BDQT15
    🎟️ كوبون 30/269$ : BDQT30

    ⚠️ الكوبونات تعمل في بعض المنتجات فقط الموجودة في هذه الصفحة :
    https://s.click.aliexpress.com/e/_c38iyTZR
    """
    res = detect_coupon_event_type(sample_post)
    assert res["is_restricted"] is True
    assert res["is_sitewide_booking"] is False
    assert res["landing_url"] == "https://s.click.aliexpress.com/e/_c38iyTZR"

def test_detect_coupon_event_type_sitewide_booking():
    from app.aliexpress.parser import detect_coupon_event_type

    sample_post = """
    🚨 كوبونات حدث Choice Day! 🛍️
    تنطلق غداً وتستمر إلى غاية 07/11/2026 🗓️

    🎟️ كوبون 4/29$ : CDDZ04
    🎟️ كوبون 7/49$ : CDDZ07
    🎟️ كوبون 12/89$ : CDDZ12

    ⭕️ طريقة حجز الكوبونات وتثبيتها في حسابك (طبقوها غداً على 08:00 صباحاً 🔥👌🏽):
    ⚠️ ابدأ دائماً بالكوبونات الكبيرة ($55 ثم $42...) ثم البقية واحداً تلو الآخر باه يبقاو في حسابك طيلة التخفيضات وما يهربلكش الستوك ✅

    🔹 طبقوا الآن كامل الكوبونات على هذا المنتج باه تبقالكم في الحساب ⤵️
    https://s.click.aliexpress.com/e/_c3d8Osgp
    """
    res = detect_coupon_event_type(sample_post)
    assert res["is_restricted"] is False
    assert res["is_sitewide_booking"] is True

@pytest.mark.asyncio
async def test_format_restricted_vs_sitewide():
    coupons = [
        {"tier": "4/35$", "code": "BDQT04"},
        {"tier": "6/59$", "code": "BDQT06"},
    ]
    aff_url = "https://s.click.aliexpress.com/e/_c3F40Fvf"

    # Restricted format
    restricted_caption = caption_generator.format_coupon_list(
        coupons,
        aff_url,
        promo_name="Brand Day Sale",
        is_restricted_event=True
    )
    assert "⚠️ <b>الكوبونات تعمل في بعض المنتجات فقط الموجودة في هذه الصفحة :</b>" in restricted_caption
    assert aff_url in restricted_caption

    # Sitewide booking format (upcoming)
    sitewide_caption = caption_generator.format_coupon_list(
        coupons,
        aff_url,
        promo_name="Choice Day",
        is_restricted_event=False
    )
    assert ("طريقة حجز الكوبونات وتثبيتها في حسابك" in sitewide_caption or "طريقة التطبيق" in sitewide_caption)

def test_competitor_link_sanitization():
    from api.coin_bot import ensure_affiliate

    # ESK Brand Day link must automatically be sanitized to our affiliate link
    esk_link = "https://s.click.aliexpress.com/e/_c38iyTZR"
    cleaned = ensure_affiliate(esk_link)
    assert cleaned == "https://s.click.aliexpress.com/e/_c3F40Fvf"
    assert "_c38iyTZR" not in cleaned

