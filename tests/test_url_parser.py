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
