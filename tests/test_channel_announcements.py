import pytest
from app.aliexpress.parser import detect_channel_announcement
from app.publisher.state_tracker import (
    is_channel_announcement_eligible,
    record_channel_announcement_published
)

def test_detect_china_holiday_announcement():
    text = "⚠️ حاليا يوجد عطلة في الصين (بعض المتاجر ممكن تتأخر في الشحن) حتى يوم 7 أكتوبر"
    is_ann, formatted, tag = detect_channel_announcement(text)
    assert is_ann is True
    assert tag == "china_holiday_shipping_delay"
    assert "عطلة رسمية في الصين" in formatted
    assert "حتى يوم 7 أكتوبر" in formatted
    assert "@DzAliexpress0" not in text

def test_detect_announcement_skips_real_deals():
    deal_text = (
        "🔥 تخفيض قوي على ماوس Attack Shark X3\n"
        "السعر: 18.50$\n"
        "كوبون: OTPRD02\n"
        "https://s.click.aliexpress.com/e/_c2ukqBQt"
    )
    is_ann, formatted, tag = detect_channel_announcement(deal_text)
    assert is_ann is False
    assert formatted is None
    assert tag is None

def test_detect_customs_notice():
    text = "تنبيه هام بخصوص طرود الجمارك في مركز الفرز: تم تحديث إجراءات التخليص"
    is_ann, formatted, tag = detect_channel_announcement(text)
    assert is_ann is True
    assert tag == "customs_postal_notice"
    assert "إشعار هـام" in formatted

def test_channel_announcement_state_tracking():
    import uuid
    tag = f"test_tag_{uuid.uuid4().hex[:6]}"
    today = "2026-10-02"
    tomorrow = "2026-10-03"

    assert is_channel_announcement_eligible(tag, today) is True
    record_channel_announcement_published(tag, today)
    assert is_channel_announcement_eligible(tag, today) is False
    assert is_channel_announcement_eligible(tag, tomorrow) is True
