import os
import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import patch, AsyncMock, MagicMock

from app.aliexpress.promos import PromoEvent
from app.publisher.promo_notifiers import (
    build_promo_ending_alert,
    build_promo_concluded_alert,
    build_promo_launch_alert,
    get_event_ended_image_path,
    get_event_started_image_path,
    send_promo_alert_to_channel,
    check_and_auto_post_promo_notifiers
)


def test_get_event_ended_image_path():
    path = get_event_ended_image_path()
    assert path is not None
    assert os.path.exists(path)
    assert os.path.getsize(path) > 100_000  # Image is high-res (~1.7MB)


def test_get_event_started_image_path():
    path = get_event_started_image_path()
    assert path is not None
    assert os.path.exists(path)
    assert os.path.getsize(path) > 100_000  # Image is high-res (~1.7MB)


def test_build_promo_ending_alert_uses_real_end_date_and_names_event():
    promo = PromoEvent(
        name="Choice Day",
        name_ar="تخفيضات تشويس داي",
        start_date=datetime(2026, 10, 1, 7, 0, tzinfo=timezone.utc),
        end_date=datetime(2026, 10, 8, 6, 59, 59, tzinfo=timezone.utc),
        banner_tag="Choice Day",
        is_major=True,
        coupon_tiers=[]
    )
    now = datetime(2026, 10, 7, 18, 0, tzinfo=timezone.utc)
    text, reply_markup = build_promo_ending_alert(promo, now=now)

    # End is derived from promo.end_date, in Algeria time (UTC+1): 06:59:59 UTC -> 08:00.
    assert "<blockquote>⚠️ <b>تنتهي التخفيضات غدا صباحا على الساعة الثامنة (08:00 بتوقيت الجزائر)</b></blockquote>" in text
    # The event that is actually ending is named (no more ambiguous "the sale ends").
    assert "🏁 <b>الحدث:</b> تخفيضات تشويس داي" in text
    assert "❌ <b>آخر فرصة للإستفادة من الكوبونات</b>" in text
    assert "✅ <b>يمكن حجز بعض المنتجات ببطاقة مجمدة لمدة تصل الى 20 يوم بعد انتهاء التخفيضات</b>" in text
    assert "🤖 <b>البوت لتخفيض الاسعار :</b> https://t.me/Alilo07BOT" in text
    assert "📢 <b>قناة التيليغرام للمزيد من العروض :</b> https://t.me/DzAliexpress0" in text

    # Inline buttons
    buttons = reply_markup["inline_keyboard"]
    assert any("Alilo07BOT" in b["url"] for row in buttons for b in row)
    assert any("DzAliexpress0" in b["url"] for row in buttons for b in row)


def test_build_promo_ending_alert_handles_november_cutoff_hour():
    """November (PST) cutoffs are 09:00 DZ, not the old hardcoded 08:00."""
    promo = PromoEvent(
        name="11.11 Global Shopping Festival Main Sale",
        name_ar="مهرجان 11.11 الأكبر عالمياً",
        start_date=datetime(2026, 11, 1, 7, 0, tzinfo=timezone.utc),
        end_date=datetime(2026, 11, 19, 7, 59, 59, tzinfo=timezone.utc),
        banner_tag="11.11",
        is_major=True,
        coupon_tiers=[]
    )
    now = datetime(2026, 11, 18, 12, 0, tzinfo=timezone.utc)
    text, _ = build_promo_ending_alert(promo, now=now)

    assert "غدا صباحا على الساعة التاسعة (09:00 بتوقيت الجزائر)" in text


def test_build_promo_ending_alert_without_promo_keeps_legacy_default():
    text, _ = build_promo_ending_alert()
    assert "تنتهي التخفيضات غدا صباحا على الساعة الثامنة" in text


def test_build_promo_concluded_alert():
    promo = PromoEvent(
        name="Winter Offers",
        name_ar="عروض الشتاء",
        start_date=datetime(2026, 10, 14, 7, 0, tzinfo=timezone.utc),
        end_date=datetime(2026, 10, 17, 7, 0, tzinfo=timezone.utc),
        banner_tag="Winter Offers",
        is_major=True,
        coupon_tiers=[]
    )
    text, reply_markup = build_promo_concluded_alert(promo)
    assert "🛑 <b>انتهت رسمياً عروض وتخفيضات علي اكسبرس (عروض الشتاء)" in text
    assert "انتهت صلاحية جميع الكوبونات" in text
    assert "20 يوم" in text
    assert "Alilo07BOT" in text


