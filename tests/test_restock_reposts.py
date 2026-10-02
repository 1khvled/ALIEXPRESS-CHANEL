import pytest
import time
from app.aliexpress.parser import detect_restock_deal
from app.publisher.state_tracker import (
    load_persistent_state,
    save_persistent_state,
    is_recent_cross_channel_duplicate
)
from app.ai.generator import caption_generator

def test_detect_restock_phrases():
    # User's exact query phrases and real Algerian competitor formats
    restock_samples = [
        "الحقق عودة العرض حبات قلا ل",
        "الححححق عودة العرض حبات قلال فقط! 🔥",
        "رجع توفر من جديد بسعر باطل ناااار",
        "صيدة رجعت توفرت.. كمية محدودة جداً سارعوا!",
        "عاود توفر بقاو حبات قلال متتراطاش",
        "سارعوا قبل نفاذ الكمية حبات قليلة",
        "الحق عودة توفر العرض لافااار 🔥"
    ]
    for sample in restock_samples:
        assert detect_restock_deal(sample) is True, f"Failed to detect restock for: {sample}"

    non_restock_samples = [
        "عرض جديد لافار هبال على ماوس قيمنق",
        "POCO C71 3/64 بسعر 57$ 🔥",
        "سماعات بلوتوث ممتازة جودة عالية",
        "كوبونات تخفيض كودات حصرية"
    ]
    for sample in non_restock_samples:
        assert detect_restock_deal(sample) is False, f"False positive restock for: {sample}"

def test_restock_exception_in_dedup():
    pid = "999888777111"
    now = time.time()
    state = load_persistent_state()
    state["published_product_timestamps"][pid] = now - 1800.0  # Posted 30 mins ago
    state["published_product_channels"][pid] = "lodydeals"
    state["published_product_prices"][pid] = 20.0
    save_persistent_state(state)

    # 1. Normal identical post from another channel within 3h is blocked
    normal_post = "عرض لافار على نفس المنتج بسعر 20$"
    is_dup, reason, _ = is_recent_cross_channel_duplicate(
        pid, "zedstoreonline", current_price=20.0, raw_text=normal_post, cooldown_hours=3.0
    )
    assert is_dup is True, "Normal duplicate should be blocked"

    # 2. Restock post from another channel within 3h is ALLOWED via Restock Exception!
    restock_post = "الححححق عودة العرض حبات قلال فقط سارعوا! 🔥"
    is_dup_restock, reason_restock, _ = is_recent_cross_channel_duplicate(
        pid, "zedstoreonline", current_price=20.0, raw_text=restock_post, cooldown_hours=3.0
    )
    assert is_dup_restock is False, "Restock post must be allowed via Restock Exception"
    assert "Restock exception" in reason_restock

@pytest.mark.asyncio
async def test_restock_caption_generation():
    caption = await caption_generator.generate(
        title="Attack Shark X11 Gaming Mouse",
        usd_price=19.99,
        eur_price=18.50,
        affiliate_url="https://s.click.aliexpress.com/e/_c3example",
        is_restock=True
    )
    # Must include authentic restock urgency hook and limited quantity badge
    assert any(k in caption for k in ["عودة العرض", "رجع توفر", "توفر من جديد"])
    assert any(k in caption for k in ["حبات قلال", "كمية محدودة"])
    assert "Attack Shark X11 Gaming Mouse" in caption
