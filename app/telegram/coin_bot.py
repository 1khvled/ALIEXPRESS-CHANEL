"""
AliExpress Coin & Discount Bot Handler
Processes incoming user messages with AliExpress links and generates:
1. Maximum Coins Discount Page URL (سعر تخفيض العملات)
2. Bundle Deals URL (سعر عرض bundle deal)
3. Super Deals URL (سعر السوبر ديلز)
4. Limited Offer / Big Save URL (سعر العرض المحدود)
All wrapped with official s.click affiliate tracking for monetization.
"""
import asyncio
import re
from typing import Optional, Dict, Any, List
import httpx
from aliexpress_api import AliexpressApi, models

from app.config.settings import settings
from app.aliexpress.urls import extract_all_urls, extract_product_id_from_url
from app.aliexpress.resolver import url_resolver
from app.utils.logger import logger

WELCOME_TEXT = """👋 مرحباً بك في بوت زيادة تخفيض العملات! 🪙

هذا البوت يعمل على **زيادة نسبة التخفيض بالعملات (النقاط)** من 1%~5% إلى نسبة عالية تصل حتى **90%** في بعض المنتجات 🤑

📌 **طريقة الاستخدام:**
1. انسخ رابط أي منتج تريده من تطبيق أو موقع AliExpress.
2. أرسل الرابط هنا في المحادثة.
3. سيرسل لك البوت فوراً روابط التخفيض الأكبر (تخفيض العملات، Bundle Deals، السوبر ديلز)! 🚀
"""

async def resolve_product_from_text(text: str) -> Optional[Dict[str, Any]]:
    """Extracts AliExpress product ID and details from user text."""
    urls = extract_all_urls(text)
    if not urls:
        # Check if the user just pasted a bare product ID
        clean = text.strip()
        if clean.isdigit() and len(clean) >= 10:
            return {"product_id": clean, "canonical_url": f"https://www.aliexpress.com/item/{clean}.html"}
        return None

    raw_url = urls[0]
    resolved = await url_resolver.resolve(raw_url)
    if not resolved or not resolved.product_id:
        return None

    return {
        "product_id": resolved.product_id,
        "canonical_url": resolved.canonical_url
    }

async def generate_coin_discount_response(product_id: str, canonical_url: str) -> Optional[Dict[str, Any]]:
    """
    Queries AliExpress Open Platform API to get product info and generates
    the 4 special discount affiliate links (Coins, Bundle, Super Deals, Limited).
    """
    app_key = settings.ALIEXPRESS_AFFILIATE_APP_KEY
    app_secret = settings.ALIEXPRESS_AFFILIATE_APP_SECRET
    tracking_id = settings.ALIEXPRESS_AFFILIATE_TRACKING_ID or "default"

    if not app_key or not app_secret:
        logger.error("AliExpress Affiliate credentials not configured")
        return None

    try:
        api = AliexpressApi(app_key, app_secret, models.Language.EN, models.Currency.USD, tracking_id)

        # 1. Fetch product title and price with retry
        prod_title = "منتج مميز من AliExpress"
        prod_price = None

        for attempt in range(3):
            try:
                details = await asyncio.to_thread(api.get_products_details, [product_id])
                if details and len(details) > 0:
                    info = details[0]
                    t = getattr(info, 'product_title', None)
                    if t:
                        prod_title = t[:90]
                    p = getattr(info, 'target_sale_price', None) or getattr(info, 'sale_price', None)
                    if p:
                        try:
                            prod_price = float(p)
                        except Exception:
                            pass
                break
            except Exception as e:
                if "ApiCallLimit" in str(e) or "frequency exceeds" in str(e):
                    await asyncio.sleep(1.5)
                else:
                    break

        # 2. Build the 5 special promotional URLs
        target_urls = [
            f"https://m.aliexpress.com/p/coin-index/index.html?productIds={product_id}",
            f"https://www.aliexpress.com/item/{product_id}.html?sourceType=620&channel=coin",
            f"https://www.aliexpress.com/ssr/300000512/BundleDeals2?productIds={product_id}",
            f"https://www.aliexpress.com/item/{product_id}.html?sourceType=680",
            f"https://www.aliexpress.com/item/{product_id}.html?sourceType=562",
        ]

        # 3. Generate official s.click affiliate links in batch with retry
        aff_map = {}
        for attempt in range(3):
            try:
                raw_links = await asyncio.to_thread(api.get_affiliate_links, ",".join(target_urls))
                if raw_links:
                    for item in raw_links:
                        orig = getattr(item, 'source_value', '')
                        promo = getattr(item, 'promotion_link', '')
                        if orig and promo:
                            aff_map[orig] = promo
                break
            except Exception as e:
                if "ApiCallLimit" in str(e) or "frequency exceeds" in str(e):
                    await asyncio.sleep(1.5)
                else:
                    break

        # Extract links or fallback to direct canonical affiliate
        coin_link_1 = aff_map.get(target_urls[0], target_urls[0])
        coin_link_2 = aff_map.get(target_urls[1], target_urls[1])
        bundle_link = aff_map.get(target_urls[2], target_urls[2])
        super_link = aff_map.get(target_urls[3], target_urls[3])
        limited_link = aff_map.get(target_urls[4], target_urls[4])

        # 4. Format message matching Algerian channel standards exactly
        price_str = f"{prod_price:.2f}" if prod_price else ""

        message_text = f"""{prod_title}

✔️ سعر تخفيض العملات: {price_str} $
🔗 الرابط في صفحة التخفيضات:
{coin_link_1}
{coin_link_2}

✔️ سعر عرض bundle deal ب : $
🔗 الرابط:
{bundle_link}

✔️ سعر السوبر ديلز : $
🔗 الرابط:
{super_link}

✔️ سعر العرض المحدود: $
🔗 الرابط:
{limited_link}"""

        # Inline buttons
        reply_markup = {
            "inline_keyboard": [
                [
                    {"text": "📢 قناتنا على Telegram", "url": "https://t.me/DzAliexpress0"},
                ],
                [
                    {
                        "text": "🔄 مشاركة البوت مع أصدقائك",
                        "url": f"https://t.me/share/url?url=https://t.me/Alilo07BOT&text={httpx.URL('بوت زيادة تخفيض العملات في علي اكسبرس 🪙🔥').path}"
                    }
                ]
            ]
        }

        return {
            "text": message_text,
            "reply_markup": reply_markup
        }

    except Exception as e:
        logger.error(f"Error generating coin bot response: {e}")
        return None

