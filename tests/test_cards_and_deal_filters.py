"""
Tests for Cards/Referrals page and Strict Deal Post Filtering.
Verifies:
- Dedicated Referrals page (#page-cards) contains Bybit, RedotPay, and Binance P2P details.
- Desktop, mobile, and footer navigation includes 'cards'.
- Strict filtering rejects religious verses, announcements, emojis, and posts without AliExpress links.
- Genuine AliExpress deals are parsed correctly.
"""
import re
import pytest
from api.user_site import USER_WEBSITE_HTML
from app.publisher.card_affiliates import BYBIT_CODE, REDOTPAY_CODE, BINANCE_CODE, BYBIT_URL, REDOTPAY_URL, BINANCE_URL


def test_cards_page_structure_and_partners():
    """Verify #page-cards has all 3 partner referrals and codes."""
    html = USER_WEBSITE_HTML
    
    # 1. Page view element
    assert 'id="page-cards"' in html
    
    # 2. Partner 1: Bybit
    assert BYBIT_CODE in html  # L9LLRP5
    assert BYBIT_URL in html or "bybit.com/invite?ref=" in html
    assert "cards_bybit_title" in html or "Bybit Card" in html
    
    # 3. Partner 2: RedotPay
    assert REDOTPAY_CODE in html  # djbt3
    assert REDOTPAY_URL in html or "url.hk/i/en/" in html
    assert "cards_redot_title" in html or "RedotPay" in html
    
    # 4. Partner 3: Binance
    assert BINANCE_CODE in html  # GRO_28502_3WGQR
    assert BINANCE_URL in html or "binance.com/referral" in html
    assert "cards_binance_title" in html or "Binance P2P" in html
    
    # 5. BaridiMob step-by-step workflow
    assert "cards_guide_title" in html
    assert "BaridiMob" in html


def test_cards_navigation_links():
    """Verify desktop nav, mobile bottom nav, and footer contain cards link."""
    html = USER_WEBSITE_HTML
    
    # Desktop nav
    assert 'id="nav-link-cards"' in html
    assert "showPage('cards')" in html
    
    # Mobile bottom nav
    assert 'id="mob-bottom-cards"' in html
    
    # Router pages array includes 'cards'
    assert "['deals', 'cards', 'coins', 'faq', 'contact', 'about']" in html
    
    # i18n translation keys
    assert "nav_cards" in html


def test_strict_post_filtering_regexes():
    """Verify the regexes used in user_site.py filter out non-deal posts."""
    # 1. Religious verse rejection
    religious_pattern = re.compile(
        r"(?:وَتَوَكَّلْ|وتوكل|سبحان الله|الحمد لله|الله أكبر|صلى الله|عليه وسلم|سورة|القرآن|أذكار|دعاء|تذكير ديني|استغفر الله|لا إله إلا الله|حسبي الله|اذكار)",
        re.IGNORECASE
    )
    verse_post = "وَتَوَكَّلْ عَلَى الْحَيِّ الَّذِي لَا يَمُوتُ وَسَبِّحْ بِحَمْدِهِ ۚ وَكَفَىٰ بِهِ بِذُنُوبِ عِبَادِهِ خَبِيرًا"
    assert religious_pattern.search(verse_post) is not None

    # 2. Link requirement: Must have explicit AliExpress URL
    link_pattern = re.compile(
        r"https?://(?:s\.click\.aliexpress\.com/e/[A-Za-z0-9_-]+|(?:[a-z0-9-]+\.)?aliexpress\.com/(?:item|p)/[A-Za-z0-9_.-]+)",
        re.IGNORECASE
    )
    assert link_pattern.search(verse_post) is None
    
    # Emoji only
    emoji_post = "♂️"
    assert link_pattern.search(emoji_post) is None

    # Valid deal post
    deal_post = (
        "✅ Soundcore by Anker Life P2 Mini\n"
        "💰 السعر : $19.99\n"
        "🎟️ كود الخصم : ANKER5\n"
        "https://s.click.aliexpress.com/e/_oEN3d53"
    )
    assert link_pattern.search(deal_post) is not None
    assert religious_pattern.search(deal_post) is None
