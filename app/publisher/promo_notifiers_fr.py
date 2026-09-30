"""
AliExpress France Promo Era Notifiers & Alerts
Publishes automated alerts to @francedealsdz:
1. Warm-up alert (1 day before start): Official French promo codes, PayPal discount pro-tip, cart prep.
2. Ending alert (1 day before end): Last chance coupon deadline, card lock / PayPal reservation tip.

Strictly deduplicated: Each alert is sent exactly once per promotion event.
"""
import os
import json
import httpx
from datetime import datetime, timezone, timedelta
from typing import Optional, Tuple, Dict, Any, List

from app.config.settings import settings
from app.aliexpress.promos import promo_tracker, PromoEvent
from app.utils.logger import logger

TARGET_FRANCE_CHANNEL = os.getenv("FRANCE_TARGET_CHANNEL_ID", "@francedealsdz")
FRANCE_STATE_FILE_PATH = os.path.join(settings.BASE_DIR, "storage", "state", "france_published_state.json")

def load_france_state() -> Dict:
    if os.path.exists(FRANCE_STATE_FILE_PATH):
        try:
            with open(FRANCE_STATE_FILE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading France state file: {e}")
    return {"published_post_keys": [], "sent_promo_notifiers": []}

def save_france_state(state: Dict):
    os.makedirs(os.path.dirname(FRANCE_STATE_FILE_PATH), exist_ok=True)
    try:
        tmp = FRANCE_STATE_FILE_PATH + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        if os.path.exists(FRANCE_STATE_FILE_PATH):
            os.replace(tmp, FRANCE_STATE_FILE_PATH)
        else:
            os.rename(tmp, FRANCE_STATE_FILE_PATH)
    except Exception as e:
        logger.error(f"Error saving France state file: {e}")

def is_france_notifier_already_sent(notifier_key: str) -> bool:
    state = load_france_state()
    sent = state.get("sent_promo_notifiers", [])
    return notifier_key in sent

def record_france_notifier_sent(notifier_key: str):
    state = load_france_state()
    if "sent_promo_notifiers" not in state:
        state["sent_promo_notifiers"] = []
    if notifier_key not in state["sent_promo_notifiers"]:
        state["sent_promo_notifiers"].append(notifier_key)
    save_france_state(state)

def build_france_promo_starting_alert(promo: PromoEvent, start_hour_paris: str = "09:00") -> Tuple[str, Dict[str, Any]]:
    """
    Builds authentic French warm-up / coupon announcement alert for @francedealsdz.
    """
    lines = [
        f"<blockquote>🚨 <b>Alerte Promo AliExpress France | Début des soldes demain dès {start_hour_paris} ! 🇫🇷</b></blockquote>",
        "",
        f"🎯 <b>Événement officiel :</b> Party Ready Sale & Choice Day France",
        f"⏰ <b>Lancement officiel :</b> Demain matin à <b>{start_hour_paris} (Heure de Paris)</b> / 08h00 (Heure DZ)",
        "",
        "🎟️ <b>Codes Promo Officiels France (actifs dès 09h00) :</b>",
        "• <b>-3€</b> dès 29€ d'achat : <code>CDFR03</code>",
        "• <b>-6€</b> dès 49€ d'achat : <code>CDFR06</code>",
        "• <b>-10€</b> dès 79€ d'achat : <code>CDFR10</code>",
        "• <b>-20€</b> dès 159€ d'achat : <code>FWFR20</code>",
        "• <b>-30€</b> dès 239€ d'achat : <code>FWFR30</code>",
        "• <b>-45€</b> dès 349€ d'achat : <code>FRLD45</code>",
        "• <b>-63€</b> dès 459€ d'achat : <code>FRLD63</code>",
        "",
        "💳 <b>Astuce Réduction PayPal :</b>",
        "En payant avec <b>PayPal</b>, bénéficiez de réductions cumulables allant jusqu'à <b>-33€</b> supplémentaires directement au paiement !",
        "",
        f"🛒 <b>Guide rapide avant le coup d'envoi de {start_hour_paris} :</b>",
        "1️⃣ <b>Préparez votre panier :</b> Ajoutez vos produits cibles dès maintenant pour éviter les ruptures de stock.",
        f"2️⃣ <b>Appliquez vos codes à {start_hour_paris} pile :</b> Les coupons les plus avantageux partent très vite.",
        "3️⃣ <b>Livraison rapide :</b> Priorisez les articles expédiés depuis les entrepôts européens/France pour une livraison en 3-7 jours.",
        "",
        "🔔 <i>Activez les notifications du canal pour ne rater aucun code ni baisse de prix !</i>",
        "━━━━━━━━━━━━━━━━━",
        "📢 <b>Canal officiel de bons plans :</b> @francedealsdz",
        "🔍 <i>#AliExpressFrance #CodesPromo #BonsPlans #AliExpress #ChoiceDay</i>"
    ]

    text = "\n".join(lines)
    reply_markup = {
        "inline_keyboard": [
            [
                {"text": "🛒 Accéder aux offres AliExpress France", "url": "https://s.click.aliexpress.com/e/_c3dQsooR"}
            ],
            [
                {"text": "📢 Rejoindre @francedealsdz", "url": "https://t.me/francedealsdz"}
            ]
        ]
    }
    return text, reply_markup

def build_france_promo_ending_alert(promo: PromoEvent, end_hour_paris: str = "08:59") -> Tuple[str, Dict[str, Any]]:
    """
    Builds the ending notifier post for France channel.
    """
    lines = [
        f"<blockquote>⚠️ <b>Dernières 24 Heures | Fin des soldes et codes promo demain à {end_hour_paris} ! 🇫🇷</b></blockquote>",
        "",
        "📌 <b>Événement en cours :</b> Party Ready Sale & Choice Day France",
        "",
        "❌ <b>Dernière chance pour utiliser vos coupons :</b>",
        "Tous les codes promo <code>CDFR03</code>, <code>CDFR06</code>, <code>CDFR10</code>, <code>FWFR20</code>, <code>FWFR30</code>, <code>FRLD45</code> et <code>FRLD63</code> cesseront de fonctionner dès la fin de l'événement.",
        "",
        "💳 <b>Astuce Pro Réservation de prix :</b>",
        "Vous pouvez valider votre commande dès maintenant en choisissant un moyen de paiement en attente ou temporairement bloqué pour figer le tarif réduit et finaliser le paiement plus tard !",
        "━━━━━━━━━━━━━━━━━",
        "📢 <b>Canal officiel de bons plans :</b> @francedealsdz",
        "🔍 <i>#AliExpressFrance #CodesPromo #BonsPlans #AliExpress</i>"
    ]

    text = "\n".join(lines)
    reply_markup = {
        "inline_keyboard": [
            [
                {"text": "🛒 Dernières affaires AliExpress France", "url": "https://s.click.aliexpress.com/e/_c3dQsooR"}
            ],
            [
                {"text": "📢 Rejoindre @francedealsdz", "url": "https://t.me/francedealsdz"}
            ]
        ]
    }
    return text, reply_markup

async def send_france_promo_alert(text: str, reply_markup: Dict[str, Any]) -> Tuple[bool, Optional[str], Optional[int]]:
    bot_token = settings.TELEGRAM_BOT_TOKEN
    if not bot_token:
        return False, "TELEGRAM_BOT_TOKEN missing", None

    api_url = f"https://api.telegram.org/bot{bot_token}"
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(
                f"{api_url}/sendMessage",
                json={
                    "chat_id": TARGET_FRANCE_CHANNEL,
                    "text": text,
                    "parse_mode": "HTML",
                    "reply_markup": reply_markup,
                    "disable_web_page_preview": True
                }
            )
            data = resp.json()
            if resp.status_code == 200 and data.get("ok"):
                return True, None, data.get("result", {}).get("message_id")
            return False, data.get("description", "Error"), None
    except Exception as e:
        logger.error(f"Error sending France promo alert: {e}")
        return False, str(e), None

async def check_and_auto_post_france_promo_notifiers(now: Optional[datetime] = None) -> List[Dict[str, Any]]:
    """
    Autonomous engine check called on schedule:
    1. Checks if upcoming promo starts within 6h to 36h: posts France Starting Alert.
    2. Checks if active promo ends within 6h to 36h: posts France Ending Alert.
    """
    if now is None:
        now = datetime.now(timezone.utc)

    results = []

    for promo in promo_tracker.calendar:
        # 1. Starting alert check (Warm-up ~24h before start)
        if now < promo.start_date:
            time_until_start = promo.start_date - now
            if timedelta(hours=6) <= time_until_start <= timedelta(hours=36):
                notifier_key = f"FR_START_ALERT_{promo.name}_{promo.start_date.strftime('%Y%m%d')}"
                if not is_france_notifier_already_sent(notifier_key):
                    logger.info(f"Triggering France Promo Starting Alert for {promo.name}")
                    text, markup = build_france_promo_starting_alert(promo)
                    success, err, msg_id = await send_france_promo_alert(text, markup)
                    if success:
                        record_france_notifier_sent(notifier_key)
                        results.append({
                            "type": "france_promo_starting_alert",
                            "promo": promo.name,
                            "message_id": msg_id,
                            "status": "published"
                        })
                    else:
                        logger.error(f"Failed to post France promo starting alert: {err}")

        # 2. Ending alert check (~24h before end)
        elif promo.start_date <= now <= promo.end_date:
            time_until_end = promo.end_date - now
            if timedelta(hours=6) <= time_until_end <= timedelta(hours=36):
                notifier_key = f"FR_END_ALERT_{promo.name}_{promo.end_date.strftime('%Y%m%d')}"
                if not is_france_notifier_already_sent(notifier_key):
                    logger.info(f"Triggering France Promo Ending Alert for {promo.name}")
                    text, markup = build_france_promo_ending_alert(promo)
                    success, err, msg_id = await send_france_promo_alert(text, markup)
                    if success:
                        record_france_notifier_sent(notifier_key)
                        results.append({
                            "type": "france_promo_ending_alert",
                            "promo": promo.name,
                            "message_id": msg_id,
                            "status": "published"
                        })
                    else:
                        logger.error(f"Failed to post France promo ending alert: {err}")

    return results
