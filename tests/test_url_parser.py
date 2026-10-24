import pytest
from app.aliexpress.urls import (
    extract_all_urls,
    is_aliexpress_url,
    is_potential_shortener,
    extract_product_id_from_url,
    normalize_aliexpress_url
)

def test_extract_all_urls():
    text = (
        "Check this deal: https://www.aliexpress.com/item/1005006382910245.html! "
        "Also see https://a.aliexpress.com/_mt8123 and bit.ly/3xyz."
    )
    urls = extract_all_urls(text)
    assert len(urls) >= 2
    assert "https://www.aliexpress.com/item/1005006382910245.html" in urls
    assert "https://a.aliexpress.com/_mt8123" in urls

def test_extract_bare_aliexpress_urls():
    # Test bare domain without https:// and with touching Arabic text
    text = "🔥رابط s.click.aliexpress.com/e/_c4LARstxكوبون 15/119$ : OTPRD15"
    urls = extract_all_urls(text)
    assert len(urls) == 1
    assert urls[0] == "https://s.click.aliexpress.com/e/_c4LARstx"

    text2 = "🔥الرابط : s.click.aliexpress.com/e/_c3b0oYB7ضع البلد الجزائر 🇩🇿"
    urls2 = extract_all_urls(text2)
    assert len(urls2) == 1
    assert urls2[0] == "https://s.click.aliexpress.com/e/_c3b0oYB7"

def test_is_aliexpress_url():
    assert is_aliexpress_url("https://www.aliexpress.com/item/1005006382910245.html")
    assert is_aliexpress_url("https://a.aliexpress.com/_mt8123")
    assert is_aliexpress_url("https://s.click.aliexpress.com/e/_DFxyz")
    assert not is_aliexpress_url("https://amazon.com/dp/B08XYZ")

def test_is_potential_shortener():
    assert is_potential_shortener("https://bit.ly/3xyz")
    assert is_potential_shortener("https://tinyurl.com/abc12")
    assert not is_potential_shortener("https://www.aliexpress.com")

def test_extract_product_id_from_url():
    # Canonical format
    url1 = "https://www.aliexpress.com/item/1005006382910245.html"
    assert extract_product_id_from_url(url1) == "1005006382910245"

    # Query param format
    url2 = "https://aliexpress.com/item?productId=1005006382910245&spm=a2g0o"
    assert extract_product_id_from_url(url2) == "1005006382910245"

    # Url with path without .html
    url3 = "https://aliexpress.com/item/1005006382910245"
    assert extract_product_id_from_url(url3) == "1005006382910245"

def test_normalize_aliexpress_url():
    dirty_url = (
        "https://www.aliexpress.com/item/1005006382910245.html"
        "?spm=a2g0o.productlist.main.1.1234&algo_pvid=abcd-1234&aff_fcid=oldaff"
    )
    clean = normalize_aliexpress_url(dirty_url)
    assert clean == "https://www.aliexpress.com/item/1005006382910245.html"


def test_bundle_deals_url_product_id():
    bundle_url = (
        "https://www.aliexpress.com/ssr/300000512/BundleDeals2?disableNav=YES"
        "&pha_manifest=ssr&_immersiveMode=true&productIds=1005007027334636"
        "&aff_fcid=abcd123"
    )
    assert extract_product_id_from_url(bundle_url) == "1005007027334636"


@pytest.mark.asyncio
async def test_resolve_any_ali_link_history_resolution(monkeypatch):
    from api.coin_bot import resolve_any_ali_link
    import httpx

    # Test resolving bare s.click that redirects to bundledeals with productIds
    class DummyHistory:
        def __init__(self, url):
            self.url = url
            self.headers = {}

    class DummyResponse:
        def __init__(self):
            self.url = "https://www.aliexpress.com/p/error/404.html"
            self.headers = {}
            self.text = "Error 404"
            self.history = [
                DummyHistory("https://s.click.aliexpress.com/e/_mockTest"),
                DummyHistory("https://www.aliexpress.com/ssr/300000512/BundleDeals2?productIds=1005007027334636&aff_fcid=123")
            ]

    class MockAsyncClient:
        def __init__(self, *args, **kwargs):
            pass
        async def __aenter__(self):
            return self
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass
        async def get(self, url, headers=None):
            return DummyResponse()

    monkeypatch.setattr(httpx, "AsyncClient", MockAsyncClient)

    sample_post = (
        "\"عودة SSD بكمية قليلة ألحق 🏃\"\n"
        "📍 أختر بلد الحساب الجزائر 🇩🇿\n"
        "✔️ ضف 3 قطع ثم أدفع\n\n"
        "⭐️ 3 SOMNAMBULIST SSD (128g)\n"
        "💵 السعر : 28.5 $ 🔥\n"
        "🔗 باندل: https://s.click.aliexpress.com/e/_mockTest"
    )

    pid = await resolve_any_ali_link(sample_post)
    assert pid == "1005007027334636"


def test_detect_deal_type_coin_and_accessories():
    from app.aliexpress.parser import detect_deal_type

    # Accessories with tech keywords must default to coin, not item
    assert detect_deal_type("Aluminum Laptop Stand", "https://aliexpress.com/item/1005013413640708.html") == "coin"
    assert detect_deal_type("360° Clip Mobile Phone Holder", "https://aliexpress.com/item/1005013423507579.html") == "coin"
    assert detect_deal_type("KUULAA USB C 60W Cable", "https://aliexpress.com/item/1005008901941749.html") == "coin"
    assert detect_deal_type("Redmi Note 13 Pro Case Cover", "https://aliexpress.com/item/100500123.html") == "coin"

    # Even high-value phones default to coin for max discount unless it is a bundle
    assert detect_deal_type("POCO X6 Pro 5G Global Version", "https://aliexpress.com/item/100500456.html") == "item"

    # Bundle deals check
    bundle_text = "عروض الحزم Choice Bundle ضف 3 قطع للحصول على الشحن المجاني"
    assert detect_deal_type(bundle_text, "https://aliexpress.com/ssr/300000512/BundleDeals2") == "bundle"


def test_product_extractor_url_priority():
    from app.aliexpress.urls import extract_all_urls

    text = """
    عرض لافار ممتاز
    رابط مباشر: https://s.click.aliexpress.com/e/_c40Ifxnh
    خصم النقاط: https://s.click.aliexpress.com/e/_c3CYrQtt
    """
    urls = extract_all_urls(text)
    ali_urls = [u for u in urls if "aliexpress" in u]

    def _url_priority(u: str) -> int:
        u_low = u.lower()
        if "coin" in u_low or "sourcetype=620" in u_low or "channel=coin" in u_low:
            return 0
        idx = text.find(u)
        if idx > 0:
            prefix = text[max(0, idx - 45):idx].lower()
            if any(k in prefix for k in ["نقاط", "عملات", "coins", "خصم النقاط", "تخفيض العملات", "تخفيض النقاط", "رابط العملات"]):
                return 0
            if any(k in prefix for k in ["مباشر", "direct", "رابط مباشر", "عادي"]):
                return 1
        return 2

    ali_urls.sort(key=_url_priority)
    # The coin discount link MUST be sorted first
    assert ali_urls[0] == "https://s.click.aliexpress.com/e/_c3CYrQtt"
    assert ali_urls[1] == "https://s.click.aliexpress.com/e/_c40Ifxnh"
