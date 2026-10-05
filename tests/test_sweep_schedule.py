from unittest.mock import patch
import pytest

from app.publisher.state_tracker import (
    is_deal_posting_due,
    get_schedule_config,
    update_schedule_config
)


@pytest.fixture(autouse=True)
def clean_schedule_state():
    reset_state = {
        "day_interval_minutes": 5,
        "night_interval_minutes": 60,
        "current_interval_minutes": 5,
        "is_paused": False,
        "night_mode_enabled": True,
        "night_start_hour_dz": 0,
        "night_end_hour_dz": 8
    }
    update_schedule_config(reset_state)
    yield
    update_schedule_config(reset_state)


def test_default_schedule_config():
    cfg = get_schedule_config()
    assert cfg.get("day_interval_minutes") == 5
    assert cfg.get("current_interval_minutes") == 5
    assert cfg.get("night_mode_enabled") is True


def test_deal_posting_due_when_active():
    update_schedule_config({"is_paused": False})
    is_due, msg, _ = is_deal_posting_due(channel="algeria")
    assert is_due is True
    assert "نشطة" in msg


def test_admin_pause():
    update_schedule_config({"is_paused": True})
    is_due, msg, _ = is_deal_posting_due(channel="algeria")
    assert is_due is False
    assert "متوقف مؤقتاً" in msg