async def handle_telegram_update(update: Dict[str, Any]) -> bool:
    """Handles an incoming Telegram update from webhook or polling."""
    token = settings.TELEGRAM_BOT_TOKEN
    if not token:
        return False

    message = update.get("message") or update.get("edited_message")
    if not message:
        return False

    chat_id = message.get("chat", {}).get("id")
    text = (message.get("text") or "").strip()
    if not chat_id:
        return False

    # 1. /start command
    if text.startswith("/start"):
        await send_telegram_message(token, chat_id, WELCOME_TEXT)
        return True

    # 2. Check for product link
    product_data = await resolve_product_from_text(text)
    if not product_data:
        help_msg = (
            "⚠️ الرجاء إرسال رابط صحيح لمنتج من AliExpress.\n\n"
            "مثال:\n"
            "https://a.aliexpress.com/_c4ttSySh\n"
            "أو\n"
            "https://www.aliexpress.com/item/1005006533038973.html"
        )
        await send_telegram_message(token, chat_id, help_msg)
        return True

    # Send processing indicator
    async with httpx.AsyncClient(timeout=8.0) as client:
        await client.post(
            f"https://api.telegram.org/bot{token}/sendChatAction",
            json={"chat_id": chat_id, "action": "typing"}
        )

    # 3. Generate discount links
    res = await generate_coin_discount_response(
        product_data["product_id"],
        product_data["canonical_url"]
    )

    if not res:
        err_msg = "❌ تعذر استخراج روابط التخفيض لهذا المنتج. يرجى التأكد من الرابط والمحاولة مجدداً."
        await send_telegram_message(token, chat_id, err_msg)
        return False

    # 4. Reply with discounts
    await send_telegram_message(
        token=token,
        chat_id=chat_id,
        text=res["text"],
        reply_markup=res["reply_markup"]
    )
    return True

async def send_telegram_message(
    token: str,
    chat_id: int,
    text: str,
    reply_markup: Optional[Dict[str, Any]] = None
) -> bool:
    """Sends a Telegram message using Bot API."""
    try:
        payload = {
            "chat_id": chat_id,
            "text": text,
            "disable_web_page_preview": False
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup

        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json=payload
            )
            return resp.status_code == 200
    except Exception as e:
        logger.error(f"Failed to send telegram message to {chat_id}: {e}")
        return False
