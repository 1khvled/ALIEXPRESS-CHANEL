"""
Tests for Website Marketing Promo module (app/publisher/website_promo.py).
"""
import pytest
from app.publisher.website_promo import (
    POST_WEBSITE_PROMO_DZ,
    POST_WEBSITE_PROMO_FR,
    BUTTONS_DZ,
    BUTTONS_FR,
    WEBSITE_URL
)

def test_promo_captions_and_urls():
    assert "dealscout-green.vercel.app" in WEBSITE_URL
    assert len(POST_WEBSITE_PROMO_DZ) <= 1024, "Arabic caption must not exceed Telegram photo caption limit (1024)"
    assert len(POST_WEBSITE_PROMO_FR) <= 1024, "French caption must not exceed Telegram photo caption limit (1024)"
    
    assert "عروض الشتاء" in POST_WEBSITE_PROMO_DZ or "WOAE" in POST_WEBSITE_PROMO_DZ
    assert "BaridiMob" in POST_WEBSITE_PROMO_DZ
    assert "@Alilo07BOT" in POST_WEBSITE_PROMO_DZ
    
    assert "Winter Offers" in POST_WEBSITE_PROMO_FR
    assert "FRWO" in POST_WEBSITE_PROMO_FR

def test_buttons_structure():
    assert len(BUTTONS_DZ) >= 2
    assert any("dealscout-green.vercel.app" in btn["url"] for row in BUTTONS_DZ for btn in row)
    assert any("dealscout-green.vercel.app" in btn["url"] for row in BUTTONS_FR for btn in row)
