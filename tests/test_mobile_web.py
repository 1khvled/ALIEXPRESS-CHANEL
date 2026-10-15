"""
Test suite for user-facing web app and mobile optimizations in api/user_site.py.
"""
import sys
import re
import json
from pathlib import Path

# Configure utf-8 stdout for Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Add repo root to sys.path
repo_root = Path(__file__).resolve().parent
sys.path.insert(0, str(repo_root))

def test_user_site_html():
    print("[1/6] Importing api.user_site.USER_WEBSITE_HTML...")
    try:
        from api.user_site import USER_WEBSITE_HTML
    except Exception as e:
        print(f"❌ Failed to import api.user_site: {e}")
        sys.exit(1)

    assert isinstance(USER_WEBSITE_HTML, str), "USER_WEBSITE_HTML must be a string"
    assert len(USER_WEBSITE_HTML) > 1000, "USER_WEBSITE_HTML is unexpectedly short"
    print(f"  ✓ Imported successfully ({len(USER_WEBSITE_HTML)} chars).")

    print("[2/6] Verifying mobile viewport & safe-area insets...")
    assert 'viewport-fit=cover' in USER_WEBSITE_HTML, "Missing viewport-fit=cover in viewport meta tag"
    assert 'env(safe-area-inset-bottom' in USER_WEBSITE_HTML, "Missing env(safe-area-inset-bottom) style"
    assert 'env(safe-area-inset-top' in USER_WEBSITE_HTML, "Missing env(safe-area-inset-top) style"
    assert 'bottom-nav-safe' in USER_WEBSITE_HTML, "Missing bottom-nav-safe class"
    assert 'apple-mobile-web-app-capable' in USER_WEBSITE_HTML, "Missing apple-mobile-web-app-capable meta"
    assert 'format-detection' in USER_WEBSITE_HTML, "Missing format-detection telephone=no"
    print("  ✓ Mobile viewport and safe-area insets verified.")

    print("[3/6] Verifying touch target guidelines (min 44px ergonomics)...")
    assert 'touch-action: manipulation' in USER_WEBSITE_HTML or 'touch-manipulation' in USER_WEBSITE_HTML, "Missing touch-manipulation"
    assert 'min-h-[44px]' in USER_WEBSITE_HTML or 'min-h-[48px]' in USER_WEBSITE_HTML, "Missing min-height 44px/48px touch targets"
    assert '-webkit-tap-highlight-color: transparent' in USER_WEBSITE_HTML, "Missing tap highlight removal"
    assert 'active:scale-' in USER_WEBSITE_HTML, "Missing active touch feedback scales"
    print("  ✓ Touch target guidelines & thumb feedback verified.")

    print("[4/6] Verifying mobile bottom navigation bar & bottom sheet modal...")
    assert 'id="deal-modal"' in USER_WEBSITE_HTML, "Missing deal-modal component"
    assert 'modal-container' in USER_WEBSITE_HTML, "Missing modal-container"
    assert ('id="mob-nav-all"' in USER_WEBSITE_HTML or 'id="mob-bottom-deals"' in USER_WEBSITE_HTML), "Missing bottom navigation items"
    assert 'animate-slide-up' in USER_WEBSITE_HTML, "Missing native bottom sheet slide animation"
    print("  ✓ Bottom navigation & native bottom sheet modal verified.")

    print("[5/6] Verifying image performance & lazy loading...")
    assert 'loading="lazy"' in USER_WEBSITE_HTML, "Missing loading='lazy'"
    assert 'decoding="async"' in USER_WEBSITE_HTML, "Missing decoding='async'"
    assert 'handleImgError' in USER_WEBSITE_HTML, "Missing handleImgError placeholder fallback"
    assert 'aspect-[4/3]' in USER_WEBSITE_HTML, "Missing aspect-[4/3] responsive aspect ratio"
    print("  ✓ Image lazy loading, async decoding, and placeholder handling verified.")

    print("[6/6] Verifying JSON-LD and HTML tag structure...")
    json_ld_match = re.search(r'<script type="application/ld\+json">(.*?)</script>', USER_WEBSITE_HTML, re.DOTALL)
    assert json_ld_match, "Missing JSON-LD script tag"
    schema_data = json.loads(json_ld_match.group(1).strip())
    assert schema_data.get("@type") == "WebSite", f"Unexpected schema type: {schema_data.get('@type')}"
    
    assert "<!DOCTYPE html>" in USER_WEBSITE_HTML, "Missing <!DOCTYPE html>"
    assert "<html" in USER_WEBSITE_HTML and "</html>" in USER_WEBSITE_HTML, "Unclosed <html> tag"
    assert "<head>" in USER_WEBSITE_HTML and "</head>" in USER_WEBSITE_HTML, "Unclosed <head> tag"
    assert "<body" in USER_WEBSITE_HTML and "</body>" in USER_WEBSITE_HTML, "Unclosed <body> tag"
    print("  ✓ Structured JSON-LD schema & HTML structure verified.")

    print("\n🎉 ALL CHECKS PASSED: Mobile optimization & ergonomics are in perfect state!")

if __name__ == "__main__":
    test_user_site_html()
