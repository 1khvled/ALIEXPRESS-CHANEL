import pytest
from app.ai.generator import caption_generator
from app.ai.validator import caption_validator

@pytest.mark.asyncio
async def test_generated_caption_format_exact():
    title = "ATTACK SHARK L80 Ultra-Light"
    usd = 20.12
    eur = 17.71
    aff_url = "https://s.click.aliexpress.com/e/_c4MFjazx"
    coupon = "SHARK5"
    has_points = True

    caption = await caption_generator.generate(
        title=title,
        usd_price=usd,
        eur_price=eur,
        affiliate_url=aff_url,
        coupon_code=coupon,
        has_points_discount=has_points
    )

    # Check structural requirements
    assert any(h in caption for h in ["DealScout", "صفقة اليوم المعتمدة", "صفقة قيمنق مختارة", "عتاد قيمنق", "توفير فائق بالعملات", "أقصى خصم بالعملات", "أفضل قيمة مقابل سعر", "هبوط قوي في السعر", "صفقة كود الخصم", "تخفيض مباشر بالكوبون", "منتج مختار بعناية", "العرض مستمر"])
    assert title in caption
    assert f"${usd:.2f}" in caption
    assert f"{eur:.2f}€" in caption
    assert aff_url in caption
    assert f"<code>{coupon}</code>" in caption
    assert ("خصم النقاط" in caption or "تخفيض العملات" in caption)
    assert ("DealScout" in caption or "@DzAliexpress0" in caption)


    # Validate with validator
    validation = caption_validator.validate(
        caption=caption,
        expected_title=title,
        expected_usd_price=usd,
        expected_eur_price=eur,
        expected_affiliate_url=aff_url,
        expected_coupon=coupon,
        expected_points=has_points
    )
    assert validation.approved
    assert len(validation.errors) == 0

def test_validation_catches_hallucinations_and_errors():
    # Caption with wrong price and missing CTA
    bad_caption = (
        "العرض مستمر 🚨\n"
        "تخفيض لـ Test Mouse\n"
        "السعر : 99.99$ (90.00€)🔥\n"
        "رابط https://example.com"
    )

    validation = caption_validator.validate(
        caption=bad_caption,
        expected_title="Test Mouse",
        expected_usd_price=10.00,
        expected_eur_price=9.20,
        expected_affiliate_url="https://example.com",
        expected_coupon=None,
        expected_points=False
    )

    assert not validation.approved
    assert any("price" in err.lower() for err in validation.errors)
    assert any("CTA" in err or "البوت" in err for err in validation.errors)
