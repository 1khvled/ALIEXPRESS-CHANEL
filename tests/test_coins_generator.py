"""
Unit tests for the Coins Deal Link Generator and backend link resolution.
"""
import pytest
from httpx import AsyncClient, ASGITransport
from api.index import app
from api.user_site import USER_WEBSITE_HTML


def test_coins_generator_html_components():
    """Verify that the interactive Coins Deal Link Generator is integrated into the site."""
    # Generator card and input
    assert 'id="coins-generator-card"' in USER_WEBSITE_HTML
    assert 'id="coins-input-url"' in USER_WEBSITE_HTML
    assert 'id="coins-submit-btn"' in USER_WEBSITE_HTML
    assert 'id="coins-paste-btn"' in USER_WEBSITE_HTML
    assert 'id="coins-gen-result"' in USER_WEBSITE_HTML
    assert 'id="coins-gen-out-coin"' in USER_WEBSITE_HTML
    assert 'id="coins-gen-btn-buy"' in USER_WEBSITE_HTML
    assert 'id="coins-gen-out-super"' in USER_WEBSITE_HTML
    assert 'id="coins-gen-btn-super"' in USER_WEBSITE_HTML
    assert 'id="coins-gen-out-bundle"' in USER_WEBSITE_HTML
    assert 'id="coins-gen-btn-bundle"' in USER_WEBSITE_HTML

    # Client-side generator JS functions and affiliate tracking ID
    assert 'const AFF_TRACKING_TAG = \'dzkhvled16\'' in USER_WEBSITE_HTML
    assert 'function extractAliExpressPid' in USER_WEBSITE_HTML
    assert 'function generateCoinLink' in USER_WEBSITE_HTML
    assert 'function copyCoinLink' in USER_WEBSITE_HTML
    assert 'sourceType=620&channel=coin' in USER_WEBSITE_HTML
    assert 'sourceType=561&channel=superdeal' in USER_WEBSITE_HTML
    assert 'BundleDeals2' in USER_WEBSITE_HTML

    # Modal shortcut
    assert 'tools_coin_generator' in USER_WEBSITE_HTML


def test_universal_viewport_overflow_prevention():
    """Verify universal viewport constraints are enforced in CSS."""
    assert 'overflow-x: hidden !important' in USER_WEBSITE_HTML
    assert 'max-width: 100vw !important' in USER_WEBSITE_HTML


@pytest.mark.asyncio
async def test_resolve_coin_link_api_endpoint():
    """Test the /api/resolve-coin-link endpoint with standard product URL."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Standard URL with product ID
        resp = await client.get("/api/resolve-coin-link?url=https://www.aliexpress.com/item/1005007421890123.html")
        assert resp.status_code == 200
        data = resp.json()
        assert data["ok"] is True
        assert data["product_id"] == "1005007421890123"
        assert "sourceType=620&channel=coin" in data["coin_link"]
        assert "aff_fcid=dzkhvled16" in data["coin_link"]
        assert "aff_fcid=dzkhvled16" in data["super_link"]
        assert "aff_fcid=dzkhvled16" in data["bundle_link"]
        assert "aff_fcid=dzkhvled16" in data["direct_link"]

        # Raw numeric ID
        resp2 = await client.get("/api/resolve-coin-link?url=1005006677889900")
        assert resp2.status_code == 200
        data2 = resp2.json()
        assert data2["ok"] is True
        assert data2["product_id"] == "1005006677889900"
        assert "aff_fcid=dzkhvled16" in data2["coin_link"]

        # Invalid URL returns 400
        resp3 = await client.get("/api/resolve-coin-link?url=https://google.com/search")
        assert resp3.status_code == 400
        data3 = resp3.json()
        assert data3["ok"] is False
