import pytest
from unittest.mock import AsyncMock, patch
from app.aliexpress.urls import check_competitor_contamination, strip_competitor_elements
from app.ai.validator import caption_validator
from app.publisher.publisher import telegram_publisher
from app.db.models import Deal

def test_check_competitor_contamination():
    # 1. Competitor shortcode
    is_contam, reason = check_competitor_contamination(url="https://s.click.aliexpress.com/e/_c38iyTZR")
    assert is_contam is True
    assert "_c38iyTZR" in reason

    # 2. Competitor channel handle in caption
    is_contam, reason = check_competitor_contamination(caption="اشترك في قناة @ECKSDEAL لأحدث العروض")
    assert is_contam is True
    assert "ecksdeal" in reason

    # 3. Competitor t.me link in caption
    is_contam, reason = check_competitor_contamination(caption="زوروا قناتنا https://t.me/lodydeals")
    assert is_contam is True
    assert "lodydeals" in reason

    # 4. Unauthorized bot in caption
    is_contam, reason = check_competitor_contamination(caption="استخدم البوت @dzgamingcoinbot")
    assert is_contam is True
    assert "dzgamingcoinbot" in reason

    # 5. Competitor aff_fcid tracking ID
    is_contam, reason = check_competitor_contamination(url="https://www.aliexpress.com/item/123.html?aff_fcid=competitor123")
    assert is_contam is True
    assert "competitor123" in reason

    # 6. Clean post with our authorized bot and tracking
    is_contam, reason = check_competitor_contamination(
        caption="تخفيض ممتاز 💰 السعر: $15 🔥 بوت: @Alilo07BOT قناة: @DzAliexpress0",
        url="https://s.click.aliexpress.com/e/_c3F40Fvf"
    )
    assert is_contam is False
    assert reason is None

def test_strip_competitor_elements():
    raw = "عرض رائع من @ECKSDEAL تابعونا على t.me/lodydeals واستخدموا @otherbot"
    cleaned = strip_competitor_elements(raw)
    assert "@ECKSDEAL" not in cleaned
    assert "lodydeals" not in cleaned
    assert "@otherbot" not in cleaned

def test_caption_validator_blocks_competitor():
    caption_with_competitor = (
        "🔥 تخفيض قوي على المنتج\n"
        "السعر: $25.00\n"
        "رابط الشراء: https://s.click.aliexpress.com/e/_c38iyTZR\n"
        "بوت تخفيض العملات: @Alilo07BOT\n"
        "قناة: @DzAliexpress0\n"
        "منقول من @zedstoreonline"
    )
    val = caption_validator.validate(
        caption=caption_with_competitor,
        expected_title="منتج",
        expected_usd_price=25.0,
        expected_eur_price=23.0,
        expected_affiliate_url="https://s.click.aliexpress.com/e/_c38iyTZR"
    )
    assert val.approved is False
    assert any("VIOLATION OF CORE RULE" in err for err in val.errors)

@pytest.mark.asyncio
async def test_publisher_firewall_blocks_competitor():
    mock_session = AsyncMock()
    deal = Deal(
        id=999,
        affiliate_url="https://s.click.aliexpress.com/e/_c38iyTZR",
        title="Test Deal"
    )
    success, err = await telegram_publisher.publish_deal(
        session=mock_session,
        deal=deal,
        caption="Test caption with https://s.click.aliexpress.com/e/_c38iyTZR @DzAliexpress0 @Alilo07BOT",
        force=True
    )
    assert success is False
    assert "SECURITY RULE VIOLATION" in err
