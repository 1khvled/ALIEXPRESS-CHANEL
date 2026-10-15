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
    assert '<link rel="canonical" href="https://dealscout-green.vercel.app/">' in html
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
    """Verify Schema.org WebSite, Organization, CollectionPage and dynamic ItemList markup."""
    html = USER_WEBSITE_HTML
    assert '"@type": "WebSite"' in html
    assert '"@type": "Organization"' in html
    assert '"@type": "CollectionPage"' in html
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
    assert "Disallow: /admin" in text
    assert "Disallow: /api/" in text
    assert "Sitemap: https://dealscout-green.vercel.app/sitemap.xml" in text


def test_sitemap_xml_route():
    """Verify /sitemap.xml response code, valid XML format, and URLs."""
    response = client.get("/sitemap.xml")
    assert response.status_code == 200
    assert "application/xml" in response.headers.get("content-type", "") or "text/xml" in response.headers.get("content-type", "")
    assert "public, max-age=3600" in response.headers.get("cache-control", "")
    
    # Check valid XML parsing
    root = ET.fromstring(response.text)
    assert "urlset" in root.tag
    
    urls = [elem.text for elem in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
    assert "https://dealscout-green.vercel.app/" in urls
    assert "https://dealscout-green.vercel.app/deals" in urls


def test_public_web_routes():
    """Verify / and /deals return 200 with USER_WEBSITE_HTML."""
    r_home = client.get("/")
    assert r_home.status_code == 200
    assert "text/html" in r_home.headers.get("content-type", "")
    assert "DealScout DZ" in r_home.text

    r_deals = client.get("/deals")
    assert r_deals.status_code == 200
    assert "text/html" in r_deals.headers.get("content-type", "")
    assert "DealScout DZ" in r_deals.text
