"""
Unit and regression tests for SEO enhancements on DealScout DZ.
Verifies metadata, structured data, canonical tags, OpenGraph, Twitter cards,
semantic HTML hierarchy, robots.txt, and sitemap.xml.
"""
import pytest
import xml.etree.ElementTree as ET
from fastapi.testclient import TestClient
from api.user_site import USER_WEBSITE_HTML
from api.index import app


client = TestClient(app)


def test_seo_metadata_in_user_site_html():
    """Verify presence of canonical URL, meta keywords, and geo tags."""
    html = USER_WEBSITE_HTML
    assert '<link rel="canonical" href="https://dealscoutgreen.vercel.app/">' in html
    assert '<meta name="robots" content="index, follow">' in html
    assert 'name="keywords"' in html
    assert 'name="geo.region" content="DZ"' in html
    assert 'name="geo.placename" content="Algeria"' in html
    assert 'name="language" content="Arabic"' in html
    assert 'hreflang="ar"' in html
    assert 'hreflang="ar-DZ"' in html


def test_opengraph_and_twitter_cards():
    """Verify complete OpenGraph and Twitter card metadata."""
    html = USER_WEBSITE_HTML
    assert 'property="og:site_name" content="DealScout DZ"' in html
    assert 'property="og:locale" content="ar_DZ"' in html
    assert 'property="og:locale:alternate" content="fr_DZ"' in html
    assert 'property="og:image"' in html
    assert 'name="twitter:card" content="summary_large_image"' in html
    assert 'name="twitter:site" content="@DzAliexpress0"' in html


def test_schema_org_structured_data():
    """Verify Schema.org WebSite, Organization, CollectionPage, FAQPage and dynamic ItemList markup."""
    html = USER_WEBSITE_HTML
    assert '"@type": "WebSite"' in html
    assert '"@type": "Organization"' in html
    assert '"@type": "CollectionPage"' in html
    assert '"@type": "FAQPage"' in html
    assert '"SearchAction"' in html
    assert 'updateDealsStructuredData' in html
    assert '"@type": "ItemList"' in html


def test_semantic_html_structure():
    """Verify semantic tags h1, h2, h3, header, main, nav, and footer."""
    html = USER_WEBSITE_HTML
    assert "<h1" in html
    assert "</h1>" in html
    assert "<h2" in html
    assert "</h2>" in html
    assert "<h3" in html
    assert "<header" in html
    assert "<main" in html
    assert "<nav" in html
    assert '<footer role="contentinfo"' in html
    assert 'aria-label=' in html


def test_robots_txt_route():
    """Verify /robots.txt response code, headers, and rules."""
    response = client.get("/robots.txt")
    assert response.status_code == 200
    assert "text/plain" in response.headers.get("content-type", "")
    assert "public, max-age=86400" in response.headers.get("cache-control", "")
    text = response.text
    assert "Allow: /" in text
    assert "Allow: /deals" in text
    assert "Allow: /cards" in text
    assert "Allow: /coins" in text
    assert "Allow: /faq" in text
    assert "Allow: /about" in text
    assert "Allow: /contact" in text
    assert "Disallow: /admin" in text
    assert "Disallow: /api/" in text
    assert "Sitemap: https://dealscoutgreen.vercel.app/sitemap.xml" in text


