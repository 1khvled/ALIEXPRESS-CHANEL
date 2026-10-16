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
    assert any(h in caption for h in ["DealScout", "سعر ممتاز", "ســـعـــر ممت", "عرض نااار", "ألحق لافار", "لافار", "لافاااااار", "قيمنق", "صيدة", "نزول قوي في السعر", "عتاد قيمنق", "عتـاد قيمنق", "تخفيض قوي", "صفقة اليوم المعتمدة", "صفقة قيمنق مختارة", "توفير فائق بالعملات", "أقصى خصم بالعملات", "أفضل قيمة مقابل سعر", "هبوط قوي في السعر", "صفقة كود الخصم", "تخفيض مباشر بالكوبون", "منتج مختار بعناية", "العرض مستمر"])
    assert title in caption
    assert f"${usd:.2f}" in caption
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

@pytest.mark.asyncio
async def test_phone_hook_and_seller_coupon_generation():
    caption = await caption_generator.generate(
        title="REALME 15 5G (12/256)",
        usd_price=214.90,
        eur_price=197.71,
        affiliate_url="https://s.click.aliexpress.com/e/_c4duJlBL",
        coupon_code="OTPRD42",
        seller_coupon="80$ (كود: T0F4TZ)",
        country_info="كندا 🇨🇦",
        raw_text="أجرررررررري لافــــــــــار سعرو حالياً في البلاد فوق 82000دج"
    )

    # Must contain authentic phone hook
    assert any(h in caption for h in ["الهواتف", "أجرررررري لافــــــــــار", "صفقة قوية في الهواتف", "المحبوب", "مواصفات قوية"])
    # Must NOT contain the bad generic million centime hook
    assert "سعرها يفوق مليون سنتيم" not in caption
    # Must contain seller coupon
    assert "قسيمــة البــائع" in caption
    assert "80$ (كود: T0F4TZ)" in caption
    # Must contain coupon
    assert "OTPRD42" in caption
    # Must contain Canada flag
    assert "كــــــندا 🇨🇦" in caption
    assert "82000دج" in caption


@pytest.mark.asyncio
async def test_headphones_and_wearables_never_get_phone_hook():
    # 1. Headphones must NEVER get phone hook
    caption_audio = await caption_generator.generate(
        title="HAYLOU FlowLoop S33 Wireless Headphones 45dB ANC Hi-Res LDAC 100h Playtime",
        usd_price=26.29,
        eur_price=24.18,
        affiliate_url="https://s.click.aliexpress.com/e/_c3DKWzSH",
        coupon_code="WOAE02",
        country_info="كندا 🇨🇦",
        raw_text="قناة ميغافونا @megaphonna سماعات haylou"
    )
    assert "هاتف" not in caption_audio
    assert "الهواتف" not in caption_audio
    assert "📱" not in caption_audio.splitlines()[0]  # First line/hook must not have phone emoji
    assert any(h in caption_audio for h in ["سماعات", "السماعات", "لافار", "تخفيض"])

    # 2. Smartwatch must NEVER get phone hook
    caption_watch = await caption_generator.generate(
        title="HAYLOU Watch Faro Voice Calling Smart Watch",
        usd_price=19.00,
        eur_price=17.50,
        affiliate_url="https://s.click.aliexpress.com/e/_c43QJfHn",
        coupon_code="WOAE02"
    )
    assert "هاتف" not in caption_watch
    assert "الهواتف" not in caption_watch
    assert "ساعة ذكية" in caption_watch or "الساعات الذكية" in caption_watch
