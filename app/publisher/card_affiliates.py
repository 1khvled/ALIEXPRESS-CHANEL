"""
Card & Crypto Affiliate Marketing Module (Square Algérie Partners)
Automates strategic, high-converting educational & sponsored posts for:
1. Bybit Card (100% Free Virtual Card, 0 fees, cashback, crypto/P2P funding)
2. RedotPay Card (Instant Virtual Visa, $5 welcome bonus, accepted globally)
3. Binance (P2P BaridiMob/CCP for Algeria, SEPA free deposits for France/EU)

Marketing Angles:
- Algerian Channel (@DzAliexpress0):
  Angle: Solving the payment problem for Algerians wanting to buy from AliExpress without international bank accounts.
  Highlights: Bybit is 100% FREE (0 fees, 0 subscription), instant issuance, easy funding via BaridiMob (Binance P2P).

- French Channel (@francedealsdz):
  Angle: Avoiding 2-3% bank FX fees, earning up to 10% Cashback on AliExpress purchases, spending crypto directly with Apple/Google Pay.
  Highlights: 0€ card fee, 0€ monthly fee, crypto-to-fiat real-time conversion.
"""
import os
import json
import time
import asyncio
from pathlib import Path
from typing import Optional, Tuple, Dict, Any, List
import httpx

from app.config.settings import settings
from app.utils.logger import logger, record_system_log
from app.utils.network import enforce_ipv4

enforce_ipv4()

# Partner Assets
AFFILIATES_DIR = Path(r"C:\Users\Abdelli\Desktop\square-rates-affiliates")
REDOTPAY_IMG = AFFILIATES_DIR / "partner-redotpay.jpg"
BINANCE_IMG = AFFILIATES_DIR / "partner-binance.jpg"

# Partner Referral URLs & Codes
BYBIT_CODE = "L9LLRP5"
BYBIT_URL = f"https://www.bybit.com/invite?ref={BYBIT_CODE}&medium=referral&utm_campaign=evergreen&share_to=Telegram"

REDOTPAY_CODE = "djbt3"
REDOTPAY_URL = f"https://url.hk/i/en/{REDOTPAY_CODE}"

BINANCE_CODE = "GRO_28502_3WGQR"
BINANCE_URL = f"https://www.binance.com/referral/earn-together/refer2earn-usdc/claim?hl=en&ref={BINANCE_CODE}&utm_source=referral_entrance"

STATE_FILE_DZ = Path(settings.BASE_DIR) / "storage" / "state" / "published_state.json"
STATE_FILE_FR = Path(settings.BASE_DIR) / "storage" / "state" / "france_published_state.json"
TARGET_FRANCE_CHANNEL = os.getenv("FRANCE_TARGET_CHANNEL_ID", "@francedealsdz")


# ==============================================================================
# ALGERIAN CHANNEL COPYWRITING (Dialect / Modern Arabic - Focus on Paying on AliExpress)
# ==============================================================================

