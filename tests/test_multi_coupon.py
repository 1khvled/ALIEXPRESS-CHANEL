import pytest
from app.aliexpress.parser import extract_multi_coupons, extract_deal_coupons_and_description

def test_extract_various_coupon_formats():
    text = """
    ✅ هاتف شاومي ريدمي نوت 13 برو بلس 5G
    ▫️ شاشة AMOLED منحنية 1.5K 120Hz
    ▫️ كاميرا احترافية 200MP مع مثبت بصري OIS
    ▫️ معالج Dimensity 7200 Ultra
    ▫️ شحن خارق 120W (من 0 إلى 100% في 19 دقيقة)

    السعر: 289$
    كوبون: WOAE20
    كوبون آخر: WOAE30
    كود المتجر: REDMISTORE
    كود: DZ10 / ALIDZ15
    Code promo: PROMO12
    قسيمة: VOUCHER5

    📍 خلي بلد الحساب كندا 🇨🇦
    🔗 رابط الشراء: https://s.click.aliexpress.com/e/_oEN3d53
    بوت العملات: @Alilo07BOT
    قناتنا: @DzAliexpress0
    """
    res = extract_multi_coupons(text)
    
    # 1. All unique codes extracted in order
    assert res["coupons"] == ["WOAE20", "WOAE30", "REDMISTORE", "DZ10", "ALIDZ15", "PROMO12", "VOUCHER5"]
    assert res["coupon_code"] == "WOAE20"
    
    # 2. Structured details
    details = res["coupon_details"]
    assert len(details) == 7
    assert details[0]["code"] == "WOAE20"
    assert "كوبون" in details[0]["label"]
    assert details[1]["code"] == "WOAE30"
    assert "آخر" in details[1]["label"] or "كوبون" in details[1]["label"]
    assert details[2]["code"] == "REDMISTORE"
    assert "المتجر" in details[2]["label"]
    assert details[3]["code"] == "DZ10"
    assert details[4]["code"] == "ALIDZ15"
    assert details[5]["code"] == "PROMO12"
    assert details[6]["code"] == "VOUCHER5"

    # 3. Clean Description
    desc = res["description"]
    assert "https://" not in desc
    assert "s.click" not in desc
    assert "@Alilo07BOT" not in desc
    assert "@DzAliexpress0" not in desc
    assert "رابط الشراء" not in desc
    assert "بوت العملات" not in desc
    assert "200MP" in desc
    assert "Dimensity 7200 Ultra" in desc
    assert "120W" in desc

def test_extract_tiered_coupons():
    text = """
    🎟️ 6/49$ : WOAE06
    🎟️ 12/89$ : WOAE12
    🎟️ 20/159$ : WOAE20
    🎟️ 30/239$ : WOAE30
    """
    res = extract_multi_coupons(text)
    assert res["coupons"] == ["WOAE06", "WOAE12", "WOAE20", "WOAE30"]
    assert res["coupon_code"] == "WOAE06"
    assert res["coupon_details"][0]["tier"] == "6/49$"
    assert res["coupon_details"][1]["tier"] == "12/89$"
    assert res["coupon_details"][2]["tier"] == "20/159$"
    assert res["coupon_details"][3]["tier"] == "30/239$"

def test_blacklist_and_competitor_filtering():
    text = """
    كوبون: ANISDEAL20
    كود آخر: BNDSALE10
    كود المتجر: ZEDSTORE5
    قسيمة: ECKS05
    كود: https://t.me/channel
    كود: item100500123
    كود: camera
    كود: battery
    كوبون: WOAE06
    Code promo: VALIDCODE
    """
    res = extract_multi_coupons(text)
    # Competitor and blacklisted codes must be excluded
    assert "ANISDEAL20" not in res["coupons"]
    assert "BNDSALE10" not in res["coupons"]
    assert "ZEDSTORE5" not in res["coupons"]
    assert "ECKS05" not in res["coupons"]
    assert "CAMERA" not in res["coupons"]
    assert "BATTERY" not in res["coupons"]
    
    assert res["coupons"] == ["WOAE06", "VALIDCODE"]
    assert res["coupon_code"] == "WOAE06"

def test_slashed_and_or_coupons():
    text = """
    كود: FIRST10 / SECOND20 | THIRD30 أو FOURTH40
    """
    res = extract_multi_coupons(text)
    assert res["coupons"] == ["FIRST10", "SECOND20", "THIRD30", "FOURTH40"]

def test_html_tags_and_markdown():
    text = """
    Code promo : <code>PROMO10</code>
    كود الخصم: `MARKDOWN05`
    كوبون: **BOLD15**
    """
    res = extract_multi_coupons(text)
    assert res["coupons"] == ["PROMO10", "MARKDOWN05", "BOLD15"]