@pytest.mark.asyncio
async def test_send_promo_alert_auto_detects_ended_image():
    text, markup = build_promo_ending_alert()

    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"ok": True, "result": {"message_id": 998877}}

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_resp
        success, err, msg_id = await send_promo_alert_to_channel(
            text=text,
            reply_markup=markup,
            bot_token="TEST_BOT_TOKEN",
            channel_id="@TestChannel"
        )
        assert success is True
        assert msg_id == 998877

        # Verify sendPhoto was called with photo file
        call_args_list = mock_post.call_args_list
        assert len(call_args_list) >= 1
        first_call = call_args_list[0]
        url = first_call[0][0]
        assert "sendPhoto" in url
        # Files dict should contain the photo
        files = first_call[1].get("files", {})
        assert "photo" in files


@pytest.mark.asyncio
async def test_send_promo_alert_auto_detects_started_image():
    promo = PromoEvent(
        name="Choice Day",
        name_ar="تشويس داي",
        start_date=datetime(2026, 10, 1, 7, 0, tzinfo=timezone.utc),
        end_date=datetime(2026, 10, 8, 7, 0, tzinfo=timezone.utc),
        banner_tag="Choice",
        is_major=True,
        coupon_tiers=[]
    )
    text, markup = build_promo_launch_alert(promo)

    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"ok": True, "result": {"message_id": 112233}}

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_resp
        success, err, msg_id = await send_promo_alert_to_channel(
            text=text,
            reply_markup=markup,
            bot_token="TEST_BOT_TOKEN",
            channel_id="@TestChannel"
        )
        assert success is True
        assert msg_id == 112233

        call_args_list = mock_post.call_args_list
        assert len(call_args_list) >= 1
        first_call = call_args_list[0]
        url = first_call[0][0]
        assert "sendPhoto" in url


@pytest.mark.asyncio
async def test_check_and_auto_post_promo_notifiers_triggers_ending():
    now = datetime(2026, 10, 7, 18, 0, tzinfo=timezone.utc)
    mock_promo = PromoEvent(
        name="Test Choice Day",
        name_ar="تشويس داي تجريبي",
        start_date=datetime(2026, 10, 1, 7, 0, tzinfo=timezone.utc),
        end_date=datetime(2026, 10, 8, 7, 0, tzinfo=timezone.utc),
        banner_tag="Choice",
        is_major=True,
        coupon_tiers=[]
    )

    from unittest.mock import PropertyMock
    from app.aliexpress.promos import PromoTracker

    with patch.object(PromoTracker, "calendar", new_callable=PropertyMock, return_value=[mock_promo]), \
         patch("app.publisher.promo_notifiers.is_promo_notifier_already_sent", return_value=False), \
         patch("app.publisher.promo_notifiers.record_promo_notifier_sent") as mock_record, \
         patch("app.publisher.promo_notifiers.send_promo_alert_to_channel", new=AsyncMock(return_value=(True, None, 12345))) as mock_send, \
         patch("app.publisher.promo_notifiers.ensure_active_promo_coupons_pinned", new=AsyncMock(return_value=None)):

        results = await check_and_auto_post_promo_notifiers(now=now, bot_token="TOKEN", channel_id="@TEST")

        assert len(results) == 1
        assert results[0]["type"] == "promo_ending_alert"
        assert results[0]["message_id"] == 12345
        mock_record.assert_called_once()
        assert mock_send.call_count == 1
        # Check that image_path was passed
        kwargs = mock_send.call_args[1]
        assert kwargs.get("image_path") is not None
        assert "dealscout_event_ended.png" in kwargs.get("image_path")


@pytest.mark.asyncio
async def test_ending_alert_suppressed_while_bigger_sale_still_running():
    """12 Nov regression: Brand Day ends 13 Nov but 11.11 runs until 18 Nov -> no 'sale ends tomorrow'."""
    now = datetime(2026, 11, 12, 12, 0, tzinfo=timezone.utc)
    brand_day = PromoEvent(
        name="Brand Day Novembre 2026",
        name_ar="مهرجان Brand Day لشهر نوفمبر 🏷️",
        start_date=datetime(2026, 11, 9, 7, 0, tzinfo=timezone.utc),
        end_date=datetime(2026, 11, 13, 6, 59, 59, tzinfo=timezone.utc),
        banner_tag="Brand Day",
        is_major=True,
        coupon_tiers=[],
        source="discovered"
    )
    main_sale = PromoEvent(
        name="11.11 Global Shopping Festival Main Sale",
        name_ar="مهرجان 11.11 الأكبر عالمياً 🛍️",
        start_date=datetime(2026, 11, 1, 7, 0, tzinfo=timezone.utc),
        end_date=datetime(2026, 11, 18, 6, 59, 59, tzinfo=timezone.utc),
        banner_tag="11.11",
        is_major=True,
        coupon_tiers=[{"tier": "3/15$", "code": "OTD1103"}],
        source="baseline"
    )

    from unittest.mock import PropertyMock
    from app.aliexpress.promos import PromoTracker

    with patch.object(PromoTracker, "calendar", new_callable=PropertyMock, return_value=[main_sale, brand_day]), \
         patch("app.publisher.promo_notifiers.is_promo_notifier_already_sent", return_value=False), \
         patch("app.publisher.promo_notifiers.record_promo_notifier_sent") as mock_record, \
         patch("app.publisher.promo_notifiers.send_promo_alert_to_channel", new=AsyncMock(return_value=(True, None, 1))) as mock_send:

        results = await check_and_auto_post_promo_notifiers(now=now, bot_token="TOKEN", channel_id="@TEST")

        assert results == []
        mock_send.assert_not_called()
        mock_record.assert_not_called()


