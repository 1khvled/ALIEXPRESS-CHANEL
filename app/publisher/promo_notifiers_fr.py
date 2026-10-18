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
from app.publisher.promo_notifiers import get_event_ended_image_path, get_event_started_image_path
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
    Includes booking tutorial with eligible high-value product to bind codes.
    """
    coupons = promo.coupon_tiers_fr if promo.coupon_tiers_fr else []
    coupon_lines = []
    for c in coupons:
        t = c.get("tier", "").strip()
        code = c.get("code", "").strip()
        if t and code:
            coupon_lines.append(f"🎟️ <b>Code {t} :</b> <code>{code}</code>")

    if coupon_lines:
        lines = [
            f"🚨 <b>CODES PROMO | {promo.name_fr or promo.name} ! 🇫🇷</b>",
            f"Du <b>{promo.start_date.strftime('%d')} au {promo.end_date.strftime('%d %B %Y')}</b> 🛍️",
            f"⏰ Actifs dès demain à <b>{start_hour_paris} (Paris) / 08h00 (DZ)</b>",
            "",
            *coupon_lines,
            "",
            "💳 <b>Astuce PayPal :</b> Jusqu'à <b>-33€ supplémentaires</b> au paiement !",
            "",
            "⭕️ <b>Tutoriel : Verrouiller tous les codes sur votre compte :</b>",
            "⚠️ <b>Commencez par les gros codes (-60€, -45€...)</b> puis appliquez les suivants pour les lier à votre compte avant rupture de stock !",
            "",
            "🔹 <b>Appliquez tous les codes sur ce produit (tous les seuils passent) ⤵️</b>",
            "https://s.click.aliexpress.com/e/_c2QPADRL",
            "",
            "🪙 Bot réduction pièces : @Alilo07BOT",
            "━━━━━━━━━━━━━━━━━",
            "📢 <b>Canal :</b> @francedealsdz"
        ]
    else:
        lines = [
            f"🚨 <b>PROCHAINEMENT | {promo.name_fr or promo.name} ! 🇫🇷</b>",
            f"Du <b>{promo.start_date.strftime('%d')} au {promo.end_date.strftime('%d %B %Y')}</b> 🛍️",
            f"⏰ Lancement prévu dès demain à <b>{start_hour_paris} (Paris) / 08h00 (DZ)</b>",
            "",
            "💡 <b>Offres & Réductions :</b>",
            "Remises immédiates avec pièces AliExpress 🪙 et coupons vendeurs dédiés !",
            "Activez vos pièces et préparez vos paniers dès aujourd'hui.",
            "",
            "🪙 Bot réduction pièces : @Alilo07BOT",
            "━━━━━━━━━━━━━━━━━",
            "📢 <b>Canal :</b> @francedealsdz"
        ]

    text = "\n".join(lines)
    reply_markup = {}
    return text, reply_markup

def build_france_promo_launch_alert(promo: PromoEvent, start_hour_paris: str = "09:00") -> Tuple[str, Dict[str, Any]]:
    """Builds the launch alert when promo officially starts for France shoppers."""
    coupons = promo.coupon_tiers_fr if promo.coupon_tiers_fr else []
    coupon_lines = []
    for c in coupons:
        t = c.get("tier", "").strip()
        code = c.get("code", "").strip()
        if t and code:
            coupon_lines.append(f"🎟️ <b>Code {t} :</b> <code>{code}</code>")

    if coupon_lines:
        lines = [
            f"🚀 <b>C'EST PARTI ! Lancement officiel : {promo.name_fr or promo.name} ! 🇫🇷🛍️</b>",
            f"⏰ <b>Les codes promo viennent d'être activés dès maintenant ({start_hour_paris}) :</b>",
            "Appliquez-les immédiatement sur vos commandes avant épuisement des quotas !",
            "",
            *coupon_lines,
            "",
            "💳 <b>Rappel PayPal :</b> Réduction immédiate supplémentaire possible au paiement !",
            "",
            "🔹 <b>Lien rapide vers l'événement ⤵️</b>",
            "https://s.click.aliexpress.com/e/_c2QPADRL",
            "",
            "🪙 Bot réduction pièces : @Alilo07BOT",
            "━━━━━━━━━━━━━━━━━",
            "📢 <b>Canal :</b> @francedealsdz"
        ]
    else:
        lines = [
            f"🚀 <b>C'EST PARTI ! Lancement officiel : {promo.name_fr or promo.name} ! 🇫🇷🛍️</b>",
            f"⏰ <b>Les offres sont actives dès maintenant ({start_hour_paris}) :</b>",
            "Profitez des remises pièces et des coupons vendeurs disponibles sur les sélections !",
            "",
            "🔹 <b>Lien rapide vers l'événement ⤵️</b>",
            "https://s.click.aliexpress.com/e/_c2QPADRL",
            "",
            "🪙 Bot réduction pièces : @Alilo07BOT",
            "━━━━━━━━━━━━━━━━━",
            "📢 <b>Canal :</b> @francedealsdz"
        ]
    return "\n".join(lines), {}

def build_france_promo_ending_alert(promo: PromoEvent, end_hour_paris: str = "08:59") -> Tuple[str, Dict[str, Any]]:
    """
    Builds the ending notifier post for France channel.
    """
    lines = [
        f"<blockquote>⚠️ <b>Dernières 24 Heures | Fin des soldes et codes promo demain à {end_hour_paris} ! 🇫🇷</b></blockquote>",
        "",
        f"📌 <b>Événement en cours :</b> {promo.name_fr or promo.name}",
        "",
        "❌ <b>Dernière chance pour utiliser vos coupons :</b>",
        "Tous les codes promo cesseront de fonctionner dès la fin de l'événement.",
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
                {"text": "🛒 Dernières affaires AliExpress France", "url": "https://s.click.aliexpress.com/e/_c2QPADRL"}
            ],
            [
                {"text": "📢 Rejoindre @francedealsdz", "url": "https://t.me/francedealsdz"}
            ]
        ]
    }
    return text, reply_markup

def build_france_sunday_alert(promo: Optional[PromoEvent] = None) -> Tuple[str, Dict[str, Any]]:
    """
    Builds the high-converting Sunday Flash promo notification for @francedealsdz:
    - Announces the 24h flash Sunday event
    - Lists active SUNFR promo codes
    - References top verified live deals (Realme GT 7T, Realme 16 5G)
    - PayPal extra discount reminder
    - Inline buttons for AliExpress France event page and bot
    """
    coupons = (promo.coupon_tiers_fr if promo and promo.coupon_tiers_fr else [
        {"tier": "-20€ dès 199€", "code": "SUNFR20"},
        {"tier": "-30€ dès 280€", "code": "SUNFR30"}
    ])
    coupon_lines = []
    for c in coupons:
        t = c.get("tier", "").strip()
        code = c.get("code", "").strip()
        if t and code:
            coupon_lines.append(f"🎟️ <b>Code {t} :</b> <code>{code}</code>")

    lines = [
        "⚡️ <b>OFFRES DU DIMANCHE | CODES PROMO FLASH 🇫🇷</b>",
        "Du <b>Dimanche uniquement (jusqu'à 23h59)</b> 🛍️",
        "",
        "⏰ <b>Codes promo exclusifs pour la France :</b>",
        *coupon_lines,
        "",
        "📱 <b>Bons plans vérifiés éligibles aujourd'hui :</b>",
        "• <b>Realme GT 7T (12/256GB)</b> à <b>283,00€</b> (avec <code>SUNFR30</code>) ➡️ <a href=\"https://t.me/francedealsdz/179\">Voir l'offre</a>",
        "• <b>Realme 16 5G (8/256GB)</b> à <b>258,69€</b> (avec <code>SUNFR20</code>) ➡️ <a href=\"https://t.me/francedealsdz/180\">Voir l'offre</a>",
        "",
        "💳 <b>Astuce PayPal :</b> Remise supplémentaire possible au paiement !",
        "⚠️ <i>Codes valables sur les produits expédiés vers la France, dans la limite des quotas.</i>",
        "━━━━━━━━━━━━━━━━━",
        "📢 <b>Canal :</b> @francedealsdz",
        "🔍 <i>#AliExpressFrance #CodesPromo #SuperSunday #BonsPlans</i>"
    ]
    reply_markup = {
        "inline_keyboard": [
            [
                {"text": "🛍️ Accéder aux Offres AliExpress France", "url": "https://s.click.aliexpress.com/e/_c2QPADRL"}
            ],
            [
                {"text": "🪙 Bot Réduction Pièces", "url": "https://t.me/Alilo07BOT"},
                {"text": "📢 Rejoindre @francedealsdz", "url": "https://t.me/francedealsdz"}
            ]
        ]
    }
    return "\n".join(lines), reply_markup


async def send_france_promo_alert(
    text: str,
    reply_markup: Optional[Dict[str, Any]] = None,
    coupon_list: Optional[List[Dict[str, str]]] = None,
    promo_title: str = "Choice Day France",
    image_path: Optional[str] = None
) -> Tuple[bool, Optional[str], Optional[int]]:
    from app.media.renderer import media_renderer
    bot_token = settings.TELEGRAM_BOT_TOKEN or getattr(settings, "ADMIN_BOT_TOKEN", None) or os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("ADMIN_BOT_TOKEN")
    if not bot_token:
        return False, "TELEGRAM_BOT_TOKEN missing", None

    api_url = f"https://api.telegram.org/bot{bot_token}"
    card_path = image_path

    # If no explicit image_path provided, resolve dynamically based on content
    if not card_path:
        if any(kw in text for kw in ["Fin des soldes", "Dernières 24 Heures", "Cesseront de fonctionner", "Fin de l'événement"]):
            card_path = get_event_ended_image_path()
        elif coupon_list:
            card_path = media_renderer.render_coupon_bulletin_card(
                coupon_list,
                promo_title=promo_title,
                channel_handle="@francedealsdz",
                is_french=True
            )
        elif any(kw in text for kw in ["Lancement officiel", "C'EST PARTI", "PROCHAINEMENT", "CODES PROMO", "OFFRES DU DIMANCHE"]):
            card_path = get_event_started_image_path()

    try:
        async with httpx.AsyncClient(timeout=25.0) as client:
            if card_path and os.path.exists(card_path) and len(text) <= 1024:
                data_payload = {
                    "chat_id": TARGET_FRANCE_CHANNEL,
                    "caption": text,
                    "parse_mode": "HTML"
                }
                if reply_markup:
                    data_payload["reply_markup"] = json.dumps(reply_markup)
                with open(card_path, "rb") as pf:
                    resp = await client.post(
                        f"{api_url}/sendPhoto",
                        data=data_payload,
                        files={"photo": ("promo_alert_fr.png", pf, "image/png")}
                    )
            else:
                json_payload = {
                    "chat_id": TARGET_FRANCE_CHANNEL,
                    "text": text,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": True
                }
                if reply_markup:
                    json_payload["reply_markup"] = reply_markup
                resp = await client.post(
                    f"{api_url}/sendMessage",
                    json=json_payload
                )
            data = resp.json()
            if resp.status_code == 200 and data.get("ok"):
                msg_id = data.get("result", {}).get("message_id")
                if msg_id:
                    try:
                        await client.post(
                            f"{api_url}/pinChatMessage",
                            json={"chat_id": TARGET_FRANCE_CHANNEL, "message_id": msg_id, "disable_notification": False}
                        )
                    except Exception as pe:
                        logger.warning(f"Failed to auto-pin France message {msg_id}: {pe}")
                return True, None, msg_id
            return False, data.get("description", "Error"), None
    except Exception as e:
        logger.error(f"Error sending France promo alert: {e}")
        return False, str(e), None


async def check_and_auto_post_france_promo_notifiers(now: Optional[datetime] = None) -> List[Dict[str, Any]]:
    """
    Autonomous engine check called on schedule:
    1. Checks if upcoming promo starts within 6h to 36h: posts France Starting Alert.
    2. Checks if active promo ends within 6h to 36h: posts France Ending Alert.
    3. Checks weekly Super Sunday flash promotions: posts France Sunday Flash Alert.
    4. Guarantees active French coupon bulletin is pinned.
    5. Automatically unpins expired bulletins.
    """
    if now is None:
        now = datetime.now(timezone.utc)

    results = []

    # 1. Weekly Sunday Flash Alert check (Super Sunday / Offres du Dimanche)
    active_fr_promo = getattr(promo_tracker, "get_active_france_promo", promo_tracker.get_active_promo)(now)
    if active_fr_promo and getattr(active_fr_promo, "is_sunday_flash", False):
        sunday_key = f"FR_SUNDAY_ALERT_{now.strftime('%Y%m%d')}"
        if not is_france_notifier_already_sent(sunday_key):
            logger.info("Triggering France Promo Sunday Flash Alert (@francedealsdz)")
            text, markup = build_france_sunday_alert(active_fr_promo)
            success, err, msg_id = await send_france_promo_alert(
                text,
                markup,
                coupon_list=active_fr_promo.coupon_tiers_fr,
                promo_title="Offres du Dimanche"
            )
            if success:
                record_france_notifier_sent(sunday_key)
                if msg_id:
                    promo_key = f"FR_{active_fr_promo.name}_{active_fr_promo.start_date.strftime('%Y%m%d')}"
                    state = load_france_state()
                    if "pinned_promo_events" not in state:
                        state["pinned_promo_events"] = {}
                    state["pinned_promo_events"][promo_key] = msg_id
                    save_france_state(state)
                results.append({
                    "type": "france_sunday_flash_alert",
                    "promo": active_fr_promo.name,
                    "message_id": msg_id,
                    "status": "published"
                })
            else:
                logger.error(f"Failed to post France Sunday flash alert: {err}")

    # 2. General Promo Calendar checks (Choice Day, Brand Day, 11.11, etc.)
    for promo in promo_tracker.calendar:
        if now < promo.start_date:
            pass
        elif promo.start_date <= now <= promo.end_date:
            time_since_start = now - promo.start_date
            if timedelta(hours=0) <= time_since_start <= timedelta(hours=6):
                notifier_key = f"FR_LAUNCH_ALERT_{promo.name}_{promo.start_date.strftime('%Y%m%d')}"
                if not is_france_notifier_already_sent(notifier_key):
                    logger.info(f"Triggering France Promo Launch Alert for {promo.name}")
                    text, markup = build_france_promo_launch_alert(promo)
                    success, err, msg_id = await send_france_promo_alert(text, markup, coupon_list=promo.coupon_tiers_fr, promo_title=promo.name_fr or promo.name)
                    if success:
                        record_france_notifier_sent(notifier_key)
                        results.append({
                            "type": "france_promo_launch_alert",
                            "promo": promo.name,
                            "message_id": msg_id,
                            "status": "published"
                        })
                    else:
                        logger.error(f"Failed to post France promo launch alert: {err}")

            time_until_end = promo.end_date - now
            if timedelta(hours=6) <= time_until_end <= timedelta(hours=36):
                notifier_key = f"FR_END_ALERT_{promo.name}_{promo.end_date.strftime('%Y%m%d')}"
                if not is_france_notifier_already_sent(notifier_key):
                    logger.info(f"Triggering France Promo Ending Alert for {promo.name}")
                    text, markup = build_france_promo_ending_alert(promo)
                    success, err, msg_id = await send_france_promo_alert(text, markup, coupon_list=promo.coupon_tiers_fr, promo_title=promo.name_fr or promo.name)
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

    # 3. Clean up expired pinned bulletins if promo has concluded
    try:
        await unpin_france_expired_bulletins(now)
    except Exception as e:
        logger.warning(f"Error unpinning France expired bulletins: {e}")

    # 4. Guarantee active event coupon bulletin is always pinned in France
    try:
        pinned_msg_id = await ensure_france_active_promo_coupons_pinned(now)
        if pinned_msg_id:
            results.append({
                "type": "france_active_promo_coupons_pinned",
                "message_id": pinned_msg_id,
                "status": "pinned"
            })
    except Exception as e:
        logger.warning(f"Error in ensure_france_active_promo_coupons_pinned: {e}")

    return results


async def ensure_france_active_promo_coupons_pinned(
    now: Optional[datetime] = None,
    force_post: bool = False
) -> Optional[int]:
    """
    Guarantees that during EVERY active promo event (e.g. Choice Day, Mega Brands, Super Sunday),
    an official French promo coupon bulletin is published and PINNED at the top of @francedealsdz.
    If already published and pinned for this event, verifies it remains pinned via Telegram API.
    """
    if now is None:
        now = datetime.now(timezone.utc)

    promo = getattr(promo_tracker, "get_active_france_promo", promo_tracker.get_active_promo)(now)
    if not promo or not promo.coupon_tiers_fr:
        return None

    state = load_france_state()
    pinned_promos = state.get("pinned_promo_events", {})
    promo_key = f"FR_{promo.name}_{promo.start_date.strftime('%Y%m%d')}"

    existing_msg_id = pinned_promos.get(promo_key)
    bot_token = settings.TELEGRAM_BOT_TOKEN or getattr(settings, "ADMIN_BOT_TOKEN", None) or os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("ADMIN_BOT_TOKEN")
    target = TARGET_FRANCE_CHANNEL

    # If already published for this event, re-verify it remains pinned in the channel
    if existing_msg_id and not force_post:
        try:
            api_url = f"https://api.telegram.org/bot{bot_token}"
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    f"{api_url}/pinChatMessage",
                    json={"chat_id": target, "message_id": existing_msg_id, "disable_notification": True}
                )
                if resp.status_code == 200 and resp.json().get("ok"):
                    logger.info(f"[FRANCE PROMO PIN] Verified active promo coupon bulletin #{existing_msg_id} remains PINNED for {promo.name}")
                    return existing_msg_id
        except Exception as e:
            logger.warning(f"Error checking France pinned status: {e}")

    # Build and post the official French coupon bulletin for this active event
    logger.info(f"[FRANCE PROMO PIN] Publishing and pinning official French coupon bulletin for {promo.name}...")
    if getattr(promo, "is_sunday_flash", False):
        text, markup = build_france_sunday_alert(promo)
    else:
        text, markup = build_france_promo_launch_alert(promo)
    success, err, msg_id = await send_france_promo_alert(text, markup, coupon_list=promo.coupon_tiers_fr, promo_title=promo.name_fr or promo.name)
    if success and msg_id:
        if "pinned_promo_events" not in state:
            state["pinned_promo_events"] = {}
        state["pinned_promo_events"][promo_key] = msg_id
        save_france_state(state)
        logger.info(f"[FRANCE PROMO PIN] Successfully published & PINNED coupon bulletin for {promo.name} (Msg #{msg_id}) to {target}")
        return msg_id
    else:
        logger.error(f"[FRANCE PROMO PIN] Failed to publish & pin France coupon bulletin: {err}")
        return None


async def unpin_france_expired_bulletins(now: Optional[datetime] = None) -> List[int]:
    """
    Unpins expired France promo bulletins when their respective promotional events conclude.
    """
    if now is None:
        now = datetime.now(timezone.utc)

    state = load_france_state()
    pinned = state.get("pinned_promo_events", {})
    if not pinned:
        return []

    bot_token = settings.TELEGRAM_BOT_TOKEN or getattr(settings, "ADMIN_BOT_TOKEN", None) or os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("ADMIN_BOT_TOKEN")
    if not bot_token:
        return []

    unpinned_ids = []
    keys_to_remove = []

    active_promo = getattr(promo_tracker, "get_active_france_promo", promo_tracker.get_active_promo)(now)
    active_key = f"FR_{active_promo.name}_{active_promo.start_date.strftime('%Y%m%d')}" if active_promo else None

    api_url = f"https://api.telegram.org/bot{bot_token}"
    async with httpx.AsyncClient(timeout=15.0) as client:
        for p_key, msg_id in list(pinned.items()):
            if p_key != active_key:
                try:
                    resp = await client.post(
                        f"{api_url}/unpinChatMessage",
                        json={"chat_id": TARGET_FRANCE_CHANNEL, "message_id": msg_id}
                    )
                    logger.info(f"[FRANCE UNPIN] Unpinned expired France bulletin #{msg_id} ({p_key}): {resp.status_code}")
                except Exception as e:
                    logger.warning(f"[FRANCE UNPIN] Failed to unpin message #{msg_id}: {e}")
                keys_to_remove.append(p_key)
                unpinned_ids.append(msg_id)

    if keys_to_remove:
        for k in keys_to_remove:
            pinned.pop(k, None)
        state["pinned_promo_events"] = pinned
        save_france_state(state)

    return unpinned_ids
