import pytest
from app.publisher.card_affiliates import (
    DZ_VARIANTS,
    FR_VARIANTS,
    BYBIT_CODE,
    REDOTPAY_CODE,
    BINANCE_CODE,
    is_card_affiliate_eligible_dz,
    is_card_affiliate_eligible_fr,
    record_card_affiliate_published_dz,
    record_card_affiliate_published_fr
)

def test_algerian_marketing_angles_and_codes():
    # 1. Bybit Free Card variant for Algeria
    bybit_dz = next(v for v in DZ_VARIANTS if v["id"] == "dz_bybit_card_free")
    cap_bybit = bybit_dz["caption"]
    assert "مجانية 100%" in cap_bybit or "مجانية تماماً" in cap_bybit
    assert "0 دج مصاريف" in cap_bybit or "بدون أي اشتراك" in cap_bybit
    assert BYBIT_CODE in cap_bybit
    assert "BaridiMob" in cap_bybit
    assert "AliExpress" in cap_bybit

    # 2. RedotPay Visa variant for Algeria
    redotpay_dz = next(v for v in DZ_VARIANTS if v["id"] == "dz_redotpay_visa")
    cap_redot = redotpay_dz["caption"]
    assert REDOTPAY_CODE in cap_redot
    assert "5$" in cap_redot
    assert "AliExpress" in cap_redot

    # 3. Binance P2P BaridiMob variant for Algeria
    binance_dz = next(v for v in DZ_VARIANTS if v["id"] == "dz_binance_p2p_guide")
    cap_binance = binance_dz["caption"]
    assert BINANCE_CODE in cap_binance
    assert "BaridiMob" in cap_binance
    assert "Binance" in cap_binance


def test_french_marketing_angles_and_codes():
    # 1. Bybit Free Card & Cashback variant for France/Europe
    bybit_fr = next(v for v in FR_VARIANTS if v["id"] == "fr_bybit_card_cashback")
    cap_bybit = bybit_fr["caption"]
    assert "100% Gratuite" in cap_bybit or "100% GRATUITE" in cap_bybit
    assert "0€" in cap_bybit
    assert "Cashback" in cap_bybit
    assert BYBIT_CODE in cap_bybit
    assert "AliExpress" in cap_bybit

    # 2. RedotPay Crypto Visa variant for France
    redotpay_fr = next(v for v in FR_VARIANTS if v["id"] == "fr_redotpay_visa")
    cap_redot = redotpay_fr["caption"]
    assert REDOTPAY_CODE in cap_redot
    assert "5$" in cap_redot
    assert "AliExpress" in cap_redot

    # 3. Binance Crypto + Stocks + P2P + Secured variant for France
    binance_fr = next(v for v in FR_VARIANTS if v["id"] == "fr_binance_invest_crypto_stocks")
    cap_binance = binance_fr["caption"]
    assert BINANCE_CODE in cap_binance
    assert "Actions" in cap_binance or "Stocks" in cap_binance
    assert "P2P" in cap_binance
    assert "Sécurité" in cap_binance or "SAFU" in cap_binance
    assert "SEPA" in cap_binance
    assert "Binance" in cap_binance

@pytest.mark.asyncio
async def test_card_affiliate_strict_24h_cooldown(tmp_path):
    from unittest.mock import patch, AsyncMock
    import time

    test_dz_file = tmp_path / "published_state.json"
    with patch("app.publisher.card_affiliates.STATE_FILE_DZ", test_dz_file), \
         patch("app.publisher.card_affiliates.has_recent_card_post_in_channel", new=AsyncMock(return_value=False)):
        # 1. Fresh state is eligible
        eligible, _ = await is_card_affiliate_eligible_dz(min_hours=24.0)
        assert eligible is True

        # 2. Record publish
        record_card_affiliate_published_dz(variant_idx=0)

        # 3. Immediately after (within 24h), must be strictly locked
        eligible2, reason2 = await is_card_affiliate_eligible_dz(min_hours=24.0)
        assert eligible2 is False
        assert "Anti-duplicate lock" in reason2 or "required" in reason2
