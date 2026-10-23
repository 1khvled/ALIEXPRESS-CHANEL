import pytest
from app.publisher.facebook import FacebookPublisher


def test_facebook_caption_formatter_strips_html_and_preserves_structure():
    publisher = FacebookPublisher(page_id="12345", access_token="token_xyz")
    telegram_html = """
🔥 <b>تخفيض مجنون على هاتف POCO X6 Pro!</b>

<blockquote>القطعة بـ <b>28,500 دج</b> بدلاً من <s>34,000 دج</s>!</blockquote>

استعمل كود الخصم: <code>ALILO11</code>
<a href="https://s.click.aliexpress.com/e/_test123">اضغط هنا للشراء من علي إكسبرس</a>
"""
    fb_text = publisher.format_caption_for_facebook(
        caption=telegram_html,
        deal_link="https://s.click.aliexpress.com/e/_test123",
        price=28500.0
    )

    # HTML tags removed
    assert "<b>" not in fb_text
    assert "</b>" not in fb_text
    assert "<blockquote>" not in fb_text
    assert "<s>" not in fb_text

    # Code tags converted
    assert "[ALILO11]" in fb_text

    # Link converted cleanly
    assert "اضغط هنا للشراء من علي إكسبرس 👉 https://s.click.aliexpress.com/e/_test123" in fb_text or "https://s.click.aliexpress.com/e/_test123" in fb_text

    # Facebook tags appended
    assert "#AliExpress" in fb_text
    assert "#تخفيضات" in fb_text


def test_facebook_is_configured():
    unconfigured = FacebookPublisher(page_id=None, access_token=None)
    assert unconfigured.is_configured() is False

    configured = FacebookPublisher(page_id="999888777", access_token="EAAB...")
    assert configured.is_configured() is True


@pytest.mark.asyncio
async def test_facebook_publish_deal_unconfigured():
    pub = FacebookPublisher(page_id=None, access_token=None)
    ok, post_id, err = await pub.publish_deal(caption="Test Caption")
    assert ok is False
    assert post_id is None
    assert "not configured" in err
