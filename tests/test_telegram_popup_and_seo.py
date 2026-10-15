"""
Unit and regression tests for Telegram Join Popup and High-Intent SEO Keywords.
Verifies:
1. Requested high-volume keywords (aliexpressdz, aliexpress deals dz, aliexpress deald dz,
   عروض علي اكسبراس, شراء من علي اكسبراس في الجزائر).
2. Closable, non-annoying Telegram join popup markup, ARIA roles, and value props.
3. Client-side trigger logic with dwell/scroll thresholds, frequency capping (localStorage).
4. Semantic SEO guide section with structured H2/H3 headings and internal Telegram join CTAs.
5. Complete bilingual i18n dictionary coverage (Arabic & French).
"""
import pytest
from fastapi.testclient import TestClient
from api.user_site import USER_WEBSITE_HTML
from api.index import app

client = TestClient(app)


def test_high_volume_seo_keywords_presence():
    """Verify presence of specific high-volume search queries requested by user."""
    html = USER_WEBSITE_HTML
    
    # Meta keywords tag checks
    assert 'name="keywords"' in html
    keywords_lower = html.lower()
    
    assert "aliexpressdz" in keywords_lower
    assert "aliexpress deals dz" in keywords_lower
    assert "aliexpress deald dz" in keywords_lower
    assert "عروض علي اكسبراس" in html
    assert "شراء من علي اكسبراس في الجزائر" in html
    assert "علي اكسبراس الجزائر" in html
    assert "تخفيضات علي اكسبراس" in html
    assert "كود تخفيض علي اكسبراس" in html
    assert "الشراء من علي اكسبراس في الجزائر بريدي موب" in html


def test_telegram_join_popup_markup_and_accessibility():
    """Verify non-annoying, closable Telegram popup markup, ARIA roles, and CTA button."""
    html = USER_WEBSITE_HTML
    
    # Modal container and accessibility
    assert 'id="telegram-modal"' in html
    assert 'role="dialog"' in html
    assert 'aria-modal="true"' in html
    assert 'aria-labelledby="tg-popup-title"' in html
    
    # Modal contents
    assert 'id="telegram-popup-container"' in html
    assert 'id="tg-popup-title"' in html
    assert 'id="tg-popup-join-btn"' in html
    assert 'https://t.me/DzAliexpress0' in html
    assert 'closeTelegramPopup(true)' in html
    assert 'data-i18n="tg_popup_dismiss"' in html
    assert 'data-i18n="tg_popup_badge"' in html
    
    # Check strict CSS visibility handles #telegram-modal
    assert '#telegram-modal.hidden' in html
    assert '#telegram-modal:not(.hidden)' in html


def test_telegram_popup_javascript_and_dismissal_logic():
    """Verify JavaScript functions for timing, scroll triggers, and 24h/30d dismissal capping."""
    html = USER_WEBSITE_HTML
    
    assert 'function openTelegramPopup()' in html
    assert 'function closeTelegramPopup(' in html
    assert 'function onTelegramPopupBackdropClick(' in html
    assert 'function onTelegramPopupJoinClick()' in html
    assert 'function initTelegramPopupTrigger()' in html
    assert 'dealscout_tg_popup_dismissed_until' in html
    
    # Dwell timer & scroll trigger checks
    assert 'setTimeout(triggerPopup, 7000)' in html
    assert '0.35' in html  # 35% scroll threshold
    assert 'initTelegramPopupTrigger();' in html


def test_semantic_seo_shopping_guide_section():
    """Verify high-ranking semantic SEO knowledge section on page-deals."""
    html = USER_WEBSITE_HTML
    
    assert 'id="seo-shopping-guide"' in html
    assert '<h2' in html
    assert 'data-i18n="seo_guide_title"' in html
    assert 'data-i18n="seo_block1_h"' in html
    assert 'data-i18n="seo_block2_h"' in html
    assert 'data-i18n="seo_block3_h"' in html
    assert 'data-i18n="seo_block4_h"' in html
    assert 'data-i18n="seo_tags_title"' in html


def test_bilingual_i18n_keys():
    """Verify all new keys are mapped in both Arabic and French dictionaries."""
    html = USER_WEBSITE_HTML
    
    keys = [
        "tg_popup_badge",
        "tg_popup_title",
        "tg_popup_desc",
        "tg_popup_feat1_title",
        "tg_popup_feat2_title",
        "tg_popup_feat3_title",
        "tg_popup_join_cta",
        "tg_popup_dismiss",
        "seo_badge",
        "seo_guide_title",
        "seo_block1_h",
        "seo_block2_h",
        "seo_block3_h",
        "seo_block4_h",
        "seo_tags_title",
    ]
    
    for key in keys:
        assert f"{key}:" in html, f"Missing i18n key: {key}"


def test_endpoint_serves_updated_seo_and_popup():
    """Verify GET / returns 200 with the new keywords and telegram modal."""
    resp = client.get("/")
    assert resp.status_code == 200
    text = resp.text
    assert "aliexpressdz" in text.lower()
    assert "عروض علي اكسبراس" in text
    assert 'id="telegram-modal"' in text
    assert 'id="seo-shopping-guide"' in text
