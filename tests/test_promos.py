"""
Tests for Autonomous Event Knower (app/aliexpress/promos.py)
Verifies multilingual date parsing, coupon extraction, recurring calendar generation,
dynamic event sniffing, persistence, and unified promo tracking.
"""
import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import patch

from app.aliexpress.promos import (
    PromoEvent,
    parse_promo_dates,
    extract_coupon_tiers_from_text,
    sniff_event_from_text,
    generate_recurring_promos,
    load_dynamic_events,
    save_dynamic_events,
    PromoTracker,
    promo_tracker
)


def test_parse_promo_dates_arabic():
    # 1. Standard Arabic same month
    res = parse_promo_dates("تخفيضات Choice Day تنطلق من 1 إلى 7 أكتوبر 2026", default_year=2026)
    assert res is not None
    start, end = res
    assert start == datetime(2026, 10, 1, 7, 0, 0, tzinfo=timezone.utc)
    assert end == datetime(2026, 10, 8, 6, 59, 59, tzinfo=timezone.utc)

    # 2. Algerian dialect month (جانفي / فيفري)
    res_dz = parse_promo_dates("مهرجان التسوق من 01 الى 07 جانفي 2027", default_year=2027)
    assert res_dz is not None
    start_dz, end_dz = res_dz
    assert start_dz.month == 1
    assert start_dz.day == 1

    # 3. Arabic across two months
    res_cross = parse_promo_dates("تخفيضات الجمعة السوداء من 24 نوفمبر إلى 1 ديسمبر 2026", default_year=2026)
    assert res_cross is not None
    start_c, end_c = res_cross
    assert start_c.month == 11 and start_c.day == 24
    assert end_c.month == 12 and end_c.day == 2


def test_parse_promo_dates_french():
    # 1. French format: du 1er au 7 octobre
    res = parse_promo_dates("Codes promo AliExpress Choice Day du 1er au 7 octobre 2026", default_year=2026)
    assert res is not None
    start, end = res
    assert start == datetime(2026, 10, 1, 7, 0, 0, tzinfo=timezone.utc)
    assert end == datetime(2026, 10, 8, 6, 59, 59, tzinfo=timezone.utc)

    # 2. French across months: du 24 nov au 1er dec
    res_cross = parse_promo_dates("Soldes Black Friday du 24 novembre au 1er décembre 2026", default_year=2026)
    assert res_cross is not None
    start_c, end_c = res_cross
    assert start_c.month == 11 and start_c.day == 24
    assert end_c.month == 12 and end_c.day == 2


def test_parse_promo_dates_english_and_numeric():
    # English
    res_en = parse_promo_dates("Choice Day sale from Oct 1 to Oct 7 2026", default_year=2026)
    assert res_en is not None
    assert res_en[0].month == 10 and res_en[0].day == 1

    # Numerical
    res_num = parse_promo_dates("Offres spéciales du 01/10 au 07/10/2026", default_year=2026)
    assert res_num is not None
    assert res_num[0].day == 1 and res_num[0].month == 10


def test_extract_coupon_tiers_multilingual():
    text = """
    🚨 أحدث كوبونات تخفيضات Choice Day الرسمية:
    🎟️ كوبون 2/15$ : OTPRD02
    🎟️ كوبون 4/30$ : OTPRD04
    🎟️ كوبون 55/449$ : OTPRD55
    
    Pour la France :
    🎟️ Code -2€ dès 18€ : FRPRD02
    🎟️ Code -6€ dès 45€ : FRPRD06
    🎟️ Code -60€ dès 475€ : FRPRD60
    """
    dz_tiers, fr_tiers = extract_coupon_tiers_from_text(text)

    # Algeria / Global coupons
    assert len(dz_tiers) >= 3
    dz_codes = [c["code"] for c in dz_tiers]
    assert "OTPRD02" in dz_codes
    assert "OTPRD04" in dz_codes
    assert "OTPRD55" in dz_codes

    # France coupons
    assert len(fr_tiers) >= 3
    fr_codes = [c["code"] for c in fr_tiers]
    assert "FRPRD02" in fr_codes
    assert "FRPRD06" in fr_codes
    assert "FRPRD60" in fr_codes


