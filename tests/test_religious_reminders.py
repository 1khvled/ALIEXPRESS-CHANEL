import pytest
from datetime import datetime, timezone, timedelta
from app.publisher.state_tracker import (
    is_religious_reminder_eligible,
    record_religious_reminder_published
)
from app.publisher.religious_reminders import (
    JUMUAH_MORNING_TEXT,
    JUMUAH_ASR_TEXT,
    FAJR_VARIANTS,
    JUMUAH_MORNING_KEYBOARD,
    JUMUAH_ASR_KEYBOARD
)

def test_religious_reminder_state_tracking():
    import uuid
    rem_id = f"test_rem_{uuid.uuid4().hex[:8]}"
    today = "2026-10-02"
    tomorrow = "2026-10-03"

    # Initially eligible for unique mock reminder
    assert is_religious_reminder_eligible(rem_id, today) is True

    # Record as published today
    record_religious_reminder_published(rem_id, today)

    # Should no longer be eligible today
    assert is_religious_reminder_eligible(rem_id, today) is False

    # Should be eligible tomorrow
    assert is_religious_reminder_eligible(rem_id, tomorrow) is True

def test_jumuah_reminder_content():
    # User's exact requested verse must be present
    assert "إِنَّ اللَّهَ وَمَلَائِكَتَهُ يُصَلُّونَ عَلَى النَّبِيِّ" in JUMUAH_MORNING_TEXT
    assert "صلوا عليه وسلموا تسليما" in JUMUAH_MORNING_TEXT or "صَلُّوا عَلَيْهِ وَسَلِّمُوا تَسْلِيمًا" in JUMUAH_MORNING_TEXT
    assert "سورة الكهف" in JUMUAH_MORNING_TEXT
    assert len(JUMUAH_MORNING_KEYBOARD["inline_keyboard"]) >= 1

def test_jumuah_asr_content():
    assert "ساعة الاستجابة" in JUMUAH_ASR_TEXT
    assert "فلسطين" in JUMUAH_ASR_TEXT
    assert len(JUMUAH_ASR_KEYBOARD["inline_keyboard"]) >= 1

def test_fajr_variants():
    assert len(FAJR_VARIANTS) >= 3
    for v in FAJR_VARIANTS:
        text = v["text"]
        assert "الصلاة خيرٌ من النوم" in text or "الصلاة خير من النوم" in text
        assert "الفجر" in text
        assert "inline_keyboard" in v["keyboard"]
