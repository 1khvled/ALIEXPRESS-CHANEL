import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.publisher.facebook import FacebookPublisher, get_high_res_aliexpress_image


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
    unconfigured = FacebookPublisher(page_id="", access_token="")
    assert unconfigured.is_configured() is False

    configured = FacebookPublisher(page_id="999888777", access_token="EAAB...")
    assert configured.is_configured() is True


@pytest.mark.asyncio
async def test_facebook_publish_deal_unconfigured():
    pub = FacebookPublisher(page_id="", access_token="")
    ok, post_id, err = await pub.publish_deal(caption="Test Caption")
    assert ok is False
    assert post_id is None
    assert "not configured" in err


def test_get_high_res_aliexpress_image():
    raw_urls = [
        ("https://ae-pic-a1.aliexpress-media.com/kf/S7a14e912440348cbbf99a779dd584fb7f.jpg_350x350.jpg", "https://ae-pic-a1.aliexpress-media.com/kf/S7a14e912440348cbbf99a779dd584fb7f.jpg"),
        ("https://ae01.alicdn.com/kf/H842938472.png_220x220.png", "https://ae01.alicdn.com/kf/H842938472.png"),
        ("https://ae-pic-a1.aliexpress-media.com/kf/S123.jpg_.webp", "https://ae-pic-a1.aliexpress-media.com/kf/S123.jpg"),
        ("https://ae01.alicdn.com/kf/S456.jpg_640x640Q90.jpg_.webp", "https://ae01.alicdn.com/kf/S456.jpg"),
        ("https://ae01.alicdn.com/kf/S456.jpg?extra=123", "https://ae01.alicdn.com/kf/S456.jpg"),
        ("https://example.com/banner.jpg", "https://example.com/banner.jpg"),
        (None, None),
        ("", None)
    ]
    for raw, expected in raw_urls:
        assert get_high_res_aliexpress_image(raw) == expected


@pytest.mark.asyncio
async def test_facebook_publish_deal_prioritizes_high_res_url():
    pub = FacebookPublisher(page_id="12345", access_token="token_xyz")

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"id": "photo_9999", "post_id": "12345_9999"}
        mock_post.return_value = mock_resp

        with patch("app.publisher.facebook.is_fb_duplicate", return_value=False):
            ok, post_id, err = await pub.publish_deal(
                caption="High Res Deal",
                deal_link="https://s.click.aliexpress.com/e/_test_high_res",
                image_url="https://ae01.alicdn.com/kf/S456.jpg_350x350.jpg",
                image_bytes=b"low_res_framed_bytes"
            )

        assert ok is True
        assert post_id == "12345_9999"
        # Check that post was called with URL payload and cleaned master image
        assert mock_post.called
        call_kwargs = mock_post.call_args.kwargs
        assert "data" in call_kwargs
        assert call_kwargs["data"]["url"] == "https://ae01.alicdn.com/kf/S456.jpg"
