import pytest
from unittest.mock import patch, AsyncMock
from app.publisher.admin_alerts import notify_admin_error, _ALERT_COOLDOWN_CACHE

@pytest.fixture(autouse=True)
def clear_alert_cache():
    _ALERT_COOLDOWN_CACHE.clear()
    yield
    _ALERT_COOLDOWN_CACHE.clear()

@pytest.mark.asyncio
async def test_notify_admin_error_missing_creds():
    with patch("app.publisher.admin_alerts.get_admin_credentials", return_value=("", None)):
        success = await notify_admin_error("Test Error", "Some details", channel="algeria")
        assert success is False

@pytest.mark.asyncio
async def test_notify_admin_error_success():
    with patch("app.publisher.admin_alerts.get_admin_credentials", return_value=("fake_token", 12345678)):
        with patch("httpx.AsyncClient.post") as mock_post:
            mock_post.return_value = AsyncMock(status_code=200, json=lambda: {"ok": True})
            success = await notify_admin_error("Sweeping Failed", "HTTP 403 on @channel", channel="algeria")
            assert success is True
            assert mock_post.called
            call_kwargs = mock_post.call_args[1]
            payload = call_kwargs["json"]
            assert payload["chat_id"] == 12345678
            assert "Sweeping Failed" in payload["text"]
            assert "@DzAliexpress0" in payload["text"]

@pytest.mark.asyncio
async def test_notify_admin_error_deduplication():
    with patch("app.publisher.admin_alerts.get_admin_credentials", return_value=("fake_token", 12345678)):
        with patch("httpx.AsyncClient.post") as mock_post:
            mock_post.return_value = AsyncMock(status_code=200, json=lambda: {"ok": True})
            # First call succeeds
            s1 = await notify_admin_error("Posting Error", "Error 400 Bad Request", channel="algeria")
            assert s1 is True
            assert mock_post.call_count == 1

            # Second identical call within cooldown is throttled
            s2 = await notify_admin_error("Posting Error", "Error 400 Bad Request", channel="algeria")
            assert s2 is False
            assert mock_post.call_count == 1