def test_sniff_event_from_text():
    # 1. Arabic Choice Day Announcement
    ar_announcement = """
    🚨 كوبونات حدث Party Ready Sale لشهر أكتوبر! 🛍️
    تنطلق غداً 01 أكتوبر وتستمر إلى غاية 07 أكتوبر 🗓️
    🎟️ كوبون 2/15$ : OTPRD02
    🎟️ كوبون 4/30$ : OTPRD04
    🎟️ كوبون 55/449$ : OTPRD55
    حجز الكوبونات يبدأ على 08:00 صباحاً!
    """
    ev_ar = sniff_event_from_text(ar_announcement)
    assert ev_ar is not None
    assert "Choice Day" in ev_ar.name or "Party Ready" in ev_ar.name
    assert ev_ar.start_date.month == 10
    assert len(ev_ar.coupon_tiers) >= 2
    assert ev_ar.source == "discovered"

    # 2. French Choice Day Announcement
    fr_announcement = """
    🚨 CODES PROMO | Choice Day Octobre ! 🇫🇷
    Du 1er au 7 octobre 2026 🛍️
    🎟️ Code -2€ dès 18€ : FRPRD02
    🎟️ Code -6€ dès 45€ : FRPRD06
    🎟️ Code -60€ dès 475€ : FRPRD60
    Actifs dès 09h00 (Paris) !
    """
    ev_fr = sniff_event_from_text(fr_announcement)
    assert ev_fr is not None
    assert "Choice Day" in ev_fr.name
    assert len(ev_fr.coupon_tiers_fr) >= 2

    # 3. Normal product deal should NOT trigger event discovery (no false positives)
    deal_text = "🔥 سماعة رأس لاسلكية Lenovo LP40 Pro بسعر $9.99 فقط مع شحن مجاني للجزائر! رابط الشراء: https://s.click.aliexpress.com/e/_test"
    ev_deal = sniff_event_from_text(deal_text)
    assert ev_deal is None


def test_generate_recurring_promos():
    ref = datetime(2026, 10, 1, 12, 0, 0, tzinfo=timezone.utc)
    recurring = generate_recurring_promos(ref, months_ahead=3)

    # Must contain Choice Day and Brand Day for Oct, Nov, Dec, Jan
    event_names = [e.name for e in recurring]
    assert any("Choice Day Octobre 2026" in name for name in event_names)
    assert any("Brand Day Octobre 2026" in name for name in event_names)
    assert any("Choice Day Novembre 2026" in name for name in event_names)
    assert any("11.11 Global Shopping Festival Main Sale 2026" in name for name in event_names)
    assert any("Black Friday & Cyber Monday 2026" in name for name in event_names)

    # Choice Day is 7 full days (1st 07:00 to 8th 06:59:59)
    oct_choice = next(e for e in recurring if "Choice Day Octobre" in e.name)
    assert oct_choice.start_date == datetime(2026, 10, 1, 7, 0, 0, tzinfo=timezone.utc)
    assert oct_choice.end_date == datetime(2026, 10, 8, 6, 59, 59, tzinfo=timezone.utc)


def test_dynamic_persistence(tmp_path):
    test_file = tmp_path / "dynamic_events.json"
    ev = PromoEvent(
        name="Mega Flash Sale",
        name_ar="تخفيضات فلاش كبرى 🔥",
        name_fr="Méga Vente Flash 🇫🇷",
        start_date=datetime(2026, 10, 5, 7, 0, 0, tzinfo=timezone.utc),
        end_date=datetime(2026, 10, 7, 6, 59, 59, tzinfo=timezone.utc),
        banner_tag="⚡ Flash Sale",
        is_major=True,
        coupon_tiers=[{"tier": "5/40$", "code": "FLASH05"}],
        coupon_tiers_fr=[{"tier": "-5€ dès 40€", "code": "FRFLASH05"}],
        source="discovered"
    )

    with patch("app.aliexpress.promos.DYNAMIC_EVENTS_FILE", test_file):
        save_dynamic_events([ev])
        loaded = load_dynamic_events()
        assert len(loaded) == 1
        assert loaded[0].name == "Mega Flash Sale"
        assert loaded[0].coupon_tiers[0]["code"] == "FLASH05"
        assert loaded[0].coupon_tiers_fr[0]["code"] == "FRFLASH05"
        assert loaded[0].source == "discovered"


def test_promo_tracker_integration(tmp_path):
    test_file = tmp_path / "dynamic_events.json"
    with patch("app.aliexpress.promos.DYNAMIC_EVENTS_FILE", test_file):
        tracker = PromoTracker()

        # 1. Current active Choice Day in October 2026
        now_oct = datetime(2026, 10, 3, 12, 0, 0, tzinfo=timezone.utc)
        active = tracker.get_active_promo(now_oct)
        assert active is not None
        assert "Choice Day" in active.name or "Party Ready" in active.name

        # 2. Upcoming promo in mid-October
        next_ev = tracker.get_next_promo(now_oct)
        assert next_ev is not None
        ev, days_left = next_ev
        assert days_left > 0
        assert "Brand Day" in ev.name

        # 3. Sniff and register live event
        announcement = """
        🚀 تخفيضات خاصة جديدة من 15 إلى 18 أكتوبر 2026
        🎟️ كوبون 10/80$ : SPECIAL10
        🎟️ كوبون 20/160$ : SPECIAL20
        """
        registered = tracker.sniff_and_register_event(announcement)
        assert registered is not None
        assert len(registered.coupon_tiers) == 2
        assert registered.coupon_tiers[0]["code"] == "SPECIAL10"

        # Verify it now appears in unified promos
        all_promos = tracker.get_all_promos(now_oct)
        assert any(p.coupon_tiers and p.coupon_tiers[0].get("code") == "SPECIAL10" for p in all_promos)