DZ_VARIANTS = [
    # Variant 0: Bybit Virtual Card (100% FREE - No opening fee, no monthly fee)
    {
        "id": "dz_bybit_card_free",
        "title": "Bybit Free Card (Algeria)",
        "image_path": None,
        "caption": """<blockquote>💳 <b>كيفاش تشري من AliExpress وأنت في الجزائر؟ | بطاقة Bybit Card مجانية 100%! 🔥</b></blockquote>

بزاف ناس يعجبوهم عروض وهواتف AliExpress لكن ما يقدروش يطلبوها لأن البطاقات البنكية الجزائرية (بريدي موب، BNA...) ما تخدمش في المواقع العالمية.

الحل الأسهل والأضمن حالياً هو <b>بطاقة Bybit Card</b>:
✨ <b>مجانية تماماً (Gratuite):</b> 0 دج مصاريف فتح، وبدون أي اشتراك شهري أو اقتطاعات خفية!
✨ <b>بطاقة ماستركارد عالمية:</b> مقبولة 100% على AliExpress وPayPal وجميع المتاجر.
✨ <b>شحن فوري بالدينار:</b> تقدر تشحن رصيدك بسهولة عن طريق BaridiMob في 2 دقائق عبر P2P.
✨ <b>تفعيل فوري:</b> تسجل اليوم، تبدا تشري صيداتك وعروض العملات فوراً من هاتفك!

🎁 <b>كـود التسجيل الحصري للحصول على البونص:</b>
⏺ <code>L9LLRP5</code>

🔗 <b>رابط فتح حسابك وطلب بطاقتك المجانية ⤵️</b>
{bybit_url}

💡 <i>ملاحظة: البطاقة مجانية تماماً وتقدر تستعملها في الشراء العادي أو ربطها بالباي بال مباشرة.</i>
━━━━━━━━━━━━━━━━━
📢 <b>قناة الصيدات والصفقات:</b> @DzAliexpress0""".format(bybit_url=BYBIT_URL)
    },

    # Variant 1: RedotPay Card (Instant Virtual Visa + $5 Welcome Bonus)
    {
        "id": "dz_redotpay_visa",
        "title": "RedotPay Visa Card (Algeria)",
        "image_path": str(REDOTPAY_IMG) if REDOTPAY_IMG.exists() else None,
        "caption": """<blockquote>💳 <b>بطاقة فيزا RedotPay | الحل الأسرع للشراء من AliExpress مع هدية 5$ مجاناً! 🎁🔥</b></blockquote>

راهم كاينين صيدات قوية في AliExpress ومحتاج بطاقة فيزا افتراضية تتفعل في دقائق؟

<b>بطاقة فيزا RedotPay العالمية:</b>
✅ <b>هدية 5$ فورية:</b> بمجرد التسجيل بالكود الحصري <code>djbt3</code> يوصلك رصيد ترحيبي في حسابك!
✅ <b>مقبولة 100% في AliExpress:</b> تدعم خصم العملات، وتخفيضات الكوبونات وشحن الحزم.
✅ <b>ربط مباشر مع PayPal:</b> تقبل الربط مع بايبال جزائري أو أجنبي وتفعله كلياً.
✅ <b>شحن سهل وسريع:</b> تشحنها عبر Binance أو أي محفظة بـ USDT في ثوانٍ.

🎁 <b>كـود البـونص الترحيبي (5$ مجاناً):</b>
⏺ <code>djbt3</code>

🔗 <b>رابط التسجيل وتحميل التطبيق ⤵️</b>
{redotpay_url}

━━━━━━━━━━━━━━━━━
📢 <b>قناة الصيدات اليومية:</b> @DzAliexpress0""".format(redotpay_url=REDOTPAY_URL)
    },

    # Variant 2: Complete Toolkit - Binance P2P BaridiMob + Cards
    {
        "id": "dz_binance_p2p_guide",
        "title": "Binance P2P BaridiMob Guide (Algeria)",
        "image_path": str(BINANCE_IMG) if BINANCE_IMG.exists() else None,
        "caption": """<blockquote>🛒 <b>دليل الشراء بالدينار الجزائري (BaridiMob) | كيف تشحن بطاقاتك وتتسوق من AliExpress! 🇩🇿⚡</b></blockquote>

الكثير يسأل: <i>"عندي تطبيق بريدي موب، كيفاش نحولو لدولار ونشري بيه من AliExpress؟"</i>

الطريقة الرسمية والآمنة 100% التي يستعملها كل المحترفين:
1️⃣ <b>فتح حساب في منصة Binance:</b> أضخم وأضمن منصة تداول في العالم.
2️⃣ <b>شراء USDT عبر P2P:</b> تدخل لقسم P2P، تختار الدفع بـ <b>BaridiMob</b> وتشتري الدولار الرقمي (USDT) بالدينار الجزائري مباشرة من بائعين جزائريين موثوقين ومحميين بالنظام في دقيقتين.
3️⃣ <b>شحن بطاقتك (Bybit أو RedotPay):</b> ترسل الرصيد لبطاقتك بضغطة زر وتتسوق من AliExpress بأقل سعر صرف وبدون وسطاء يأخذون عليك عمولات مضاعفة!

🎁 <b>كـود الإحـالة للتسجيل والحصول على بونص الترحيب:</b>
⏺ <code>GRO_28502_3WGQR</code>

🔗 <b>رابط التسجيل الرسمي في Binance ⤵️</b>
{binance_url}

━━━━━━━━━━━━━━━━━
📢 <b>قناة الصيدات المعتمدة:</b> @DzAliexpress0""".format(binance_url=BINANCE_URL)
    }
]


