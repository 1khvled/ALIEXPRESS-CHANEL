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
