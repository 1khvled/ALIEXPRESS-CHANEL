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
    assert detect_deal_type("ماوس قيمنق", url="https://aliexpress.com/item/123.html?sourceType=620") == "coin"

    # Smartphones, tablets, CPUs must NEVER be bundle deals even with sourceType=620 or bundle keywords
    assert detect_deal_type("OPPO A6 Pro 8/256GB", url="https://aliexpress.com/item/100500123.html?sourceType=620") == "item"
    assert detect_deal_type("POCO M7 (6/128)", url="https://aliexpress.com/item/100500123.html?sourceType=620") == "item"
    assert detect_deal_type("AMD Ryzen 5 7600X USED R5 7600X", url="https://aliexpress.com/item/100500123.html?sourceType=620") == "item"
    assert detect_deal_type("معالج Intel Core i5 12400F", url="https://aliexpress.com/item/100500123.html?sourceType=562") == "item"

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
    assert "€" not in caption
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

def test_france_coupon_and_country_extraction():
    from app.aliexpress.parser import extract_coupon, extract_country_instruction, extract_prices
    sample_text = """
    HONOR 600 EUROPEAN VERSION
    Code -45€ : FRPRD45
    Prix : 289.0€
    Lien : https://s.click.aliexpress.com/e/_oENzM7m
    """
    coupon = extract_coupon(sample_text)
    assert coupon == "FRPRD45"

    country = extract_country_instruction(sample_text)
    assert country == "فرنسا 🇫🇷"

    usd, eur = extract_prices(sample_text)
    assert eur == 289.0

@pytest.mark.asyncio
async def test_france_caption_generator_formatting():
    from app.ai.generator_fr import france_caption_generator
    caption = await france_caption_generator.generate(
        title="POCO F8 Pro 5G Snapdragon 8 Elite",
        eur_price=419.0,
        usd_price=455.43,
        affiliate_url="https://s.click.aliexpress.com/e/_oD34123",
        coupon_code="FRPRD60",
        deal_type="coin",
        has_points_discount=True
    )

    assert "<blockquote>" in caption
    assert "POCO F8 Pro 5G Snapdragon 8 Elite" in caption
    assert "419.00€" in caption
    assert "$455.43" in caption
    assert "🏷️ <b>Code promo :</b> <code>FRPRD60</code>" in caption
    assert "🤐" not in caption
    assert "________________________________" not in caption
    assert "📢 @francedealsdz" in caption
    assert "@Alilo07BOT" in caption


@pytest.mark.asyncio
async def test_france_restock_and_price_drop_caption():
    from app.ai.generator_fr import france_caption_generator

    # 1. Restock caption
    cap_restock = await france_caption_generator.generate(
        title="POCO X6 Pro 5G",
        eur_price=219.0,
        usd_price=238.0,
        affiliate_url="https://s.click.aliexpress.com/e/_test123",
        is_restock=True,
        raw_text="De retour en stock ! Stock limité !"
    )
    assert "Alerte Restock" in cap_restock
    assert "De retour en stock" in cap_restock

    # 2. Price drop caption with retail comparison
    cap_price_drop = await france_caption_generator.generate(
        title="Anker Soundcore Space One",
        eur_price=64.0,
        usd_price=69.5,
        affiliate_url="https://s.click.aliexpress.com/e/_test456",
        seller_coupon="5$",
        raw_text="Baisse de prix importante ! Prix constaté ailleurs : 99€ en magasin"
    )
    assert "Baisse de Prix" in cap_price_drop
    assert "Nouveau prix réduit" in cap_price_drop
    assert "Prix constaté :" in cap_price_drop
    assert "<code>5€</code>" in cap_price_drop


def test_france_deduplication_cooldown_and_exceptions():
    import time
    from scripts.post_france_deals import is_recent_france_duplicate

    mock_state = {
        "published_deals_history": [
            {
                "product_id": "1005001111111",
                "title": "Xiaomi Pad 6 Global",
                "price_eur": 240.0,
                "timestamp": time.time() - 3600  # 1 hour ago
            }
        ]
    }

    # Same price within 24h -> duplicate
    is_dup, reason, is_drop = is_recent_france_duplicate(
        product_id="1005001111111",
        current_price_eur=240.0,
        title="Xiaomi Pad 6 Global",
        raw_text="Xiaomi Pad 6 promo",
        state=mock_state
    )
    assert is_dup is True
    assert "cooldown" in reason

    # Price dropped by 15€ (>4% and >3€) -> allowed through!
    is_dup2, reason2, is_drop2 = is_recent_france_duplicate(
        product_id="1005001111111",
        current_price_eur=225.0,
        title="Xiaomi Pad 6 Global",
        raw_text="Xiaomi Pad 6 promo",
        state=mock_state
    )
    assert is_dup2 is False
    assert is_drop2 is True
    assert "Price drop" in reason2

    # Restock deal -> allowed through!
    is_dup3, reason3, is_drop3 = is_recent_france_duplicate(
        product_id="1005001111111",
        current_price_eur=240.0,
        title="Xiaomi Pad 6 Global",
        raw_text="Alerte Restock ! De retour en stock !",
        state=mock_state
    )
    assert is_dup3 is False
    assert "Restock exception" in reason3