# ==============================================================================
# FRENCH CHANNEL COPYWRITING (French - Focus on 0% FX fees, Cashback, Crypto Spend)
# ==============================================================================

FR_VARIANTS = [
    # Variant 0: Bybit Card (100% Free, Up to 10% Cashback on AliExpress, 0€ fees)
    {
        "id": "fr_bybit_card_cashback",
        "title": "Carte Bybit Cashback & 0€ Frais (France)",
        "image_path": None,
        "caption": """<blockquote>💳 <b>Astuce Bons Plans | Carte Bybit 100% GRATUITE & Jusqu'à 10% de Cashback sur AliExpress ! 🔥🇪🇺</b></blockquote>

Saviez-vous que la plupart des banques traditionnelles françaises facturent entre <b>2% et 3% de frais de change</b> sur les paiements internationaux en ligne ?

La <b>Carte Bybit</b> est le moyen le plus rentable pour payer vos commandes AliExpress, Amazon et tech :
✨ <b>100% Gratuite :</b> 0€ de frais de création, 0€ d'abonnement mensuel et sans conditions de revenus !
✨ <b>Jusqu'à 10% de Cashback :</b> Récupérez une partie de votre argent sur chaque achat effectué.
✨ <b>Multi-devises & Crypto :</b> Payez en Euros ou directement avec vos cryptos (USDT, BTC, ETH) avec conversion instantanée au taux officiel Mastercard.
✨ <b>Paiement Sans Contact :</b> Compatible Apple Pay & Google Pay dès la validation.

🎁 <b>Code Parrainage Exclusif :</b>
⏺ <code>L9LLRP5</code>

🔗 <b>Commandez votre carte virtuelle gratuite en 2 minutes ⤵️</b>
{bybit_url}

━━━━━━━━━━━━━━━━━
📢 <b>Bons Plans & Codes Promo France :</b> @francedealsdz""".format(bybit_url=BYBIT_URL)
    },

    # Variant 1: RedotPay Crypto Visa Card (5$ Welcome Gift)
    {
        "id": "fr_redotpay_visa",
        "title": "Carte Visa RedotPay 5$ Offerts (France)",
        "image_path": str(REDOTPAY_IMG) if REDOTPAY_IMG.exists() else None,
        "caption": """<blockquote>💳 <b>Carte Visa RedotPay | Dépensez vos cryptos sur AliExpress en toute liberté (+ 5$ offerts) 🎁⚡</b></blockquote>

Besoin d'une carte Visa internationale sans passer par une banque classique pour vos achats high-tech et AliExpress ?

<b>La carte Visa RedotPay :</b>
✅ <b>Bonus de 5$ offert :</b> Recevez 5$ de crédit dès votre inscription avec le code <code>djbt3</code>.
✅ <b>Zéro paperasse :</b> Carte virtuelle émise en quelques secondes, prête à l'emploi.
✅ <b>Acceptée partout :</b> Fonctionne à 100% sur AliExpress, Amazon, abonnements en ligne et PayPal.
✅ <b>Recharge instantanée :</b> Déposez en USDT ou cryptos sans frais cachés.

🎁 <b>Code Promo Bonus (5$ gratuits) :</b>
⏺ <code>djbt3</code>

🔗 <b>Activez votre carte Visa et réclamez vos 5$ ⤵️</b>
{redotpay_url}

━━━━━━━━━━━━━━━━━
📢 <b>Canal Officiel France :</b> @francedealsdz""".format(redotpay_url=REDOTPAY_URL)
    },

    # Variant 2: Binance Europe (Invest in Crypto + Stocks, P2P, Secured, 0€ SEPA)
    {
        "id": "fr_binance_invest_crypto_stocks",
        "title": "Binance Invest Crypto, Stocks & P2P (France)",
        "image_path": str(BINANCE_IMG) if BINANCE_IMG.exists() else None,
        "caption": """<blockquote>🚀 <b>Binance | N°1 Mondial : Investissez en Crypto, Actions & Achetez en P2P en toute Sécurité ! 🇪🇺⚡</b></blockquote>

Vous cherchez la plateforme la plus fiable et complète pour gérer vos cryptos, diversifier votre épargne et financer vos achats high-tech ?

<b>Pourquoi choisir Binance :</b>
🔹 <b>Investissement Crypto & Actions :</b> Achetez Bitcoin, Ethereum, USDT et accédez aux marchés mondiaux ainsi qu'aux actions tokenisées en toute simplicité.
🔹 <b>Achat Crypto P2P & Virement SEPA Gratuit :</b> Déposez des Euros sans aucun frais via SEPA instantané ou achetez/vendez directement entre particuliers (P2P) au taux réel sans intermédiaire.
🔹 <b>Sécurité Maximale (Fonds SAFU) :</b> Plateforme enregistrée PSAN en France (régulée par l'AMF) avec protection intégrale de vos avoirs grâce au fonds de garantie SAFU.
🔹 <b>Revenus Passifs (Earn & Staking) :</b> Faites fructifier vos USDT et cryptos stables avec des rendements attractifs pendant que vous profitez des soldes en ligne.

🎁 <b>Bonus de bienvenue exclusif via notre lien partenaire :</b>
⏺ <b>Code Référent :</b> <code>GRO_28502_3WGQR</code>

🔗 <b>Inscrivez-vous et débloquez votre bonus de bienvenue ⤵️</b>
{binance_url}

━━━━━━━━━━━━━━━━━
📢 <b>Bons Plans & Tech France :</b> @francedealsdz""".format(binance_url=BINANCE_URL)
    }
]