def test_sitemap_xml_route():
    """Verify /sitemap.xml response code, valid XML format, and all 6 canonical URLs."""
    response = client.get("/sitemap.xml")
    assert response.status_code == 200
    assert "application/xml" in response.headers.get("content-type", "") or "text/xml" in response.headers.get("content-type", "")
    assert "public, max-age=3600" in response.headers.get("cache-control", "")
    
    # Check valid XML parsing
    root = ET.fromstring(response.text)
    assert "urlset" in root.tag
    
    urls = [elem.text for elem in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
    assert "https://dealscoutgreen.vercel.app/" in urls
    assert "https://dealscoutgreen.vercel.app/deals" in urls
    assert "https://dealscoutgreen.vercel.app/cards" in urls
    assert "https://dealscoutgreen.vercel.app/coins" in urls
    assert "https://dealscoutgreen.vercel.app/faq" in urls
    assert "https://dealscoutgreen.vercel.app/about" in urls
    assert "https://dealscoutgreen.vercel.app/contact" in urls


def test_public_web_routes():
    """Verify all 6 public routes return 200 with USER_WEBSITE_HTML."""
    for path in ["/", "/deals", "/cards", "/coins", "/faq", "/about", "/contact"]:
        r = client.get(path)
        assert r.status_code == 200
        assert "text/html" in r.headers.get("content-type", "")
        assert "DealScout DZ" in r.text


def test_active_event_api_and_seo_banner(monkeypatch):
    """Verify active event API and active event banner with SEO keywords."""
    from app.aliexpress.promos import PromoEvent
    from datetime import datetime, timezone, timedelta

    mock_event = PromoEvent(
        name="Winter Offers",
        name_ar="عروض الشتاء",
        name_fr="Offres d'Hiver",
        start_date=datetime.now(timezone.utc) - timedelta(days=1),
        end_date=datetime.now(timezone.utc) + timedelta(days=2),
        is_major=True,
        coupon_tiers=[
            {"spend": 39, "discount": 5, "code": "WOAE06"},
            {"spend": 269, "discount": 35, "code": "WOAE35"}
        ],
        banner_tag="تخفيضات عروض الشتاء"
    )
    monkeypatch.setattr("app.aliexpress.promos.promo_tracker.get_active_promo", lambda *args, **kwargs: mock_event)

    # 1. API endpoint check with active event
    resp = client.get("/api/active-event")
    assert resp.status_code == 200
    data = resp.json()
    assert "active_event" in data
    assert data["active_event"] is not None
    assert "Winter Offers" in data["active_event"]["name"]
    assert any("WOAE" in c for c in data["active_event"]["codes"])

    # 2. Page HTML check with active event SEO
    html_resp = client.get("/")
    assert html_resp.status_code == 200
    html = html_resp.text
    assert 'id="active-event-banner"' in html
    assert 'id="active-deals-keywords"' in html
    assert 'WOAE06' in html
    assert 'WOAE35' in html
    assert 'عروض الشتاء' in html

    # 3. API endpoint check when no event is active
    monkeypatch.setattr("app.aliexpress.promos.promo_tracker.get_active_promo", lambda *args, **kwargs: None)
    resp_inactive = client.get("/api/active-event")
    assert resp_inactive.status_code == 200
    assert resp_inactive.json() == {"active": False, "event": None}


def test_llms_txt_and_full_endpoints():
    """Verify /llms.txt and /llms-full.txt routes follow llmstxt.org specification."""
    # 1. Standard llms.txt
    resp = client.get("/llms.txt")
    assert resp.status_code == 200
    assert "text/plain" in resp.headers.get("content-type", "")
    assert "public, max-age=3600" in resp.headers.get("cache-control", "")
    text = resp.text
    assert "# DealScout DZ" in text
    assert "Core Features & Capabilities" in text
    assert "BaridiMob & Binance P2P Payment Guide" in text
    assert "AliExpress Coins Discount Generator" in text
    assert "https://dealscoutgreen.vercel.app/llms-full.txt" in text

    # 2. Extended llms-full.txt
    resp_full = client.get("/llms-full.txt")
    assert resp_full.status_code == 200
    assert "text/plain" in resp_full.headers.get("content-type", "")
    text_full = resp_full.text
    assert "Complete AI & LLM Knowledge Base" in text_full
    assert "Bybit" in text_full
    assert "RedotPay" in text_full
    assert "Algérie Poste" in text_full


def test_ai_summary_endpoint():
    """Verify /api/ai-summary provides structured JSON data for AI agents."""
    resp = client.get("/api/ai-summary")
    assert resp.status_code == 200
    assert "application/json" in resp.headers.get("content-type", "")
    data = resp.json()
    assert data["platform"] == "DealScout DZ"
    assert data["country"] == "Algeria"
    assert data["iso_code"] == "DZ"
    assert "currency_context" in data
    assert "payment_workflow" in data
    assert any("Bybit" in card["name"] for card in data["payment_workflow"]["destination_cards"])
    assert "telegram_channels" in data
    assert "DzAliexpress0" in data["telegram_channels"]["algeria_deals"]
    assert any("Coins" in tool["name"] for tool in data["core_tools"])


def test_ai_crawlers_in_robots_txt():
    """Verify robots.txt explicitly allows major Generative AI bots and points to llms.txt."""
    resp = client.get("/robots.txt")
    assert resp.status_code == 200
    text = resp.text
    assert "User-agent: GPTBot" in text
    assert "User-agent: ChatGPT-User" in text
    assert "User-agent: PerplexityBot" in text
    assert "User-agent: ClaudeBot" in text
    assert "User-agent: Google-Extended" in text
    assert "User-agent: Applebot-Extended" in text
    assert "Allow: /llms.txt" in text
    assert "Allow: /llms-full.txt" in text


def test_geo_schema_and_on_page_elements():
    """Verify WebApplication schema, SpeakableSpecification, and AI Overview facts block."""
    html = USER_WEBSITE_HTML
    # Alternate link in head
    assert '<link rel="alternate" type="text/plain" href="https://dealscoutgreen.vercel.app/llms.txt"' in html
    # Schema.org WebApplication for Coins tool
    assert '"@type": "WebApplication"' in html
    assert 'AliExpress Coins Deal Discount Link Generator Algeria' in html
    # Schema.org SpeakableSpecification
    assert '"@type": "SpeakableSpecification"' in html
    assert '#ai-overview-facts' in html
    # On-page AI Overview facts block
    assert 'id="ai-overview-facts"' in html
    assert 'data-i18n="geo_badge"' in html
    assert 'data-i18n="geo_summary_title"' in html


def test_tracking_web_route():
    """Verify /tracking route returns 200 with the tracking page markup."""
    resp = client.get("/tracking")
    assert resp.status_code == 200
    assert "text/html" in resp.headers.get("content-type", "")
    html = resp.text
    assert 'id="page-tracking"' in html
    assert 'id="tracking-input-num"' in html
    assert 'id="tracking-carrier-badge"' in html
    assert 'id="tracking-stages-container"' in html
    assert 'id="YQContainer"' in html
    assert 'nav-link-tracking' in html
    assert 'mob-bottom-tracking' in html


def test_tracking_api_endpoint():
    """Verify /api/track-parcel responds with carrier info and delivery stages."""
    # Cainiao Choice format
    resp = client.get("/api/track-parcel?num=LP00612345678901")
    assert resp.status_code == 200
    data = resp.json()
    assert data["tracking_number"] == "LP00612345678901"
    assert data["carrier"]["id"] == "cainiao"
    assert "delivery_stages" in data
    assert len(data["delivery_stages"]) == 5
    assert "direct_links" in data
    assert "track17" in data["direct_links"]

    # Algérie Poste format
    resp_dz = client.get("/api/track-parcel?num=RE123456789DZ")
    assert resp_dz.status_code == 200
    data_dz = resp_dz.json()
    assert data_dz["carrier"]["id"] == "algerie_poste"

    # Missing / empty number
    resp_empty = client.get("/api/track-parcel?num=")
    assert resp_empty.status_code == 400


def test_parcel_tracker_carrier_detection():
    """Verify parcel carrier auto-detection patterns for Algeria packages."""
    from api.parcel_tracker import detect_carrier

    assert detect_carrier("LP00123456789012")["id"] == "cainiao"
    assert detect_carrier("RE987654321DZ")["id"] == "algerie_poste"
    assert detect_carrier("SY12345678901")["id"] == "sunyou"
    assert detect_carrier("UJ123456789YP")["id"] == "yanwen"
    assert detect_carrier("RB123456789SG")["id"] == "singapore_post"
    assert detect_carrier("RA123456789CN")["id"] == "china_post"
    assert detect_carrier("RR123456789NL")["id"] == "upu_standard"


def test_sitemap_and_robots_tracking():
    """Verify sitemap.xml and robots.txt include /tracking."""
    sitemap_resp = client.get("/sitemap.xml")
    assert sitemap_resp.status_code == 200
    assert "<loc>https://dealscoutgreen.vercel.app/tracking</loc>" in sitemap_resp.text

    robots_resp = client.get("/robots.txt")
    assert robots_resp.status_code == 200
    assert "Allow: /tracking" in robots_resp.text

