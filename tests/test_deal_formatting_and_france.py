import pytest
from app.aliexpress.parser import is_france_deal, detect_deal_type
from app.ai.generator import caption_generator
from app.ai.validator import caption_validator

def test_is_france_deal_detection():
    # 1. French shipping or France keywords
    assert is_france_deal("عرض حصري توصيل لفرنسا فقط") is True
    assert is_france_deal("Super promo livraison France") is True
    assert is_france_deal("كود فرنسا FR05 متوفر الآن") is True
    assert is_france_deal("عرض عادي", country_info="فرنسا 🇫🇷") is True
    assert is_france_deal("promo", url="https://aliexpress.com/item/123.html?shiptocountry=fr") is True

    # 2. Algerian deals must NOT be flagged as France
    assert is_france_deal("تخفيض كندا 🇨🇦 ماوس قيمنق هبال") is False
    assert is_france_deal("صيدة اليوم في الجزائر 🇩🇿 كيبورد ميكانيكي") is False
    assert is_france_deal("عرض كوريا 🇰🇷 سماعات أصلية") is False

def test_detect_deal_type_bundle_vs_coin():
    # Bundle deals
    assert detect_deal_type("عروض الحزم Choice Bundle 3 قطع بـ 5$") == "bundle"
    assert detect_deal_type("3 قطع بسعر باطل", url="https://aliexpress.com/item/123.html?sourceType=562") == "bundle"
    assert detect_deal_type("رابط الباندل متفوتوش") == "bundle"
    assert detect_deal_type("3items for 4.99$") == "bundle"

    # Smartphone / expensive items should use clean item page, NOT broken coin index
    assert detect_deal_type("هاتف realme P3 5G 8/256 بسعر خيالي مع عملات وكوبون") == "item"
    assert detect_deal_type("Redmi Note 13 Pro 5G تخفيض قوي بالعملات") == "item"

    # Genuine small coin deals
    assert detect_deal_type("ماوس قيمنق تخفيض قوي بالعملات (Coins)") == "coin"

@pytest.mark.asyncio
async def test_clean_algerian_post_formatting():
    caption = await caption_generator.generate(
        title="Attack Shark X3 Pro 8K",
        usd_price=35.50,
        eur_price=32.20,
        affiliate_url="https://s.click.aliexpress.com/e/_Dk12345",
        coupon_code="SHARK3",
        seller_coupon="5$",
        has_points_discount=True,
        country_info="كندا 🇨🇦",
        deal_type="coin"
    )

    # Must contain modern blockquote
    assert "<blockquote>" in caption
    assert "</blockquote>" in caption
    assert "كــــــندا 🇨🇦" in caption
    assert "Attack Shark X3 Pro 8K" in caption
    assert "$35.50" in caption
    assert "32.20€" in caption
    assert "<code>SHARK3</code>" in caption
    assert "<code>5$</code>" in caption
    assert "🛒 <b>رابط الشراء ⤵️</b>" in caption
    assert "📢 @DzAliexpress0" in caption

    # Must NOT have old clutter
    assert "تنبيه : لي يراسلك ويقلك انا ادمن القناة" not in caption
    assert "بوت مطور لشراء بأفضل سعر وتتبع الطرود" not in caption

@pytest.mark.asyncio
async def test_bundle_deal_disclaimer_3_items():
    caption = await caption_generator.generate(
        title="Baseus 65W GaN Charger 3-pack bundle",
        usd_price=12.50,
        eur_price=11.50,
        affiliate_url="https://s.click.aliexpress.com/e/_bundle123",
        deal_type="bundle"
    )

    # Must contain the 3-item requirement disclaimer in blockquote
    assert "تنبيه عروض الحزم" in caption
    assert "يجب إضافة 3 قطع" in caption
    assert "Choice Bundle" in caption

def test_country_instruction_ukraine_and_australia():
    from app.aliexpress.parser import extract_country_instruction
    assert extract_country_instruction("أختر بلد الحساب أوكرانيا 🇺🇦") == "أوكرانيا 🇺🇦"
    assert extract_country_instruction("أضع البلد استراليا 🇦🇺") == "أستراليا 🇦🇺"
