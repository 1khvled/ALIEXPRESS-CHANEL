"""
Unit tests for Mobile, Tablet (iPad), Direct Telegram Access, and Square Calculator.
"""
import pytest
from api.user_site import USER_WEBSITE_HTML


def test_roulette_hidden_on_phones():
    """Verify that floating deal roulette is hidden on mobile phone viewports."""
    assert 'id="fab-roulette"' in USER_WEBSITE_HTML
    # Must have hidden md:flex so phones don't have floating button blocking deals
    assert 'class="hidden md:flex' in USER_WEBSITE_HTML
    # Roulette modal button must not have fake XP text
    assert 'id="roulette-spin-btn"' in USER_WEBSITE_HTML
    assert '+50 XP' not in USER_WEBSITE_HTML


def test_tablet_and_desktop_navbar_support():
    """Verify that iPads and tablets (768px-1024px) have desktop nav enabled."""
    # Desktop nav must be hidden md:flex (visible on iPads >= 768px), not hidden lg:flex
    assert 'class="hidden md:flex items-center gap-1 text-xs font-semibold"' in USER_WEBSITE_HTML


def test_direct_telegram_channel_links():
    """Verify prominent direct access to Telegram channel across the website."""
    # 1. Top bar telegram link
    assert 'id="top-telegram-link"' in USER_WEBSITE_HTML
    assert 'https://t.me/DzAliexpress0' in USER_WEBSITE_HTML
    
    # 2. Main sticky header button with visible label
    assert 'id="btn-telegram-join"' in USER_WEBSITE_HTML
    assert 'btn_join_channel' in USER_WEBSITE_HTML

    # 3. Direct access Telegram channel banner on deals page
    assert 'id="channel-telegram-banner"' in USER_WEBSITE_HTML
    assert 'id="channel-banner-btn"' in USER_WEBSITE_HTML
    assert 'id="channel-banner-name"' in USER_WEBSITE_HTML

    # 4. Mobile bottom navigation bar has direct telegram tab
    assert 'id="mob-bottom-tg"' in USER_WEBSITE_HTML
    assert 'nav_telegram' in USER_WEBSITE_HTML


def test_square_calculator_replaces_levels():
    """Verify that fake gaming levels/XP are replaced by useful Square Dinar Calculator."""
    # No fake levels or XP functions
    assert 'function addXP' not in USER_WEBSITE_HTML
    assert 'مستوى المتسوق' not in USER_WEBSITE_HTML
    assert 'صياد العروض (المستوى 2)' not in USER_WEBSITE_HTML
    assert 'قناص التخفيضات' not in USER_WEBSITE_HTML

    # Useful Square Dinar Calculator components exist
    assert 'id="calc-foreign-input"' in USER_WEBSITE_HTML
    assert 'id="calc-dzd-input"' in USER_WEBSITE_HTML
    assert 'id="calc-usdt-rate"' in USER_WEBSITE_HTML
    assert 'id="calc-bybit-total"' in USER_WEBSITE_HTML
    assert 'id="calc-redot-total"' in USER_WEBSITE_HTML
    assert 'onCalcForeignChange' in USER_WEBSITE_HTML
    assert 'onCalcDzdChange' in USER_WEBSITE_HTML


def test_responsive_grid_breakpoints():
    """Verify that deals grid supports phones, iPads, laptops, and ultra-wide screens."""
    assert 'grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4' in USER_WEBSITE_HTML