# ==============================================================================
# STATE & ELIGIBILITY MANAGEMENT (STRICT 24H ROTATION LOCK)
# ==============================================================================

async def has_recent_card_post_in_channel(channel_username: str, max_check: int = 15) -> bool:
    """
    Scrapes the public channel web preview to check if any partner ad was published recently.
    Prevents duplicate posts even across ephemeral CI/CD environments or state resets.
    """
    clean_ch = channel_username.replace("@", "").strip()
    try:
        url = f"https://t.me/s/{clean_ch}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        async with httpx.AsyncClient(timeout=8.0, follow_redirects=True, headers=headers) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(resp.text, "html.parser")
                msgs = soup.find_all("div", class_="tgme_widget_message_wrap")
                for m in msgs[-max_check:]:
                    text_el = m.find("div", class_="tgme_widget_message_text")
                    if text_el:
                        t = text_el.get_text()
                        if any(k in t for k in [BYBIT_CODE, REDOTPAY_CODE, BINANCE_CODE, "Bybit", "RedotPay"]):
                            return True
    except Exception as e:
        logger.warning(f"Live channel preview check failed for @{clean_ch}: {e}")
    return False


async def is_card_affiliate_eligible_dz(min_hours: float = 24.0) -> Tuple[bool, str]:
    """Checks whether the Algerian channel is eligible for the next day-to-day card affiliate post (strictly once every 24h)."""
    # 1. Check local state file
    if STATE_FILE_DZ.exists():
        try:
            with open(STATE_FILE_DZ, "r", encoding="utf-8") as f:
                state = json.load(f)
            last_time = state.get("last_card_affiliate_time_dz", 0.0)
            elapsed = (time.time() - last_time) / 3600.0
            if elapsed < min_hours:
                return False, f"Anti-duplicate lock: {elapsed:.1f}h since last card post (< {min_hours}h required). Skipping."
        except Exception as e:
            logger.warning(f"State read warning (DZ): {e}")

    # 2. Live channel verification (safety net against duplicate posts)
    chat_id = settings.TARGET_CHANNEL_ID or "@DzAliexpress0"
    if await has_recent_card_post_in_channel(chat_id, max_check=15):
        return False, "Anti-duplicate lock: Recent partner ad detected in live channel feed. Skipping."

    return True, f"Eligible: >= {min_hours}h since last card post"