def test_france_tajmi3at_regrouper():
    from app.publisher.regrouper_fr import classify_deal_category, format_france_bulletin

    # Category classification
    assert classify_deal_category("POCO X6 Pro 5G 12/512GB") == "smartphones"
    assert classify_deal_category("GameSir G7 SE Manette Gaming Hall Effect") == "gaming"
    assert classify_deal_category("Anker Soundcore Space Q45 Casque Bluetooth") == "audio"
    assert classify_deal_category("Baseus GaN 65W Chargeur Rapide USB-C") == "tech"

    # Bulletin formatting
    items = [
        {"title": "POCO X6 Pro 5G", "price_eur": 219.0, "channel_msg_id": 101},
        {"title": "Redmi Note 13 Pro+", "price_eur": 289.0, "channel_msg_id": 102},
        {"title": "OnePlus 12R", "price_eur": 450.0, "channel_msg_id": 103}
    ]
    bulletin = format_france_bulletin("smartphones", items)
    assert "Sélection des Meilleurs Smartphones du Jour" in bulletin
    assert "t.me/francedealsdz/101" in bulletin
    assert "t.me/francedealsdz/102" in bulletin
    assert "t.me/francedealsdz/103" in bulletin
    assert "219.00€" in bulletin
    assert "@francedealsdz" in bulletin


@pytest.mark.asyncio
async def test_audio_vs_watch_and_no_corny_hooks():
    from app.ai.generator import caption_generator
    # Haylou S30 is an over-ear ANC headset - must NEVER be classified as watch
    caption = await caption_generator.generate(
        title="Haylou S30 ANC Wireless Bluetooth Headphone Over-Ear Headset 43dB",
        usd_price=24.50,
        affiliate_url="https://s.click.aliexpress.com/e/_testHaylou",
        deal_type="coin"
    )
    assert "ساعة" not in caption
    assert "سوار" not in caption
    assert "صيدة" not in caption
    # Coin deals are always Canada
    assert "كــــــندا 🇨🇦" in caption


@pytest.mark.asyncio
async def test_bundle_country_rules():
    from app.ai.generator import caption_generator
    # Bundle default is Canada
    caption_ca = await caption_generator.generate(
        title="Baseus 65W GaN Charger 3-pack bundle",
        usd_price=12.50,
        affiliate_url="https://s.click.aliexpress.com/e/_bundle1",
        deal_type="bundle"
    )
    assert "كــــــندا 🇨🇦" in caption_ca
    assert "صيدة" not in caption_ca

    # Bundle with Algeria specified is Algeria
    caption_dz = await caption_generator.generate(
        title="Baseus 65W GaN Charger 3-pack bundle",
        usd_price=12.50,
        affiliate_url="https://s.click.aliexpress.com/e/_bundle2",
        deal_type="bundle",
        raw_text="عروض الحزم باندل ديرو بلاد الجزائر 🇩🇿"
    )
    assert "بلد الحساب <b>الجزائر 🇩🇿</b>" in caption_dz


def test_couponsglobal_monitored_channel():
    from app.aliexpress.parser import is_allowed_category
    from scripts.post_recent_deals import CHANNELS
    assert "CouponsGlobal" in CHANNELS
    # Allowed category check accepts couponsglobal
    allowed, _ = is_allowed_category("Random Deal", "Some text", channel_username="CouponsGlobal")
    assert allowed is True

def test_france_channel_never_accepts_arabic_deals():
    from scripts.post_france_deals import is_strictly_france_compatible_deal, FRANCE_SOURCE_CHANNELS

    # 1. Source channels list must ONLY contain verified French channels
    assert "megaphonna" not in FRANCE_SOURCE_CHANNELS
    assert "lodydeals" not in FRANCE_SOURCE_CHANNELS
    assert "aniscoupons" not in FRANCE_SOURCE_CHANNELS
    assert "CouponsGlobal" not in FRANCE_SOURCE_CHANNELS
    assert "AliFRDrop" in FRANCE_SOURCE_CHANNELS
    assert "FranceCP" in FRANCE_SOURCE_CHANNELS

    # 2. Algerian deals or channels must be rejected
    ok1, reason1 = is_strictly_france_compatible_deal("POCO X6 Pro 240$ تخفيض عملات شحن للجزائر 58 ولاية", channel_username="lodydeals")
    assert ok1 is False
    assert "Algerian" in reason1

    ok2, reason2 = is_strictly_france_compatible_deal("هاتف رخيص الدفع بريدي موب دينار جزائري", channel_username="AliFRDrop")
    assert ok2 is False
    assert "Algerian" in reason2

    # 3. Genuine French deals must be accepted
    ok3, _ = is_strictly_france_compatible_deal("POCO X8 PRO MAX 12/512GB Prix : 317€ via PayPal Code : FRLD45", channel_username="AliFRDrop")
    assert ok3 is True

    ok4, _ = is_strictly_france_compatible_deal("HONOR 600 EUROPEAN بسعر 289€ Code -45€ : FRPRD45", channel_username="FranceCP")
    assert ok4 is True

    # 4. Arabic channels dropping an explicit French deal ("عروض ففرنسا") are accepted!
    ok5, reason5 = is_strictly_france_compatible_deal("عروض ففرنسا 🇫🇷🔥 هاتف POCO X6 Pro بسعر 219€ كود FRPRD45", channel_username="megaphonna")
    assert ok5 is True
    assert "Explicit French drop" in reason5

    # 5. Arabic channels with normal Algerian deals are rejected from France
    ok6, reason6 = is_strictly_france_compatible_deal("عرض خيالي هاتف ريدمي نوت 13 شحن للجزائر بسعر 149$ تخفيض عملات", channel_username="megaphonna")
    assert ok6 is False
    assert "without explicit France markers" in reason6