def test_legacy_coupon_formats():
    cases = [
        ("🏷️ FR15", "FR15"),
        ("🎟️ DZ10", "DZ10"),
        ("الكود : SUMMER10", "SUMMER10"),
        ("الكوبون : AE05", "AE05"),
        ("Code promo : PROMO20", "PROMO20"),
        ("Utilisez le code : LOVE14", "LOVE14"),
        ("Avec le code : BONPLAN5", "BONPLAN5"),
        ("كـوبون الخصم : DZ15", "DZ15"),
        ("كـود : FAST05", "FAST05"),
        ("Code promo : <code>PROMO10</code>", "PROMO10"),
        ("كود الخصم: <code>DZ25</code>", "DZ25"),
        ("كود: KR0864", "KR0864"),
        ("كوبون: KR0864", "KR0864"),
        ("قسيمة: KR0864", "KR0864"),
    ]
    for inp, expected in cases:
        res = extract_multi_coupons(inp)
        assert res["coupon_code"] == expected, f"Failed on {inp}: got {res['coupon_code']}, expected {expected}"
        assert expected in res["coupons"]

def test_empty_and_noise_text():
    assert extract_multi_coupons("") == {
        "coupons": [],
        "coupon_details": [],
        "coupon_code": None,
        "description": ""
    }
    assert extract_multi_coupons("مجرد منشور بدون أي كوبونات ولا روابط") == {
        "coupons": [],
        "coupon_details": [],
        "coupon_code": None,
        "description": "مجرد منشور بدون أي كوبونات ولا روابط"
    }

def test_lody_saudi_post_regression():
    from app.aliexpress.parser import extract_country_instruction
    text = """
    ✅ شاحن سريع يوجرين 65W GaN
    ▫️ يدعم الشحن السريع PD 3.0 و QC 4.0
    ▫️ 3 منافذ شحن (2x Type-C + 1x USB-A)
    خيار الشاحن لوحده 21.70$
    خيار الشاحن مع كابل 100W بـ 25.40$
    
    السعر: 21.70$
    كوبون $2/15$: WOAE02
    
    ضع البلد السعودية 🇸🇦
    رابط الشراء: https://s.click.aliexpress.com/e/_oBxxxx
    بوت العملات: @Alilo07BOT
    قناتنا: @lodydeals
    """
    country = extract_country_instruction(text)
    assert country == "السعودية 🇸🇦", f"Hallucinated country! Expected 'السعودية 🇸🇦' but got '{country}'"
    
    res = extract_multi_coupons(text)
    assert "WOAE02" in res["coupons"]
    assert res["coupon_code"] == "WOAE02"
    assert res["coupon_details"][0]["tier"] == "$2/15$"
    assert "خيار الشاحن لوحده 21.70$" in res["description"]
    assert "https://" not in res["description"]
    assert "@lodydeals" not in res["description"]

def test_gulf_countries_country_instruction():
    from app.aliexpress.parser import extract_country_instruction
    assert extract_country_instruction("ضع البلد السعودية 🇸🇦") == "السعودية 🇸🇦"
    assert extract_country_instruction("خلي البلد السعودية") == "السعودية 🇸🇦"
    assert extract_country_instruction("country=sa") == "السعودية 🇸🇦"
    assert extract_country_instruction("ضع البلد الإمارات 🇦🇪") == "الإمارات 🇦🇪"
    assert extract_country_instruction("البلد الامارات 🇦🇪") == "الإمارات 🇦🇪"
    assert extract_country_instruction("country=ae") == "الإمارات 🇦🇪"
    assert extract_country_instruction("البلد قطر 🇶🇦") == "قطر 🇶🇦"
    assert extract_country_instruction("البلد الكويت 🇰🇼") == "الكويت 🇰🇼"
    assert extract_country_instruction("البلد البحرين 🇧🇭") == "البحرين 🇧🇭"
    assert extract_country_instruction("البلد عمان 🇴🇲") == "عمان 🇴🇲"
    # General coins / tech without country should still default to Canada
    assert extract_country_instruction("خصم العملات القوي على السلعة") == "كندا 🇨🇦"

def test_parse_telegram_deal_block_saudi():
    from api.index import parse_telegram_deal_block
    from bs4 import BeautifulSoup
    html = """
    <div class="tgme_widget_message" data-post="DzAliexpress0/999">
      <div class="tgme_widget_message_text">
        ✅ شاحن Baseus 65W GaN
        خيار الشاحن لوحده 21.70$
        السعر: 21.70$
        كوبون $2/15$: WOAE02
        كوبون آخر: WOAE06
        ضع البلد السعودية 🇸🇦
        https://s.click.aliexpress.com/e/_oEN3d53
      </div>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    block = soup.find("div", class_="tgme_widget_message")
    deal = parse_telegram_deal_block(block, "DzAliexpress0", 250.0)
    assert deal is not None
    assert deal["country"] == "السعودية 🇸🇦"
    assert deal["coupon_code"] == "WOAE02"
    assert "WOAE02" in deal["coupons"]
    assert "WOAE06" in deal["coupons"]
    assert "خيار الشاحن لوحده 21.70$" in deal["description"]


