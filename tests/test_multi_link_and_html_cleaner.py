import pytest
from unittest.mock import patch
from app.aliexpress.parser import extract_telegram_html_text, extract_prices, compute_title_compatibility
from app.aliexpress.product import product_extractor
from bs4 import BeautifulSoup

def test_extract_telegram_html_text_preserves_numbers_and_codes():
    html_raw = """<blockquote>⚡️<b>ألحـــــــــــــــق</b>🚨</blockquote><br/>
⭐️ <b>ATTACK SHARK G300</b><br/><br/>
💵 االسعر  : 1<b>1.7<i class="emoji"><b>💲</b></i><i class="emoji"><b>🔥</b></i></b><br/><br/>
🎟️ كوبـــون 2/15$ : <br/><br/>
👊كوبون 2$:  O<code>TPRD02 </code><br/><br/>
🔗 رابــط  :  <a href="https://s.click.aliexpress.com/e/_c2JpSWfB">https://s.click.aliexpress.com/e/_c2JpSWfB</a><br/>
🔗 مباشر : <a href="https://s.click.aliexpress.com/e/_c3ar3tq9">https://s.click.aliexpress.com/e/_c3ar3tq9</a>"""

    soup = BeautifulSoup(html_raw, "html.parser")
    clean_text = extract_telegram_html_text(soup)

    # Must preserve 11.7 contiguous and OTPRD02 contiguous
    assert "11.7" in clean_text
    assert "OTPRD02" in clean_text

    usd, eur = extract_prices(clean_text)
    assert usd == 11.7
    # Must NOT be 1.7
    assert usd != 1.7

def test_title_compatibility_detects_mismatch():
    post_title = "ATTACK SHARK G300"
    mismatched_api_title = "[World Premiere] POCO X8 5G Smartphone Global Version 8340mAh"
    matching_api_title = "ATTACK SHARK G300 Foldable Wireless Gaming Headset, Active Noise Reduction"

    score_mismatch = compute_title_compatibility(post_title, mismatched_api_title)
    score_match = compute_title_compatibility(post_title, matching_api_title)

    assert score_mismatch == 0.0
    assert score_match >= 0.5

@pytest.mark.asyncio
async def test_multi_link_prefers_matching_product():
    # Message with 2 links: link 1 is wrong phone, link 2 is correct headset
    msg_text = """⭐️ ATTACK SHARK G300
💵 االسعر : 11.7💲🔥
🎟️ كوبون : OTPRD02
🔗 رابط : https://s.click.aliexpress.com/e/_c2JpSWfB
🔗 مباشر : https://s.click.aliexpress.com/e/_c3ar3tq9"""

    from app.aliexpress.resolver import ResolvedUrlResult

    async def mock_resolve(url):
        if "_c2JpSWfB" in url:
            return ResolvedUrlResult(
                original_url=url,
                final_url="https://www.aliexpress.com/item/1005013152491360.html",
                canonical_url="https://www.aliexpress.com/item/1005013152491360.html",
                product_id="1005013152491360",
                is_valid=True
            )
        return ResolvedUrlResult(
            original_url=url,
            final_url="https://www.aliexpress.com/item/1005008390562391.html",
            canonical_url="https://www.aliexpress.com/item/1005008390562391.html",
            product_id="1005008390562391",
            is_valid=True
        )

    with patch("app.aliexpress.resolver.url_resolver.resolve", side_effect=mock_resolve):
        extracted = await product_extractor.extract_from_message(msg_text)
        assert extracted is not None
        # Must select the headset product ID (1005008390562391), NOT POCO phone (1005013152491360)
        assert extracted.product_id == "1005008390562391"
        assert extracted.current_price == 11.7

