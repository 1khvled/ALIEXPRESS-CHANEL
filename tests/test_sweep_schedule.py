import time
from datetime import datetime, timezone
import pytest
from unittest.mock import patch

from app.publisher.state_tracker import (
    is_deal_posting_due,
    get_schedule_config,
    update_schedule_config,
    record_sweep_completed,
    record_deal_posted_time
)


@pytest.fixture(autouse=True)
def clean_schedule_state():
    reset_state = {
        "day_interval_minutes": 40,
        "night_interval_minutes": 0,
        "current_interval_minutes": 40,
        "is_paused": False,
        "night_mode_enabled": True,
        "night_pause_enabled": True,
        "last_sweep_time": 0.0,
        "last_sweep_times": {},
        "night_start_hour_dz": 0,
        "night_end_hour_dz": 8
    }
    update_schedule_config(reset_state)
    yield
    update_schedule_config(reset_state)


def test_default_schedule_config():
    cfg = get_schedule_config()
    assert cfg.get("day_interval_minutes") == 40
    assert cfg.get("current_interval_minutes") == 40
    assert cfg.get("night_mode_enabled") is True
    assert cfg.get("night_start_hour_dz") == 0
    assert cfg.get("night_end_hour_dz") == 8


def test_daytime_sweep_due_when_no_previous_sweep():
    # Mock daytime (14:00 UTC = 15:00 Algiers time)
    mock_utc_now = datetime(2026, 10, 5, 14, 0, 0, tzinfo=timezone.utc)
    with patch("app.publisher.state_tracker.datetime") as mock_dt:
        mock_dt.now.return_value = mock_utc_now
        update_schedule_config({
            "is_paused": False,
            "last_sweep_time": 0.0,
            "last_sweep_times": {},
            "current_interval_minutes": 40
        })
        is_due, msg, interval = is_deal_posting_due(channel="algeria")
        assert is_due is True
        assert interval == 40
        assert "جاهز" in msg


def test_daytime_sweep_debounce_under_40_minutes():
    # Sweep happened 15 minutes ago
    mock_utc_now = datetime(2026, 10, 5, 14, 0, 0, tzinfo=timezone.utc)
    now_ts = 1791200000.0
    with patch("app.publisher.state_tracker.datetime") as mock_dt, \
         patch("app.publisher.state_tracker.time.time", return_value=now_ts):
        mock_dt.now.return_value = mock_utc_now
        update_schedule_config({
            "is_paused": False,
            "current_interval_minutes": 40,
            "last_sweep_times": {"algeria": now_ts - (15 * 60)}
        })
        is_due, msg, interval = is_deal_posting_due(channel="algeria")
        assert is_due is False
        assert interval == 40
        assert "متبقي 25.0 دقيقة" in msg or "متبقي" in msg


def test_daytime_sweep_due_after_40_minutes():
    # Sweep happened 41 minutes ago
    mock_utc_now = datetime(2026, 10, 5, 14, 0, 0, tzinfo=timezone.utc)
    now_ts = 1791200000.0
    with patch("app.publisher.state_tracker.datetime") as mock_dt, \
         patch("app.publisher.state_tracker.time.time", return_value=now_ts):
        mock_dt.now.return_value = mock_utc_now
        update_schedule_config({
            "is_paused": False,
            "current_interval_minutes": 40,
            "last_sweep_times": {"algeria": now_ts - (41 * 60)}
        })
        is_due, msg, interval = is_deal_posting_due(channel="algeria")
        assert is_due is True
        assert interval == 40


def test_night_pause_active_at_night():
    # Mock night time (02:00 UTC = 03:00 Algiers time)
    mock_utc_now = datetime(2026, 10, 5, 2, 0, 0, tzinfo=timezone.utc)
    with patch("app.publisher.state_tracker.datetime") as mock_dt:
        mock_dt.now.return_value = mock_utc_now
        update_schedule_config({
            "is_paused": False,
            "night_mode_enabled": True,
            "night_start_hour_dz": 0,
            "night_end_hour_dz": 8
        })
        is_due, msg, interval = is_deal_posting_due(channel="algeria")
        assert is_due is False
        assert interval == 0
        assert "الوضع الليلي" in msg or "متوقفة طوال الليل" in msg


def test_admin_pause():
    mock_utc_now = datetime(2026, 10, 5, 14, 0, 0, tzinfo=timezone.utc)
    with patch("app.publisher.state_tracker.datetime") as mock_dt:
        mock_dt.now.return_value = mock_utc_now
        update_schedule_config({"is_paused": True})
        is_due, msg, interval = is_deal_posting_due(channel="algeria")
        assert is_due is False
        assert "متوقف مؤقتاً" in msg


def test_independent_algeria_and_france_sweep_records():
    now_ts = 1791200000.0
    with patch("app.publisher.state_tracker.time.time", return_value=now_ts):
        record_sweep_completed(channel="algeria")
        cfg = get_schedule_config()
        assert cfg["last_sweep_times"]["algeria"] == now_ts

    with patch("app.publisher.state_tracker.time.time", return_value=now_ts + 60):
        record_sweep_completed(channel="france")
        cfg = get_schedule_config()
        assert cfg["last_sweep_times"]["algeria"] == now_ts
        assert cfg["last_sweep_times"]["france"] == now_ts + 60
