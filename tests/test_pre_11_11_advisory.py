import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import patch, AsyncMock

from app.publisher.state_tracker import (
    is_pre_11_11_season,
    is_pre_11_11_advisory_eligible,
    record_pre_11_11_advisory_published,
    load_persistent_state,
    save_persistent_state
)
from app.publisher.pre_11_11_advisory import (
    PRE_11_11_VARIANTS,
    VARIANT_0_EXACT,
    VARIANT_1_CURRENCY_STRATEGY,
    VARIANT_2_COINS_COUNTDOWN,
    check_and_auto_post_pre_11_11_advisory
)

def test_is_pre_11_11_season_boundaries():
    dz_tz = timezone(timedelta(hours=1))
    
    # Inside season: Oct 10 to Nov 10
    assert is_pre_11_11_season(datetime(2026, 10, 10, 0, 0, tzinfo=dz_tz)) is True
    assert is_pre_11_11_season(datetime(2026, 10, 18, 12, 0, tzinfo=dz_tz)) is True
    assert is_pre_11_11_season(datetime(2026, 10, 31, 23, 59, tzinfo=dz_tz)) is True
    assert is_pre_11_11_season(datetime(2026, 11, 1, 0, 0, tzinfo=dz_tz)) is True
    assert is_pre_11_11_season(datetime(2026, 11, 10, 23, 59, tzinfo=dz_tz)) is True

    # Outside season: strictly NEVER active for any other time
    assert is_pre_11_11_season(datetime(2026, 10, 9, 23, 59, tzinfo=dz_tz)) is False
    assert is_pre_11_11_season(datetime(2026, 11, 11, 0, 0, tzinfo=dz_tz)) is False
    assert is_pre_11_11_season(datetime(2026, 1, 1, 12, 0, tzinfo=dz_tz)) is False
    assert is_pre_11_11_season(datetime(2026, 6, 15, 12, 0, tzinfo=dz_tz)) is False
    assert is_pre_11_11_season(datetime(2026, 12, 1, 12, 0, tzinfo=dz_tz)) is False


def test_pre_11_11_variants_content():
    assert len(PRE_11_11_VARIANTS) == 3

    # Exact variant matches user request screenshot
    assert "باقي أقل من شهر على التخفيضات الكبرى" in VARIANT_0_EXACT or "باقي اقل من شهر" in VARIANT_0_EXACT
    assert "11/11" in VARIANT_0_EXACT
    assert "Black Friday" in VARIANT_0_EXACT
    assert "بشراء الدولار والأورو من الآن" in VARIANT_0_EXACT
    assert "Alilo07BOT" in VARIANT_0_EXACT
    assert "DzAliexpress0" in VARIANT_0_EXACT

    for var in PRE_11_11_VARIANTS:
        text = var["text"]
        buttons = var["buttons"]
        # Must mention 11/11 and Black Friday
        assert "11/11" in text
        assert "Black Friday" in text
        # Must mention currencies
        assert "الدولار" in text
        assert "الأورو" in text
        # Must include channel & bot links in buttons
        assert any("Alilo07BOT" in b["url"] for row in buttons for b in row)
        assert any("DzAliexpress0" in b["url"] for row in buttons for b in row)


@pytest.mark.asyncio
async def test_pre_11_11_eligibility_cooldown_and_season():
    # Outside season
    with patch("app.publisher.state_tracker.is_pre_11_11_season", return_value=False):
        eligible, reason = await is_pre_11_11_advisory_eligible(force=False)
        assert eligible is False
        assert "Outside Pre-11.11 season" in reason

        # Forced bypasses season
        eligible_f, _ = await is_pre_11_11_advisory_eligible(force=True)
        assert eligible_f is True

    # Inside season
    with patch("app.publisher.state_tracker.is_pre_11_11_season", return_value=True), \
         patch("app.publisher.state_tracker.refresh_channel_cache", new=AsyncMock()):
        
        state = load_persistent_state()
        now = 1760000000.0

        # Cooldown active (e.g. published 10 hours ago with 72h interval)
        state["last_pre_11_11_advisory_time"] = now - (10 * 3600)
        state["next_pre_11_11_interval_seconds"] = 72 * 3600
        save_persistent_state(state)

        with patch("time.time", return_value=now):
            eligible, reason = await is_pre_11_11_advisory_eligible(force=False)
            assert eligible is False
            assert "cooldown active" in reason

            # Cooldown passed (e.g. published 80 hours ago with 72h interval)
            state["last_pre_11_11_advisory_time"] = now - (80 * 3600)
            save_persistent_state(state)
            with patch("app.publisher.state_tracker._CACHED_CHANNEL_TEXTS", []):
                eligible, reason = await is_pre_11_11_advisory_eligible(force=False)
                assert eligible is True
                assert "eligible for publication" in reason


def test_record_pre_11_11_advisory_published():
    record_pre_11_11_advisory_published(variant_idx=1)
    state = load_persistent_state()
    assert state.get("pre_11_11_variant_idx") == 1
    interval = state.get("next_pre_11_11_interval_seconds", 0)
    # Check that randomized interval is strictly between 72h and 96h
    assert 72 * 3600 <= interval <= 96 * 3600
