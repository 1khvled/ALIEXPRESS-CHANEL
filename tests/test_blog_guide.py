from bs4 import BeautifulSoup
from fastapi.testclient import TestClient
from api.index import app, parse_telegram_deal_block

client = TestClient(app)

def test_blog_guide_route():
    response = client.get("/blog/aliexpress-algeria-guide-dz")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    html = response.text
    # Check title and meta
    assert "دليل الشراء من AliExpress في الجزائر 2026" in html
    assert "Bybit" in html
    assert "RedotPay" in html
    assert "AliExpress Standard Shipping" in html
    assert "الجمارك" in html
    assert "schema.org" in html
    assert '"@type": "Article"' in html
    assert '"@type": "FAQPage"' in html
    assert "DealScout DZ" in html

def test_blog_guide_aliases():
    for path in ["/guide", "/blog"]:
        response = client.get(path)
        assert response.status_code == 200
        assert "دليل الشراء من AliExpress في الجزائر 2026" in response.text

def test_sitemap_and_robots_include_blog():
    sitemap = client.get("/sitemap.xml").text
    assert "/blog/aliexpress-algeria-guide-dz" in sitemap

    robots = client.get("/robots.txt").text
    assert "Allow: /blog/aliexpress-algeria-guide-dz" in robots

def test_country_completion_and_tatweel():
    """Verify that 'خلي البلد' and tatweels are correctly completed to full country strings with flags."""
    test_cases = [
        ("📍 خلي البلـــد كــــوريا 🇰🇷", "كوريا 🇰🇷"),
        ("📍 خلي البلد", "كندا 🇨🇦"),
        ("📍 خلي البلـد كندا", "كندا 🇨🇦"),
        ("📍 خلي البلد : كندا 🇨🇦", "كندا 🇨🇦"),
        ("بلد الحساب : أوكرانيا", "أوكرانيا 🇺🇦"),
        ("فرنسا 🇫🇷 توصيل سريع", "فرنسا 🇫🇷"),
        ("عروض خاصة بـ الجزائر 🇩🇿", "الجزائر 🇩🇿"),
        ("استراليا 🇦🇺 تخفيض قوي", "أستراليا 🇦🇺"),
        ("📍 خلي البلــــــد", "كندا 🇨🇦"),
    ]
    for text, expected in test_cases:
        html = f'<div data-post="DzAliexpress0/123"><div class="tgme_widget_message_text">{text}<br>https://s.click.aliexpress.com/e/_test</div></div>'
        soup = BeautifulSoup(html, "html.parser")
        deal = parse_telegram_deal_block(soup.find("div"), clean_ch="DzAliexpress0", usdt_rate=250.0)
        assert deal is not None
        assert deal["country"] == expected, f"Failed on input: {text!r}, got: {deal['country']!r}, expected: {expected!r}"

def test_tracking_sources_in_api():
    """Verify that 17TRACK and Postal Ninja are included as reliable tracking sources in the API."""
    from api.parcel_tracker import get_direct_tracking_links
    links = get_direct_tracking_links("RB123456789SG")
    assert "track17" in links
    assert "https://t.17track.net/ar#nums=RB123456789SG" == links["track17"]
    assert "postal_ninja" in links
    assert "https://postal.ninja/ar/track/RB123456789SG" == links["postal_ninja"]
    assert "cainiao" in links
    assert "algerie_poste" in links

    resp = client.get("/api/track-parcel?num=RB123456789SG")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ok"] is True
    assert "source_provider" in data
    assert "17TRACK" in data["source_provider"]["name"]

    home = client.get("/").text
    assert "btn-portal-17track" in home
    assert "btn-portal-ninja" in home
    assert "Postal Ninja" in home

