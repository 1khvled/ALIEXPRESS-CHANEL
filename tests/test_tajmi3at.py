import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import patch, MagicMock

from app.publisher.state_tracker import (
    is_tajmi3at_time_window,
    is_daily_tajmi3at_eligible,
    record_daily_tajmi3at_published,
    get_regrouped_channel_msg_ids,
    record_deals_regrouped,
    load_persistent_state,
    save_persistent_state
)
from app.publisher.regrouper import (
    classify_deal_category,
    clean_item_title,
    format_deal_line,
    build_category_bulletin_text,
    build_master_daily_roundup_text,
    check_and_publish_regrouped_bulletins
)

def test_tajmi3at_time_window():
    """Verifies that 10:00 PM Algiers time (UTC+1) is properly bounded (21:30 to 23:45)."""
    dz_tz = timezone(timedelta(hours=1))

    # Outside window
    assert is_tajmi3at_time_window(datetime(2026, 10, 2, 14, 0, tzinfo=dz_tz)) is False
    assert is_tajmi3at_time_window(datetime(2026, 10, 2, 21, 29, tzinfo=dz_tz)) is False
    assert is_tajmi3at_time_window(datetime(2026, 10, 2, 23, 46, tzinfo=dz_tz)) is False
    assert is_tajmi3at_time_window(datetime(2026, 10, 2, 0, 0, tzinfo=dz_tz)) is False
    assert is_tajmi3at_time_window(datetime(2026, 10, 2, 10, 0, tzinfo=dz_tz)) is False

    # Inside window (around 10:00 PM and accommodating delays)
    assert is_tajmi3at_time_window(datetime(2026, 10, 2, 21, 30, tzinfo=dz_tz)) is True
    assert is_tajmi3at_time_window(datetime(2026, 10, 2, 21, 45, tzinfo=dz_tz)) is True
    assert is_tajmi3at_time_window(datetime(2026, 10, 2, 22, 0, tzinfo=dz_tz)) is True  # 10:00 PM
    assert is_tajmi3at_time_window(datetime(2026, 10, 2, 22, 15, tzinfo=dz_tz)) is True
    assert is_tajmi3at_time_window(datetime(2026, 10, 2, 22, 45, tzinfo=dz_tz)) is True
    assert is_tajmi3at_time_window(datetime(2026, 10, 2, 23, 0, tzinfo=dz_tz)) is True
    assert is_tajmi3at_time_window(datetime(2026, 10, 2, 23, 45, tzinfo=dz_tz)) is True

def test_daily_tajmi3at_idempotency(tmp_path):
    """Verifies that daily tajmi3at can only be published once per calendar day."""
    test_state_file = str(tmp_path / "published_state.json")
    with patch("app.publisher.state_tracker.STATE_FILE_PATH", test_state_file):
        # 1. Initially eligible
        eligible, _ = is_daily_tajmi3at_eligible("2026-10-02")
        assert eligible is True

        # 2. Record publication
        record_daily_tajmi3at_published(bulletins_count=2, date_str="2026-10-02")

        # 3. Same day now ineligible
        eligible, reason = is_daily_tajmi3at_eligible("2026-10-02")
        assert eligible is False
        assert "already published" in reason

        # 4. Next day eligible
        eligible_next, _ = is_daily_tajmi3at_eligible("2026-10-03")
        assert eligible_next is True

def test_regrouped_msg_ids_persistence(tmp_path):
    """Verifies that regrouped message IDs are persisted and retrieved correctly."""
    test_state_file = str(tmp_path / "published_state.json")
    with patch("app.publisher.state_tracker.STATE_FILE_PATH", test_state_file):
        assert len(get_regrouped_channel_msg_ids()) == 0

        record_deals_regrouped([301, 302, 303])
        ids = get_regrouped_channel_msg_ids()
        assert 301 in ids
        assert 302 in ids
        assert 303 in ids

        # Append more
        record_deals_regrouped([304])
        ids2 = get_regrouped_channel_msg_ids()
        assert len(ids2) == 4
        assert 304 in ids2

def test_category_classification_accuracy():
    """Verifies that deals are strictly classified into homogeneous categories without cross-contamination."""
    # Phones
    assert classify_deal_category("Xiaomi Redmi Note 17 5G Global Version") == "phones"
    assert classify_deal_category("Realme 14 Pro Plus Global (8/256)") == "phones"
    assert classify_deal_category("POCO C71 3/64GB") == "phones"
    assert classify_deal_category("OPPO A6 Pro 8/256GB") == "phones"

    # Smartwatches (must NOT match phones despite brand name like Honor or Xiaomi)
    assert classify_deal_category("Honor Choice Watch 2i") == "smartwatches"
    assert classify_deal_category("Honor Watch X5i") == "smartwatches"
    assert classify_deal_category("CMF Watch 3 Pro AMOLED") == "smartwatches"
    assert classify_deal_category("Zeblaze Btalk PRO Multiple") == "smartwatches"

    # Tablets (must NOT match phones)
    assert classify_deal_category("realme Pad 3 5G Global Version 8/256GB") == "tablets"
    assert classify_deal_category("Xiaomi Pad 7 (12/256)") == "tablets"
    assert classify_deal_category("Blackview LINK 1 Kids Tablets") == "tablets"

    # Gaming Mice
    assert classify_deal_category("ATTACK SHARK X11 Tri-Mode Wireless Gaming Mouse") == "mice"
    assert classify_deal_category("Attack Shark R1 Wireless Mouse") == "mice"

    # Audio / Headsets
    assert classify_deal_category("ATTACK SHARK L90 Gaming Headset") == "headsets"
    assert classify_deal_category("Lenovo XT53 Bluetooth V5.4 Earphones") == "headsets"
    assert classify_deal_category("Moondrop Chu 3 IEM") == "headsets"

    # PC Hardware
    assert classify_deal_category("SomnAmbulist SSD 2.5 128GB") == "pc_parts"
    assert classify_deal_category("AMD Ryzen 5 7600X CPU") == "pc_parts"

    # Accessories / multi-packs excluded
    assert classify_deal_category("Case for POCO C71") is None
    assert classify_deal_category("Tempered glass for Realme 14 Pro") is None
    assert classify_deal_category("Mousepad gaming large") is None

