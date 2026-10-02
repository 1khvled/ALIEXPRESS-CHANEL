import pytest
from app.aliexpress.affiliate import DirectAffiliateProvider, CustomNetworkAffiliateProvider

@pytest.mark.asyncio
async def test_direct_affiliate_provider():
    provider = DirectAffiliateProvider(tracking_id="my_track_123")
    url = "https://www.aliexpress.com/item/1005006382910245.html"
    aff_link = await provider.generate_link(url, "1005006382910245")
    assert "aff_fcid=my_track_123" in aff_link
    assert "1005006382910245" in aff_link

@pytest.mark.asyncio
async def test_custom_network_affiliate_provider():
    prefix = "https://alitems.site/g/1e8d114494"
    provider = CustomNetworkAffiliateProvider(prefix)
    url = "https://www.aliexpress.com/item/1005006382910245.html"
    aff_link = await provider.generate_link(url)
    assert aff_link.startswith(prefix)
    assert "ulp=" in aff_link

def test_ensure_affiliate_guarantees():
    from api.coin_bot import ensure_affiliate

    # 1. Existing s.click link is preserved intact
    sclick = "https://s.click.aliexpress.com/e/_c3zd64nn"
    assert ensure_affiliate(sclick) == sclick

    # 2. Raw URL adopts fallback s.click link
    raw = "https://www.aliexpress.com/item/1005008080932874.html"
    assert ensure_affiliate(raw, fallback_link=sclick) == sclick

    # 3. Raw URL without fallback s.click receives tracking parameter aff_fcid
    assert "aff_fcid=dzkhvled16" in ensure_affiliate(raw, pid="1005008080932874")

    # 4. None / empty link returns monetized URL
    empty_res = ensure_affiliate(None, pid="1005008080932874")
    assert "aff_fcid=dzkhvled16" in empty_res
    assert "1005008080932874" in empty_res

@pytest.mark.asyncio
async def test_coin_discount_response_monetization():
    from api.coin_bot import generate_coin_discount_response

    pid = "1005008080932874"
    res = await generate_coin_discount_response(pid)

    for key in ["product_link", "coin_link", "bundle_link", "super_link", "limited_link"]:
        link = res.get(key, "")
        assert link, f"Missing {key}"
        assert ("s.click.aliexpress.com" in link or "aff_fcid=dzkhvled16" in link), f"{key} ({link}) is not monetized!"

    # Verify inline keyboard buttons
    for row in res["reply_markup"]["inline_keyboard"]:
        for btn in row:
            url = btn.get("url", "")
            if "aliexpress.com" in url:
                assert ("s.click.aliexpress.com" in url or "aff_fcid=dzkhvled16" in url), f"Button {btn['text']} ({url}) is not monetized!"

