"""
Website Marketing & Launch Announcement Module
Publishes promotional, high-converting announcements for https://dealscout-green.vercel.app/
to Telegram channels (@DzAliexpress0 and @francedealsdz).
"""
import os
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple, Dict, Any, List
import httpx

from app.config.settings import settings
from app.utils.logger import logger, record_system_log
from app.utils.network import enforce_ipv4

WEBSITE_URL = "https://dealscout-green.vercel.app/"

# --- ARABIC CAMPAIGN: For @DzAliexpress0 (Algeria Audience) ---
POST_WEBSITE_PROMO_DZ = """<blockquote>🌐 <b>إطـلاق موقع DealScout DZ لصفقات AliExpress بالدينار! 🇩🇿⚡</b></blockquote>

لكل متتبعي القناة.. طورنا لكم منصة <b>DealScout DZ</b> لاقتناص الصيدات بدقة واحترافية:

✨ <b>أهم مزايا المنصة:</b>
▫️ 💰 <b>أسعار بالدينار (DZD):</b> حساب فوري بسعر السكوار الحقيقي (SquareAlgérie).
▫️ ❄️ <b>أكواد عروض الشتاء:</b> نسخ مباشر لكل الكوبونات (<code>WOAE06</code> / <code>WOAE12</code> / <code>WOAE23</code> / <code>WOAE35</code>).
▫️ 📱 <b>تصفح بالأقسام:</b> هواتف، قيمنق، سماعات، شواحن وتجميعات عروض.
▫️ 💳 <b>دليل الشراء بـ BaridiMob:</b> بطاقات Bybit و RedotPay عبر Binance P2P.
▫️ 🪙 <b>دمج بوت العملات:</b> خصم عملات يصل لـ 60% مع @Alilo07BOT.

📲 <i>الموقع خفيف جداً ويدعم التثبيت على شاشة هاتفك (PWA)!</i>

🔗 <b>تصفح الموقع الآن ⤵️</b>
https://dealscout-green.vercel.app/
━━━━━━━━━━━━━━━━━
📢 <b>قناة الصفقات:</b> @DzAliexpress0"""

BUTTONS_DZ = [
    [{"text": "🌐 تصفح موقع الصفقات الآن", "url": "https://dealscout-green.vercel.app/"}],
    [{"text": "💳 دليل بطاقات الشراء وبريدي موب", "url": "https://dealscout-green.vercel.app/cards"}],
    [{"text": "🪙 بوت تخفيض العملات (@Alilo07BOT)", "url": "https://t.me/Alilo07BOT"}]
]

# --- FRENCH CAMPAIGN: For @francedealsdz (France & Diaspora Audience) ---
POST_WEBSITE_PROMO_FR = """<blockquote>🌐 <b>Lancement de notre Plateforme Web DealScout DZ ! 🇫🇷⚡</b></blockquote>

Retrouvez tous les meilleurs bons plans et codes promos AliExpress sur une plateforme rapide et moderne :

✨ <b>Fonctionnalités clés :</b>
▫️ 💶 <b>Double devise :</b> Prix en Euros (€) et Dinars (DZD).
▫️ 🎟️ <b>Codes Promo Officiels :</b> Tous les coupons Winter Offers (<code>FRWO06</code>, <code>FRWO12</code>, <code>FRWO23</code>, <code>FRWO35</code>) en 1 clic.
▫️ 📦 <b>Rayons thématiques :</b> Smartphones, PC Gaming, Audio et High-Tech.
▫️ 💳 <b>Guide Cartes Bybit :</b> 0€ frais, 0 abonnement et cashback.
▫️ 🪙 <b>Remise Pièces :</b> Liens optimisés avec le bot @Alilo07BOT.

🔗 <b>Accédez au site dès maintenant ⤵️</b>
https://dealscout-green.vercel.app/
━━━━━━━━━━━━━━━━━
📢 <b>Canal France :</b> @francedealsdz"""

BUTTONS_FR = [
    [{"text": "🌐 Découvrir le site DealScout DZ", "url": "https://dealscout-green.vercel.app/"}],
    [{"text": "💳 Guide Cartes & Recharges", "url": "https://dealscout-green.vercel.app/cards"}]
]