def test_bulletin_caption_length_and_format():
    """Verifies that bulletin caption fits within Telegram photo caption limit (1024 chars) and contains links and prices."""
    sample_items = [
        {"channel_msg_id": 201, "title": "Realme 14 Pro Plus 5G (8/256)", "price": 294.9, "channel_url": "https://t.me/DzAliexpress0/201"},
        {"channel_msg_id": 202, "title": "Realme 15 Pro Global (8/256)", "price": 314.9, "channel_url": "https://t.me/DzAliexpress0/202"},
        {"channel_msg_id": 203, "title": "Poco C71 3/64GB", "price": 57.2, "channel_url": "https://t.me/DzAliexpress0/203"},
        {"channel_msg_id": 204, "title": "OPPO A6 Pro 8/256", "price": 204.7, "channel_url": "https://t.me/DzAliexpress0/204"},
        {"channel_msg_id": 205, "title": "Honor X70 5G 8/128", "price": 185.0, "channel_url": "https://t.me/DzAliexpress0/205"},
        {"channel_msg_id": 206, "title": "POCO X6 Pro 5G 12/512GB", "price": 240.0, "channel_url": "https://t.me/DzAliexpress0/206"},
    ]

    caption, used = build_category_bulletin_text("phones", sample_items, "DzAliexpress0")
    assert len(used) >= 4
    assert len(caption) <= 1024, f"Caption exceeded 1024 chars! Got {len(caption)}"

    # Check key components
    assert "📱" in caption
    assert "تجميعة أقوى عروض الهواتف" in caption
    assert "@Alilo07BOT" in caption
    assert "https://t.me/DzAliexpress0/" in caption
    assert "$" in caption
    assert "€" in caption

def test_master_roundup_caption_and_format():
    """Verifies that the Master Daily Roundup caption is clean, <= 1024 chars, and contains valid links."""
    sample_deals = [
        {"channel_msg_id": 210, "title": "POCO C71 3/64GB", "price": 57.2, "channel_url": "https://t.me/DzAliexpress0/210"},
        {"channel_msg_id": 211, "title": "Attack Shark X11 Mouse", "price": 22.64, "channel_url": "https://t.me/DzAliexpress0/211"},
        {"channel_msg_id": 212, "title": "Attack Shark L90 Headset", "price": 18.7, "channel_url": "https://t.me/DzAliexpress0/212"},
        {"channel_msg_id": 213, "title": "SomnAmbulist SSD 128GB", "price": 31.0, "channel_url": "https://t.me/DzAliexpress0/213"},
    ]

    caption, used = build_master_daily_roundup_text(sample_deals, "DzAliexpress0")
    assert len(used) == 4
    assert len(caption) <= 1024
    assert "🌙" in caption
    assert "تجميعة أفضل صفقات وعروض اليوم" in caption
    assert "@Alilo07BOT" in caption
    assert "https://t.me/DzAliexpress0/210" in caption

@pytest.mark.asyncio
async def test_check_and_publish_skips_outside_window():
    """Verifies that automatic execution skips when not in the 10 PM window."""
    with patch("app.publisher.regrouper.is_tajmi3at_time_window", return_value=False):
        res = await check_and_publish_regrouped_bulletins(force=False)
        assert res == []

@pytest.mark.asyncio
async def test_ensure_active_promo_coupons_pinned_dz(tmp_path):
    """Verifies that during an active promo, the official coupon post is published and pinned for Algeria."""
    from app.publisher.promo_notifiers import ensure_active_promo_coupons_pinned
    test_state = str(tmp_path / "published_state.json")
    with patch("app.publisher.state_tracker.STATE_FILE_PATH", test_state), \
         patch("app.publisher.promo_notifiers.send_promo_alert_to_channel", return_value=(True, None, 888)), \
         patch("httpx.AsyncClient.post") as mock_post:
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = {"ok": True}
        mock_post.return_value = resp

        # 1. First call: publishes and pins
        msg_id = await ensure_active_promo_coupons_pinned()
        assert msg_id == 888

        # 2. Second call during same event: re-verifies pin without re-publishing
        msg_id_2 = await ensure_active_promo_coupons_pinned()
        assert msg_id_2 == 888

@pytest.mark.asyncio
async def test_ensure_active_promo_coupons_pinned_france(tmp_path):
    """Verifies that during an active promo, the official French coupon post is published and pinned for France."""
    from app.publisher.promo_notifiers_fr import ensure_france_active_promo_coupons_pinned
    test_state = tmp_path / "france_published_state.json"
    with patch("app.publisher.promo_notifiers_fr.FRANCE_STATE_FILE_PATH", str(test_state)), \
         patch("app.publisher.promo_notifiers_fr.send_france_promo_alert", return_value=(True, None, 777)), \
         patch("httpx.AsyncClient.post") as mock_post:
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = {"ok": True}
        mock_post.return_value = resp

        # 1. First call: publishes and pins
        msg_id = await ensure_france_active_promo_coupons_pinned()
        assert msg_id == 777

        # 2. Second call during same event: re-verifies pin without re-publishing
        msg_id_2 = await ensure_france_active_promo_coupons_pinned()
        assert msg_id_2 == 777
