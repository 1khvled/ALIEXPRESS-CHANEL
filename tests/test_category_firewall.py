import pytest
from app.ai.category_firewall import (
    is_audio_product,
    is_wearable_product,
    is_tablet_product,
    is_gaming_or_pc_product,
    is_accessory_product,
    is_genuine_smartphone,
    sanitize_caption_category
)
from app.ai.generator import caption_generator
from app.ai.validator import caption_validator


AUDIO_SAMPLES = [
    "HAYLOU FlowLoop S33 Wireless Headphones 45dB ANC Hi-Res LDAC 100h Playtime",
    "Lenovo XT53 Bluetooth V5.4 Earphones LED Power Display Gaming Headphones",
    "CMF Buds 2a 42dB ANC 4HD Mics Up to 31H of playback Bluetooth 5.4 12.4mm Driver",
    "Soundcore by Anker Life Q30 Hybrid Active Noise Cancelling Headphones",
    "KZ Castor In-Ear Monitors Dual Dynamic Earphones",
    "QCY T13 ANC True Wireless Earbuds",
    "سماعات رأس لاسلكية هاي لو عازلة للضوضاء",
    "سماعة بلوتوث رياضية عازلة للضوضاء",
    "سماعات أذن لاسلكية"
]

WEARABLE_SAMPLES = [
    "HAYLOU Watch Faro Voice Calling Smart Watch",
    "Xiaomi Smart Band 8 Active 1.47 inch Display",
    "COLMI P81 Voice Calling Smart Watch Ultra 1.9 inch Screen 24H Health",
    "ساعة يد ذكية مقاومة للماء",
    "سوار ذكي لتتبع اللياقة البدنية"
]

TABLET_SAMPLES = [
    "Xiaomi Pad 7 (12/256)",
    "POCO Pad 12.1 Inch 8/256 Tablet",
    "Apple iPad Air 11-inch M2",
    "تابلت شاومي باد 6 برو شاشة 11 بوصة",
    "جهاز لوحي أندرويد شاشة 10 بوصة"
]

GAMING_PC_SAMPLES = [
    "ATTACK SHARK X3 Gaming Mouse Ultra Light",
    "AULA F75 Mechanical Keyboard Wireless 75% Layout",
    "CUSU NVMe PCIe 4.0 SSD 1TB High Speed M.2",
    "AMD Ryzen 7 5700X3D CPU Processor",
    "عتاد قيمنق لوحة مفاتيح ميكانيكية احترافية"
]

ACCESSORY_SAMPLES = [
    "Baseus 65W GaN Fast Charger Power Delivery",
    "Ugreen USB C Cable 100W PD Fast Charging",
    "Magnetic Phone Case for iPhone 16 Pro Max",
    "كفر هاتف سامسونج جالاكسي شفاف",
    "شاحن سريع 67 واط لشاومي",
    "حامي شاشة زجاجي لهاتف بوكو"
]

SMARTPHONE_SAMPLES = [
    "REALME 15 5G (12/512)",
    "OPPO A6 PRO (8/256)",
    "POCO X7 Pro 5G (12/512)",
    "Xiaomi Redmi Note 14 Pro+ 5G",
    "Infinix Note 40 Pro 4G (8/256)",
    "Samsung Galaxy A55 5G (8/256)",
    "هاتف ريلمي 12 برو بلس 5G",
    "هاتف شاومي ريدمي نوت 13 برو"
]


def test_audio_never_classified_as_phone():
    for title in AUDIO_SAMPLES:
        assert is_audio_product(title), f"Failed to identify audio: {title}"
        assert not is_genuine_smartphone(title), f"Audio misclassified as smartphone: {title}"


def test_wearable_never_classified_as_phone():
    for title in WEARABLE_SAMPLES:
        assert is_wearable_product(title), f"Failed to identify wearable: {title}"
        assert not is_genuine_smartphone(title), f"Wearable misclassified as smartphone: {title}"


