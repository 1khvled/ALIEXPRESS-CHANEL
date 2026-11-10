import pytest
from datetime import datetime, timezone, timedelta
from app.aliexpress.parser import is_coupon_claim_post
from app.ai.generator import format_coupon_claim_caption
from app.publisher.state_tracker import (
    is_coupon_restock_time_window,
    is_coupon_restock_alert_eligible,
    record_coupon_restock_alert_published
)

def test_is_coupon_claim_post_detection():
    # 1. Coupon reservation post from competitor
    sample_reservation = """
قد تتوفر الكوبونات من جديد غدا إن شاء الله على الساعة 09h00 صباحًا ، كما يتوقع أن تنخفض الأسعار أكثر يوم 11.11. 
قومو بتغيير البلد إلى الجزائر🇩🇿 ، ثم الدخول إلى الرابط غدا لحجز الكوبونات في حال إعادة توفيرها.
رابط الحجز : https://s.click.aliexpress.com/e/_c4Up4ucr 
رابط آخر : https://s.click.aliexpress.com/e/_c3nBNn5V
بوت تخفيض العملات: t.me/CouponsCoins_bot
"""
    assert is_coupon_claim_post(sample_reservation) is True

    # 2. Morning restock announcement
    sample_morning = """
🔥 توفرت الكوبونات الآن رسمياً على الساعة 9:00 صباحاً!
سارعوا بحجز الكوبونات قبل نفاد الكمية:
رابط صفحة الكوبونات : https://s.click.aliexpress.com/e/_c4Up4ucr
ضع البلد الجزائر 🇩🇿
"""
    assert is_coupon_claim_post(sample_morning) is True

    # 3. Regular single item deal (must NOT be treated as coupon claim)
    sample_item = """
تخفيض ممتاز لـ Baseus 20W PD Charger
السعر : $4.89 (€4.36) 🔥
رابط https://aliexpress.com/item/100500123.html
كوبون 2/15$ : OTD1102
"""
    assert is_coupon_claim_post(sample_item) is False

    # 4. Message without AliExpress link
    sample_no_link = "الكوبونات توفرت الآن ادخلوا احجزوا"
    assert is_coupon_claim_post(sample_no_link) is False

    # 5. Algerian dialect variation (كويونات / ترجع)
    sample_algerian = """
السلام عليكم خاوتي ترجع الكويونات ضرك على 9:00!
ادخلوا ديروا تحصيل من هنا: https://s.click.aliexpress.com/e/_c4Up4ucr
"""
    assert is_coupon_claim_post(sample_algerian) is True


def test_format_coupon_claim_caption():
    raw_sample = """
قد تتوفر الكوبونات من جديد غدا إن شاء الله على الساعة 09h00 صباحًا
رابط الحجز : https://s.click.aliexpress.com/e/_c4Up4ucr 
رابط آخر : https://s.click.aliexpress.com/e/_c3nBNn5V
بوت تخفيض العملات: t.me/CouponsCoins_bot
#تابع قناة التليغرام👈 t.me/CouponsGlobal
"""
    link_mapping = {
        "https://s.click.aliexpress.com/e/_c4Up4ucr": "https://s.click.aliexpress.com/e/_c3OOlDBD",
        "https://s.click.aliexpress.com/e/_c3nBNn5V": "https://s.click.aliexpress.com/e/_c30KcdBp"
    }

    cap = format_coupon_claim_caption(raw_sample, link_mapping)

    # 1. Native blockquote header
    assert "<blockquote>🔥 <b>تجدد الكوبونات وتوفرها رسمياً الآن! سارعوا بالحجز ⤵️</b></blockquote>" in cap

    # 2. Both monetized affiliate links present
    assert "https://s.click.aliexpress.com/e/_c3OOlDBD" in cap
    assert "https://s.click.aliexpress.com/e/_c30KcdBp" in cap

    # 3. Competitor handles scrubbed
    assert "CouponsCoins_bot" not in cap
    assert "CouponsGlobal" not in cap

    # 4. Official bot and channel present
    assert "https://t.me/Alilo07BOT" in cap
    assert "@DzAliexpress0" in cap
    assert "ضع البلد الجزائر" in cap


def test_coupon_restock_time_window():
    dz_tz = timezone(timedelta(hours=1))

    # 09:00 AM Algerian Time -> within window
    t_9am = datetime(2026, 11, 10, 9, 5, tzinfo=dz_tz)
    assert is_coupon_restock_time_window(t_9am) is True

    # 08:57 AM Algerian Time -> within window
    t_857am = datetime(2026, 11, 10, 8, 57, tzinfo=dz_tz)
    assert is_coupon_restock_time_window(t_857am) is True

    # 02:00 PM Algerian Time -> outside window
    t_2pm = datetime(2026, 11, 10, 14, 0, tzinfo=dz_tz)
    assert is_coupon_restock_time_window(t_2pm) is False

    # 07:00 AM Algerian Time -> outside window
    t_7am = datetime(2026, 11, 10, 7, 0, tzinfo=dz_tz)
    assert is_coupon_restock_time_window(t_7am) is False
