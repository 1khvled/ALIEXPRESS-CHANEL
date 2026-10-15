"""
Tests for official logo serving, coupon extraction, and product title parsing.
Verifies:
- Official logo endpoints (/logo.png and /logo_circular.png) return HTTP 200 image/png.
- User website embeds the official logo in navbar, footer, and OpenGraph metadata.
- Product titles are cleanly extracted from posts with hooks/flags (e.g., HONOR 600 Lite).
- Comprehensive coupon extraction for varied competitor and French/Arabic channel formats.
"""
import pytest
from fastapi.testclient import TestClient
from api.index import app
from api.user_site import USER_WEBSITE_HTML
from app.aliexpress.parser import extract_clean_title, extract_coupon, extract_seller_coupon

client = TestClient(app)


def test_logo_endpoints():
    """Verify /logo.png and /logo_circular.png return HTTP 200 and image/png."""
    resp_logo = client.get("/logo.png")
    assert resp_logo.status_code == 200
    assert "image/png" in resp_logo.headers.get("content-type", "")
    assert len(resp_logo.content) > 10000

    resp_circ = client.get("/logo_circular.png")
    assert resp_circ.status_code == 200
    assert "image/png" in resp_circ.headers.get("content-type", "")
    assert len(resp_circ.content) > 10000


def test_logo_in_website_html():
    """Verify official logo is referenced in navbar, footer, favicon, and og:image."""
    html = USER_WEBSITE_HTML
    assert 'src="/logo_circular.png"' in html
    assert "this.src='/logo.png'" in html or 'src="/logo.png"' in html
    assert '<link rel="icon" type="image/png" href="/logo_circular.png">' in html
    assert '<meta property="og:image" content="https://dealscoutgreen.vercel.app/logo.png">' in html


def test_extract_clean_title_with_checkmark_and_hooks():
    """Verify title is cleanly extracted when post has hooks and country instructions."""
    post_text = (
        "🔥 لافار ممتازة بأقوى سعر 🔥\n"
        "📍 خلي البلـــد كــــــندا 🇨🇦\n"
        "✅ HONOR 600 Lite 5G Global Version 8GB+256GB\n"
        "💰 السعر : $189.99 🔥\n"
        "🎟️ كـوبون الخصم : DZ15\n"
        "🛒 رابط الشراء ⤵️\n"
        "https://s.click.aliexpress.com/e/_oEN3d53"
    )
    title = extract_clean_title(post_text)
    assert title is not None
    assert "HONOR 600 Lite 5G" in title
    assert "لافار" not in title
    assert "كندا" not in title


def test_extract_clean_title_french_channel():
    """Verify French channel deal titles are cleanly extracted."""
    post_text = (
        "🔥 Excellente affaire à saisir rapidement !\n"
        "🚚 Livraison : France métropolitaine 🇫🇷\n"
        "✅ Casque Gamer Razer BlackShark V2 X\n"
        "💰 Prix : 39.99€\n"
        "🏷️ Code promo : RAZER10\n"
        "https://s.click.aliexpress.com/e/_oEN3d53"
    )
    title = extract_clean_title(post_text)
    assert title is not None
    assert "Razer BlackShark V2 X" in title
    assert "Excellente" not in title
    assert "France" not in title


def test_extract_coupon_formats():
    """Verify coupon extraction across various Telegram channel formats."""
    # 1. Emoji prefix only
    assert extract_coupon("🏷️ FR15") == "FR15"
    assert extract_coupon("🎟️ DZ10") == "DZ10"

    # 2. Definite article in Arabic
    assert extract_coupon("الكود : SUMMER10") == "SUMMER10"
    assert extract_coupon("الكوبون : AE05") == "AE05"

    # 3. French phrasing
    assert extract_coupon("Code promo : PROMO20") == "PROMO20"
    assert extract_coupon("Utilisez le code : LOVE14") == "LOVE14"
    assert extract_coupon("Avec le code : BONPLAN5") == "BONPLAN5"

    # 4. Tatweels in Arabic
    assert extract_coupon("كـوبون الخصم : DZ15") == "DZ15"
    assert extract_coupon("كـود : FAST05") == "FAST05"

    # 5. HTML code tags
    assert extract_coupon("Code promo : <code>PROMO10</code>") == "PROMO10"
    assert extract_coupon("كود الخصم: <code>DZ25</code>") == "DZ25"


def test_extract_seller_coupon():
    """Verify seller coupon parsing."""
    assert extract_seller_coupon("قسيمة المتجر : 5$") == "5$"
    assert extract_seller_coupon("🌷 قسيمة البائع : 2$") == "2$"