def test_tablet_never_classified_as_phone():
    for title in TABLET_SAMPLES:
        assert is_tablet_product(title), f"Failed to identify tablet: {title}"
        assert not is_genuine_smartphone(title), f"Tablet misclassified as smartphone: {title}"


def test_gaming_pc_never_classified_as_phone():
    for title in GAMING_PC_SAMPLES:
        assert is_gaming_or_pc_product(title), f"Failed to identify gaming/PC: {title}"
        assert not is_genuine_smartphone(title), f"PC gear misclassified as smartphone: {title}"


def test_accessory_never_classified_as_phone():
    for title in ACCESSORY_SAMPLES:
        assert is_accessory_product(title), f"Failed to identify accessory: {title}"
        assert not is_genuine_smartphone(title), f"Accessory misclassified as smartphone: {title}"


def test_genuine_smartphones_classified_correctly():
    for title in SMARTPHONE_SAMPLES:
        assert is_genuine_smartphone(title), f"Failed to identify smartphone: {title}"


def test_sanitize_caption_category_rewrites_mismatched_phone_hook():
    bad_caption = (
        "<blockquote>🔥 <b>هاتف بمواصفات قوية وسعر لافار ممتاز متتراطاش 🔥📱</b></blockquote>\n"
        "<blockquote>📍 خلي البلـــد <b>كــــــندا 🇨🇦</b></blockquote>\n\n"
        "✅ <b>HAYLOU FlowLoop S33 Wireless Headphones 45dB ANC</b>\n\n"
        "💰 <b>السعر :</b> <b>$26.29</b> 🔥\n"
        "🛒 <b>رابط الشراء ⤵️</b>\nhttps://s.click.aliexpress.com/e/_c3DKWzSH\n\n"
        "🤖 <b>بوت تخفيض العملات:</b> @Alilo07BOT\n"
        "📢 @DzAliexpress0"
    )

    sanitized, was_sanitized = sanitize_caption_category(
        bad_caption,
        "HAYLOU FlowLoop S33 Wireless Headphones 45dB ANC"
    )
    assert was_sanitized
    assert "هاتف" not in sanitized
    assert "سماعات" in sanitized
    assert "🎧" in sanitized


def test_sanitize_caption_category_preserves_genuine_phone_hook():
    phone_caption = (
        "<blockquote>🔥 <b>هاتف بمواصفات قوية وسعر لافار ممتاز متتراطاش 🔥📱</b></blockquote>\n"
        "<blockquote>📍 خلي البلـــد <b>كــــــندا 🇨🇦</b></blockquote>\n\n"
        "✅ <b>OPPO A6 PRO (8/256)</b>\n\n"
        "💰 <b>السعر :</b> <b>$211.60</b> 🔥\n"
        "🛒 <b>رابط الشراء ⤵️</b>\nhttps://s.click.aliexpress.com/e/_c33Dm7Dx\n\n"
        "🤖 <b>بوت تخفيض العملات:</b> @Alilo07BOT\n"
        "📢 @DzAliexpress0"
    )

    sanitized, was_sanitized = sanitize_caption_category(
        phone_caption,
        "OPPO A6 PRO (8/256)"
    )
    assert not was_sanitized
    assert "هاتف" in sanitized


@pytest.mark.asyncio
async def test_end_to_end_generator_and_validator_category_firewall():
    for title in AUDIO_SAMPLES:
        caption = await caption_generator.generate(
            title=title,
            usd_price=25.00,
            affiliate_url="https://s.click.aliexpress.com/e/_test"
        )
        # 1. Generator must never include phone words in hook
        hook_line = caption.splitlines()[0]
        assert "هاتف" not in hook_line
        assert "الهواتف" not in hook_line
        assert "📱" not in hook_line

        # 2. Validator must approve the generated caption
        val = caption_validator.validate(
            caption=caption,
            expected_title=title,
            expected_usd_price=25.00,
            expected_eur_price=None,
            expected_affiliate_url="https://s.click.aliexpress.com/e/_test"
        )
        assert val.approved, f"Validator failed on {title}: {val.errors}"
