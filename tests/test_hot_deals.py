"""Hot-deal repost rule: copy competitors when they keep hammering the same product."""
import time

import pytest


@pytest.fixture
def tracker(tmp_path, monkeypatch):
    import app.publisher.state_tracker as st

    monkeypatch.setattr(st, "STATE_FILE_PATH", str(tmp_path / "published_state.json"))
    return st


PID = "1005012726037568"


def _seed_published(tracker, pid=PID, age_hours=3.0, price=7.47):
    state = tracker.load_persistent_state()
    state.setdefault("published_product_timestamps", {})[pid] = time.time() - age_hours * 3600
    state.setdefault("published_product_channels", {})[pid] = "aniscoupons"
    state.setdefault("published_product_prices", {})[pid] = price
    tracker.save_persistent_state(state)


def test_hot_deal_eligible_after_repeated_pushes_from_several_channels(tracker):
    _seed_published(tracker)
    for channel in ("zedstoreonline", "lodydeals", "zedstoreonline", "BNDDEALS"):
        tracker.record_competitor_sighting(PID, channel, 7.40)

    eligible, reason = tracker.is_hot_deal_repost_eligible(PID, current_price=7.40)

    assert eligible is True
    assert "competitor channels" in reason


def test_hot_deal_not_eligible_from_a_single_channel(tracker):
    _seed_published(tracker)
    for _ in range(6):
        tracker.record_competitor_sighting(PID, "zedstoreonline", 7.40)

    eligible, reason = tracker.is_hot_deal_repost_eligible(PID, current_price=7.40)

    assert eligible is False
    assert "1 channel" in reason


def test_hot_deal_not_eligible_without_enough_pushes(tracker):
    _seed_published(tracker)
    tracker.record_competitor_sighting(PID, "zedstoreonline", 7.40)
    tracker.record_competitor_sighting(PID, "lodydeals", 7.40)

    eligible, _ = tracker.is_hot_deal_repost_eligible(PID, current_price=7.40)

    assert eligible is False


def test_hot_deal_not_eligible_when_price_went_up(tracker):
    _seed_published(tracker, price=7.40)
    for channel in ("zedstoreonline", "lodydeals", "BNDDEALS"):
        tracker.record_competitor_sighting(PID, channel, 8.10)

    eligible, reason = tracker.is_hot_deal_repost_eligible(PID, current_price=8.10)

    assert eligible is False
    assert "price went up" in reason


def test_hot_deal_not_eligible_too_soon_after_our_post(tracker):
    _seed_published(tracker, age_hours=0.25)
    for channel in ("zedstoreonline", "lodydeals", "BNDDEALS"):
        tracker.record_competitor_sighting(PID, channel, 7.40)

    eligible, reason = tracker.is_hot_deal_repost_eligible(PID, current_price=7.40)

    assert eligible is False
    assert "too soon" in reason


def test_hot_deal_repost_is_capped_per_cooldown(tracker):
    _seed_published(tracker)
    for channel in ("zedstoreonline", "lodydeals", "BNDDEALS"):
        tracker.record_competitor_sighting(PID, channel, 7.40)
    assert tracker.is_hot_deal_repost_eligible(PID, current_price=7.40)[0] is True

    tracker.record_hot_deal_repost(PID)

    eligible, reason = tracker.is_hot_deal_repost_eligible(PID, current_price=7.40)
    assert eligible is False
    assert "already done" in reason


def test_sighting_is_ignored_for_unpublished_product(tracker):
    tracker.record_competitor_sighting("999000111222", "zedstoreonline", 5.0)

    state = tracker.load_persistent_state()
    assert "999000111222" not in state.get("competitor_product_sightings", {})

    eligible, _ = tracker.is_hot_deal_repost_eligible("999000111222", current_price=5.0)
    assert eligible is False