def record_card_affiliate_published_dz(variant_idx: int):
    """Records the published timestamp and updates the variant rotation for Algeria."""
    try:
        STATE_FILE_DZ.parent.mkdir(parents=True, exist_ok=True)
        state = {}
        if STATE_FILE_DZ.exists():
            with open(STATE_FILE_DZ, "r", encoding="utf-8") as f:
                state = json.load(f)
        state["last_card_affiliate_time_dz"] = time.time()
        state["card_affiliate_variant_idx_dz"] = (variant_idx + 1) % len(DZ_VARIANTS)
        with open(STATE_FILE_DZ, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Failed to record card affiliate state (DZ): {e}")


async def is_card_affiliate_eligible_fr(min_hours: float = 24.0) -> Tuple[bool, str]:
    """Checks whether the French channel is eligible for the next day-to-day card affiliate post (strictly once every 24h)."""
    # 1. Check local state file
    if STATE_FILE_FR.exists():
        try:
            with open(STATE_FILE_FR, "r", encoding="utf-8") as f:
                state = json.load(f)
            last_time = state.get("last_card_affiliate_time_fr", 0.0)
            elapsed = (time.time() - last_time) / 3600.0
            if elapsed < min_hours:
                return False, f"Anti-duplicate lock: {elapsed:.1f}h since last card post (< {min_hours}h required). Skipping."
        except Exception as e:
            logger.warning(f"State read warning (FR): {e}")

    # 2. Live channel verification (safety net against duplicate posts)
    chat_id = TARGET_FRANCE_CHANNEL
    if await has_recent_card_post_in_channel(chat_id, max_check=15):
        return False, "Anti-duplicate lock: Recent partner ad detected in live channel feed. Skipping."

    return True, f"Eligible: >= {min_hours}h since last card post"


def record_card_affiliate_published_fr(variant_idx: int):
    """Records the published timestamp and updates the variant rotation for France."""
    try:
        STATE_FILE_FR.parent.mkdir(parents=True, exist_ok=True)
        state = {}
        if STATE_FILE_FR.exists():
            with open(STATE_FILE_FR, "r", encoding="utf-8") as f:
                state = json.load(f)
        state["last_card_affiliate_time_fr"] = time.time()
        state["card_affiliate_variant_idx_fr"] = (variant_idx + 1) % len(FR_VARIANTS)
        with open(STATE_FILE_FR, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Failed to record card affiliate state (FR): {e}")


# ==============================================================================
# PUBLISHING LOGIC
# ==============================================================================

async def publish_card_affiliate_post(
    chat_id: str,
    caption: str,
    image_path: Optional[str] = None
) -> Tuple[bool, Optional[str], Optional[int]]:
    """Publishes a photo or text post with HTML caption to Telegram."""
    enforce_ipv4()
    bot_token = (
        getattr(settings, "TELEGRAM_BOT_TOKEN", None)
        or getattr(settings, "ADMIN_BOT_TOKEN", None)
        or os.getenv("TELEGRAM_BOT_TOKEN", "")
    )
    if not bot_token:
        return False, "Missing TELEGRAM_BOT_TOKEN", None

    api_url = f"https://api.telegram.org/bot{bot_token}"

    async with httpx.AsyncClient(timeout=25.0) as client:
        # If an image exists, publish via sendPhoto
        if image_path and os.path.exists(image_path):
            try:
                with open(image_path, "rb") as photo_file:
                    files = {"photo": photo_file}
                    data = {
                        "chat_id": chat_id,
                        "caption": caption,
                        "parse_mode": "HTML"
                    }
                    resp = await client.post(f"{api_url}/sendPhoto", data=data, files=files)
                if resp.status_code == 200 and resp.json().get("ok"):
                    msg_id = resp.json().get("result", {}).get("message_id")
                    return True, None, msg_id
                else:
                    logger.warning(f"sendPhoto failed ({resp.status_code}): {resp.text}. Falling back to sendMessage.")
            except Exception as e:
                logger.warning(f"sendPhoto error: {e}. Falling back to sendMessage.")

        # Fallback to sendMessage
        try:
            data = {
                "chat_id": chat_id,
                "text": caption,
                "parse_mode": "HTML",
                "disable_web_page_preview": False
            }
            resp = await client.post(f"{api_url}/sendMessage", data=data)
            if resp.status_code == 200 and resp.json().get("ok"):
                msg_id = resp.json().get("result", {}).get("message_id")
                return True, None, msg_id
            return False, resp.text, None
        except Exception as e:
            return False, str(e), None


async def post_card_affiliate_algeria(force: bool = False, variant_idx: Optional[int] = None) -> Tuple[bool, str]:
    """Posts a card affiliate marketing post to the Algerian channel (@DzAliexpress0)."""
    if not force:
        eligible, reason = await is_card_affiliate_eligible_dz(min_hours=24.0)
        if not eligible:
            return False, f"Skipped (DZ): {reason}"

    # Determine variant
    state = {}
    if STATE_FILE_DZ.exists():
        try:
            with open(STATE_FILE_DZ, "r", encoding="utf-8") as f:
                state = json.load(f)
        except Exception:
            pass

    if variant_idx is None:
        variant_idx = state.get("card_affiliate_variant_idx_dz", 0) % len(DZ_VARIANTS)

    variant = DZ_VARIANTS[variant_idx]
    chat_id = settings.TARGET_CHANNEL_ID or "@DzAliexpress0"

    success, err, msg_id = await publish_card_affiliate_post(
        chat_id=chat_id,
        caption=variant["caption"],
        image_path=variant.get("image_path")
    )

    if success:
        record_card_affiliate_published_dz(variant_idx)
        try:
            await record_system_log(
                level="INFO",
                component="card_affiliates_dz",
                message=f"Published {variant['title']} to {chat_id} (msg #{msg_id})"
            )
        except Exception:
            pass
        return True, f"Published {variant['title']} to {chat_id} (msg #{msg_id})"
    return False, f"Failed to publish {variant['title']}: {err}"


async def post_card_affiliate_france(force: bool = False, variant_idx: Optional[int] = None) -> Tuple[bool, str]:
    """Posts a card affiliate marketing post to the French channel (@francedealsdz)."""
    if not force:
        eligible, reason = await is_card_affiliate_eligible_fr(min_hours=24.0)
        if not eligible:
            return False, f"Skipped (FR): {reason}"

    # Determine variant
    state = {}
    if STATE_FILE_FR.exists():
        try:
            with open(STATE_FILE_FR, "r", encoding="utf-8") as f:
                state = json.load(f)
        except Exception:
            pass

    if variant_idx is None:
        variant_idx = state.get("card_affiliate_variant_idx_fr", 0) % len(FR_VARIANTS)

    variant = FR_VARIANTS[variant_idx]
    chat_id = TARGET_FRANCE_CHANNEL

    success, err, msg_id = await publish_card_affiliate_post(
        chat_id=chat_id,
        caption=variant["caption"],
        image_path=variant.get("image_path")
    )

    if success:
        record_card_affiliate_published_fr(variant_idx)
        try:
            await record_system_log(
                level="INFO",
                component="card_affiliates_fr",
                message=f"Published {variant['title']} to {chat_id} (msg #{msg_id})"
            )
        except Exception:
            pass
        return True, f"Published {variant['title']} to {chat_id} (msg #{msg_id})"
    return False, f"Failed to publish {variant['title']}: {err}"
