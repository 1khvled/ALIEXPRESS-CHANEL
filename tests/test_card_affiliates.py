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

    # 3. Binance SEPA variant for France
    binance_fr = next(v for v in FR_VARIANTS if v["id"] == "fr_binance_sepa")
    cap_binance = binance_fr["caption"]
    assert BINANCE_CODE in cap_binance
    assert "SEPA" in cap_binance
    assert "Binance" in cap_binance
