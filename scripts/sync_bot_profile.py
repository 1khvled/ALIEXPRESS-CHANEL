"""
Utility to sync and harden Telegram Bot profile, descriptions, and commands.
Eliminates localized spam/malicious descriptions across all language codes.
"""
import sys
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import asyncio
from typing import List
import httpx

try:
    from app.utils.network import enforce_ipv4
    enforce_ipv4()
except Exception:
    pass

from app.config.settings import settings
from app.utils.logger import logger

DEFAULT_AR_NAME = "بوت تخفيض العملات علي اكسبرس 🇩🇿 DealScout"
DEFAULT_AR_SHORT = "🇩🇿 البوت الجزائري الأول لتفعيل أقصى تخفيض بالعملات (Coins) وحساب أسعار AliExpress بالدينار 🪙"
DEFAULT_AR_DESC = """🇩🇿 أهلاً بك في بوت تخفيض العملات علي اكسبرس (DealScout DZ)!

✨ مميزات البوت:
🪙 تحويل وتفعيل أقصى تخفيض بالعملات (Coins Discount) لأي منتج
📊 استخراج روابط التخفيض المباشرة وروابط الحزم (Bundle Deals)
💵 حساب السعر بالدينار الجزائري (DZD) حسب سعر السوق الموازي (Square)
🎟️ كشف وتطبيق أفضل الكوبونات الحصرية وقسائم المتاجر

أرسل أي رابط منتج من تطبيق AliExpress وسيقوم البوت بتجهيز التخفيض فوراً! 🚀"""

FR_NAME = "DealScout Bot 🇩🇿🇫🇷 Réduction Coins"
FR_SHORT = "🤖 Bot officiel DealScout pour maximiser vos réductions Coins sur AliExpress ! Envoyez n'importe quel lien 🪙"
FR_DESC = """🇩🇿🇫🇷 Bienvenue sur le bot officiel DealScout !

✨ Fonctionnalités du bot :
🪙 Maximiser et activer la réduction pièces (Coins jusqu'à -70%)
📊 Liens directs Super Deals et offres groupées (Bundle Deals)
🎟️ Détection automatique des meilleurs codes promo et coupons vendeurs

Envoyez simplement le lien d'un article AliExpress et le bot génère le lien optimisé immédiatement ! 🚀"""

EN_NAME = "DealScout Bot 🇩🇿 Coins Discount"
EN_SHORT = "🤖 Official DealScout bot: maximize your AliExpress Coins discounts! Send any product link 🪙"
EN_DESC = """🇩🇿 Welcome to the official DealScout Bot!

✨ Bot Features:
🪙 Activate maximum Coins discount (up to 70% off) for any product
📊 Extract direct discount and Bundle Deals links
🎟️ Automatic detection of verified promo codes and seller vouchers

Simply send any AliExpress product link and get your optimized deal link instantly! 🚀"""

KNOWN_LANGS: List[str] = [
    "en", "fr", "es", "ru", "de", "uk", "it", "pt", "tr", "zh", "ja", "ko", "fa", "pl", "nl", "hi", "id"
]

def sync_telegram_bot_profile(token: str = None) -> bool:
    bot_token = token or settings.TELEGRAM_BOT_TOKEN
    if not bot_token:
        logger.error("No TELEGRAM_BOT_TOKEN found!")
        return False

    api_base = f"https://api.telegram.org/bot{bot_token}"
    with httpx.Client(timeout=12.0) as client:
        # 1. Clear spam on all secondary language codes
        for lang in KNOWN_LANGS:
            if lang not in ["fr", "en"]:
                client.post(f"{api_base}/setMyShortDescription", json={"short_description": "", "language_code": lang})
                client.post(f"{api_base}/setMyDescription", json={"description": "", "language_code": lang})
                client.post(f"{api_base}/setMyName", json={"name": "", "language_code": lang})

        # 2. Set Default (Arabic / Main)
        client.post(f"{api_base}/setMyName", json={"name": DEFAULT_AR_NAME, "language_code": ""})
        client.post(f"{api_base}/setMyShortDescription", json={"short_description": DEFAULT_AR_SHORT, "language_code": ""})
        client.post(f"{api_base}/setMyDescription", json={"description": DEFAULT_AR_DESC, "language_code": ""})

        # 3. Set French
        client.post(f"{api_base}/setMyName", json={"name": FR_NAME, "language_code": "fr"})
        client.post(f"{api_base}/setMyShortDescription", json={"short_description": FR_SHORT, "language_code": "fr"})
        client.post(f"{api_base}/setMyDescription", json={"description": FR_DESC, "language_code": "fr"})

        # 4. Set English
        client.post(f"{api_base}/setMyName", json={"name": EN_NAME, "language_code": "en"})
        client.post(f"{api_base}/setMyShortDescription", json={"short_description": EN_SHORT, "language_code": "en"})
        client.post(f"{api_base}/setMyDescription", json={"description": EN_DESC, "language_code": "en"})

        logger.info("Successfully synchronized and hardened Telegram bot profile descriptions across all languages.")
        return True

if __name__ == "__main__":
    success = sync_telegram_bot_profile()
    print("Bot profile sync finished with status:", success)
