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


def test_build_promo_ending_alert_matches_user_screenshot():
    promo = PromoEvent(
        name="Choice Day",
        name_ar="تخفيضات تشويس داي",
        start_date=datetime(2026, 10, 1, 7, 0, tzinfo=timezone.utc),
        end_date=datetime(2026, 10, 8, 6, 59, 59, tzinfo=timezone.utc),
        banner_tag="Choice Day",
        is_major=True,
        coupon_tiers=[]
    )
    text, reply_markup = build_promo_ending_alert(promo)

    # User screenshot exact matches
    assert "<blockquote>⚠️ <b>تنتهي التخفيضات غدا صباحا على الساعة الثامنة</b></blockquote>" in text
    assert "❌ <b>آخر فرصة للإستفادة من الكوبونات</b>" in text
    assert "✅ <b>يمكن حجز بعض المنتجات ببطاقة مجمدة لمدة تصل الى 20 يوم بعد انتهاء التخفيضات</b>" in text
    assert "🤖 <b>البوت لتخفيض الاسعار :</b> https://t.me/Alilo07BOT" in text
    assert "📢 <b>قناة التيليغرام للمزيد من العروض :</b> https://t.me/DzAliexpress0" in text

    # Inline buttons
    buttons = reply_markup["inline_keyboard"]
    assert any("Alilo07BOT" in b["url"] for row in buttons for b in row)
    assert any("DzAliexpress0" in b["url"] for row in buttons for b in row)


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