def test_kz_earphones_controllers_and_keyboards_compatibility():
    from app.aliexpress.parser import is_allowed_category

    # 1. Allowed category checks
    allowed1, _ = is_allowed_category("سماعات الاذن KZ EDX PRO X", "سماعات سلكية احترافية")
    assert allowed1 is True

    allowed2, _ = is_allowed_category("يد تحكم فخمة GameSir G7", "كنترولر بي سي واكسبوكس")
    assert allowed2 is True

    allowed3, _ = is_allowed_category("كيبورد مغناطيسي Attack Shark K85", "كيبورد رابيد تريجر وهول افكت")
    assert allowed3 is True

    allowed4, _ = is_allowed_category("كيبورد ميكانيكي Aula F75", "لوحة مفاتيح ميكانيكية احترافية")
    assert allowed4 is True

    # 2. Title compatibility checks
    # KZ EDX PRO X
    score_kz = compute_title_compatibility(
        "سماعات الاذن KZ EDX PRO X",
        "KZ EDX PRO X In-Ear Earphones Dynamic IEM Earbuds Noise Cancelling HIFI Headset"
    )
    assert score_kz >= 0.4

    # GameSir Controller
    score_ctrl = compute_title_compatibility(
        "يد تحكم فخمة GameSir G7",
        "GameSir G7 SE Wired Controller Gamepad for Xbox PC"
    )
    assert score_ctrl >= 0.4

    # Magnetic Keyboard
    score_mag = compute_title_compatibility(
        "كيبورد مغناطيسي Attack Shark K85",
        "ATTACK SHARK K85 Rapid Trigger Magnetic Switch Gaming Keyboard"
    )
    assert score_mag >= 0.4

    # Mechanical Keyboard
    score_mech = compute_title_compatibility(
        "كيبورد ميكانيكي Aula F75",
        "AULA F75 Wireless Mechanical Keyboard 75% Layout"
    )
    assert score_mech >= 0.4

    # Mismatch rejection
    score_mismatch = compute_title_compatibility(
        "يد تحكم فخمة GameSir G7",
        "Xiaomi Redmi Note 13 4G Smartphone 108MP Camera"
    )
    assert score_mismatch == 0.0

def test_ugreen_webcam_ajazz_mchose_logitech():
    from app.aliexpress.parser import is_allowed_category

    # Category checks
    ok1, _ = is_allowed_category("UGREEN 1080P Webcam 8MP for PC", "كاميرا ويب احترافية للكمبيوتر")
    assert ok1 is True

    ok2, _ = is_allowed_category("ماوس Ajazz AJ159 Apex", "ماوس جيمنج لاسلكي خفيف")
    assert ok2 is True

    ok3, _ = is_allowed_category("Mchose AX5 Pro Max Mouse", "ماوس مغنيسيوم لاسلكي")
    assert ok3 is True

    ok4, _ = is_allowed_category("Logitech G Pro X Superlight 2", "ماوس لوجيتك احترافي")
    assert ok4 is True

    # Title compatibility checks
    score_webcam = compute_title_compatibility(
        "كاميرا ويب UGREEN 1080P Webcam 8MP for PC",
        "UGREEN 1080P 60FPS Webcam with Dual Microphone 8MP AutoFocus for PC Laptop"
    )
    assert score_webcam >= 0.4

    score_ajazz = compute_title_compatibility(
        "ماوس اجاز Ajazz AJ159 Apex",
        "AJAZZ AJ159 APEX Wireless Gaming Mouse PAW3950 8K Polling Rate"
    )
    assert score_ajazz >= 0.4

    score_mchose = compute_title_compatibility(
        "ماوس امشوز Mchose AX5 Pro Max",
        "MCHOSE AX5 Wireless Gaming Mouse Magnesium Alloy Tri-Mode 8K"
    )
    assert score_mchose >= 0.4

    score_logi = compute_title_compatibility(
        "كيبورد لوجيتك Logitech G Pro Keyboard",
        "Logitech G PRO Mechanical Gaming Keyboard RGB Backlit Lightsync"
    )
    assert score_logi >= 0.4

@pytest.mark.asyncio
async def test_coupon_multiline_and_country_priority():
    from app.aliexpress.parser import extract_coupon, extract_seller_coupon
    from app.ai.generator import caption_generator

    # 1. Pcgamingpart multi-emoji with newline formats
    t1 = "🎁💰كوبون 💵:\nOTPRD02\n🎁💰احجز كوبون المتجر 💵:\nKR0864"
    assert extract_coupon(t1) == "OTPRD02"
    assert extract_seller_coupon(t1) == "KR0864"

    t2 = "🎁💰كوبون 💵:\nOTPRD04\n🎁💰احجز كوبون المتجر 💵:4$"
    assert extract_coupon(t2) == "OTPRD04"
    assert extract_seller_coupon(t2) == "4$"

    # 2. Country priority over deal_type == 'coin'
    cap = await caption_generator.generate(
        title="Test Controller",
        usd_price=22.5,
        affiliate_url="https://s.click.aliexpress.com/e/test",
        coupon_code="OTPRD04",
        country_info="كوريا 🇰🇷",
        deal_type="coin",
        has_points_discount=True
    )
    assert "كــــــوريا 🇰🇷" in cap
    assert "كــــــندا 🇨🇦" not in cap
    assert "OTPRD04" in cap
    assert "كـوبون الخصم" in cap