async def publish_website_promo(channel: str = "both") -> Dict[str, Any]:
    """
    Publishes the website marketing announcement to Telegram channels.
    channel: 'dz' (Algeria), 'fr' (France), or 'both'.
    """
    enforce_ipv4()
    results = {}

    bot_token = (
        getattr(settings, "TELEGRAM_BOT_TOKEN", None)
        or getattr(settings, "ADMIN_BOT_TOKEN", None)
        or os.getenv("TELEGRAM_BOT_TOKEN", "")
    )
    if not bot_token:
        return {"error": "TELEGRAM_BOT_TOKEN is not configured"}

    api_url = f"https://api.telegram.org/bot{bot_token}"
    logo_path = settings.BASE_DIR / "assets" / "logo.png"

    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. Publish to Algerian Channel (@DzAliexpress0)
        if channel in ("dz", "both"):
            target_dz = os.getenv("TARGET_CHANNEL_ID", "@DzAliexpress0")
            reply_markup_dz = json.dumps({"inline_keyboard": BUTTONS_DZ})
            try:
                if logo_path.exists():
                    with open(logo_path, "rb") as f:
                        data = {
                            "chat_id": target_dz,
                            "caption": POST_WEBSITE_PROMO_DZ,
                            "parse_mode": "HTML",
                            "reply_markup": reply_markup_dz
                        }
                        resp = await client.post(f"{api_url}/sendPhoto", data=data, files={"photo": f})
                else:
                    data = {
                        "chat_id": target_dz,
                        "text": POST_WEBSITE_PROMO_DZ,
                        "parse_mode": "HTML",
                        "reply_markup": reply_markup_dz,
                        "disable_web_page_preview": False
                    }
                    resp = await client.post(f"{api_url}/sendMessage", data=data)

                res_json = resp.json()
                if resp.status_code == 200 and res_json.get("ok"):
                    msg_id = res_json["result"]["message_id"]
                    results["dz"] = {
                        "status": "success",
                        "channel": target_dz,
                        "message_id": msg_id,
                        "link": f"https://t.me/{target_dz.lstrip('@')}/{msg_id}"
                    }
                    logger.info(f"Published website promo to {target_dz} (msg_id: {msg_id})")
                else:
                    results["dz"] = {"status": "error", "response": res_json}
            except Exception as e:
                results["dz"] = {"status": "error", "error": str(e)}

        # 2. Publish to French Channel (@francedealsdz)
        if channel in ("fr", "both"):
            target_fr = os.getenv("FRANCE_TARGET_CHANNEL_ID", "@francedealsdz")
            bot_token_fr = os.getenv("FRANCE_BOT_TOKEN") or bot_token
            api_url_fr = f"https://api.telegram.org/bot{bot_token_fr}"
            reply_markup_fr = json.dumps({"inline_keyboard": BUTTONS_FR})
            try:
                if logo_path.exists():
                    with open(logo_path, "rb") as f:
                        data = {
                            "chat_id": target_fr,
                            "caption": POST_WEBSITE_PROMO_FR,
                            "parse_mode": "HTML",
                            "reply_markup": reply_markup_fr
                        }
                        resp = await client.post(f"{api_url_fr}/sendPhoto", data=data, files={"photo": f})
                else:
                    data = {
                        "chat_id": target_fr,
                        "text": POST_WEBSITE_PROMO_FR,
                        "parse_mode": "HTML",
                        "reply_markup": reply_markup_fr,
                        "disable_web_page_preview": False
                    }
                    resp = await client.post(f"{api_url_fr}/sendMessage", data=data)

                res_json = resp.json()
                if resp.status_code == 200 and res_json.get("ok"):
                    msg_id = res_json["result"]["message_id"]
                    results["fr"] = {
                        "status": "success",
                        "channel": target_fr,
                        "message_id": msg_id,
                        "link": f"https://t.me/{target_fr.lstrip('@')}/{msg_id}"
                    }
                    logger.info(f"Published website promo to {target_fr} (msg_id: {msg_id})")
                else:
                    results["fr"] = {"status": "error", "response": res_json}
            except Exception as e:
                results["fr"] = {"status": "error", "error": str(e)}

    return results