@pytest.mark.asyncio
async def test_recurring_placeholder_shadowed_by_real_event_is_skipped():
    """The auto-generated Brand Day placeholder must not fire while baseline 11.11 covers the same dates."""
    now = datetime(2026, 11, 12, 12, 0, tzinfo=timezone.utc)
    placeholder = PromoEvent(
        name="Brand Day Novembre 2026",
        name_ar="مهرجان Brand Day لشهر نوفمبر 🏷️",
        start_date=datetime(2026, 11, 9, 7, 0, tzinfo=timezone.utc),
        end_date=datetime(2026, 11, 13, 6, 59, 59, tzinfo=timezone.utc),
        banner_tag="Brand Day",
        is_major=True,
        coupon_tiers=[],
        source="recurring"
    )
    main_sale = PromoEvent(
        name="11.11 Global Shopping Festival Main Sale",
        name_ar="مهرجان 11.11 الأكبر عالمياً 🛍️",
        start_date=datetime(2026, 11, 1, 7, 0, tzinfo=timezone.utc),
        end_date=datetime(2026, 11, 18, 6, 59, 59, tzinfo=timezone.utc),
        banner_tag="11.11",
        is_major=True,
        coupon_tiers=[{"tier": "3/15$", "code": "OTD1103"}],
        source="baseline"
    )

    from unittest.mock import PropertyMock
    from app.aliexpress.promos import PromoTracker

    with patch.object(PromoTracker, "calendar", new_callable=PropertyMock, return_value=[main_sale, placeholder]), \
         patch("app.publisher.promo_notifiers.is_promo_notifier_already_sent", return_value=False), \
         patch("app.publisher.promo_notifiers.record_promo_notifier_sent") as mock_record, \
         patch("app.publisher.promo_notifiers.send_promo_alert_to_channel", new=AsyncMock(return_value=(True, None, 1))) as mock_send:

        results = await check_and_auto_post_promo_notifiers(now=now, bot_token="TOKEN", channel_id="@TEST")

        assert results == []
        mock_send.assert_not_called()
        mock_record.assert_not_called()


@pytest.mark.asyncio
async def test_real_sale_end_still_fires_when_it_is_the_last_event():
    now = datetime(2026, 11, 17, 12, 0, tzinfo=timezone.utc)
    main_sale = PromoEvent(
        name="11.11 Global Shopping Festival Main Sale",
        name_ar="مهرجان 11.11 الأكبر عالمياً 🛍️",
        start_date=datetime(2026, 11, 1, 7, 0, tzinfo=timezone.utc),
        end_date=datetime(2026, 11, 18, 6, 59, 59, tzinfo=timezone.utc),
        banner_tag="11.11",
        is_major=True,
        coupon_tiers=[{"tier": "3/15$", "code": "OTD1103"}],
        source="baseline"
    )

    from unittest.mock import PropertyMock
    from app.aliexpress.promos import PromoTracker

    with patch.object(PromoTracker, "calendar", new_callable=PropertyMock, return_value=[main_sale]), \
         patch("app.publisher.promo_notifiers.is_promo_notifier_already_sent", return_value=False), \
         patch("app.publisher.promo_notifiers.record_promo_notifier_sent"), \
         patch("app.publisher.promo_notifiers.send_promo_alert_to_channel", new=AsyncMock(return_value=(True, None, 99))) as mock_send:

        results = await check_and_auto_post_promo_notifiers(now=now, bot_token="TOKEN", channel_id="@TEST")

        assert len(results) == 1
        assert results[0]["type"] == "promo_ending_alert"
        sent_text = mock_send.call_args[0][0]
        assert "الحدث:" in sent_text
        assert "غدا صباحا" in sent_text
