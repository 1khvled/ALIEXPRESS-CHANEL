"""
Lightweight Serverless AliExpress Coin & Discount Bot for Vercel
Directly handles Telegram webhook updates without heavy dependencies.
"""
import asyncio
import os
import re
from typing import Optional, Dict, Any, List
from urllib.parse import urlparse, parse_qs
import httpx
from aliexpress_api import AliexpressApi, models

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8900887118:AAFuAFcxS1Xa2K4g0tlpD_YutPrsco3Y-Vo")
ALIEXPRESS_AFFILIATE_APP_KEY = os.getenv("ALIEXPRESS_AFFILIATE_APP_KEY", "538348")
ALIEXPRESS_AFFILIATE_APP_SECRET = os.getenv("ALIEXPRESS_AFFILIATE_APP_SECRET", "7z5QlJZAxNka2zBrgzCWrUNusBXJGHYx")
ALIEXPRESS_AFFILIATE_TRACKING_ID = os.getenv("ALIEXPRESS_AFFILIATE_TRACKING_ID", "dzkhvled16")
TARGET_CHANNEL_ID = os.getenv("TARGET_CHANNEL_ID", "@DzAliexpress0")

WELCOME_TEXT = """👋 مرحباً بك في بوت زيادة تخفيض العملات! 🪙

هذا البوت يعمل على **زيادة نسبة التخفيض بالعملات (النقاط)** من 1%~5% إلى نسبة عالية تصل حتى **90%** في بعض المنتجات 🤑

📌 **طريقة الاستخدام:**
1. انسخ رابط أي منتج تريده من تطبيق أو موقع AliExpress.
2. أرسل الرابط هنا في المحادثة.
3. سيرسل لك البوت فوراً روابط التخفيض الأكبر (تخفيض العملات، Bundle Deals، السوبر ديلز)! 🚀
"""

URL_REGEX = re.compile(r'(https?://[^\s<>"\',;]+)', re.IGNORECASE)

def extract_urls(text: str) -> List[str]:
    if not text:
        return []
    urls = URL_REGEX.findall(text)
    return [u.rstrip(".,;!?:)]}\"'>") for u in urls if u.startswith("http")]

def extract_pid(url: str) -> Optional[str]:
    if not url:
        return None
    # /item/{id}.html
    m = re.search(r'/item/(\d+)', url, re.IGNORECASE)
    if m:
        return m.group(1)
    # productIds=...
    m = re.search(r'productIds?=(\d+)', url, re.IGNORECASE)
    if m:
        return m.group(1)
    try:
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        for k in ["productId", "product_id", "id", "itemId"]:
            if k in qs and qs[k] and qs[k][0].isdigit():
                return qs[k][0]
    except Exception:
        pass
    return None

async def resolve_ali_url(raw_url: str) -> Optional[str]:
    """Resolves short redirect links like s.click or a.aliexpress.com."""
    pid = extract_pid(raw_url)
    if pid and "s.click" not in raw_url and "a.aliexpress" not in raw_url:
        return pid

    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            resp = await client.get(
                raw_url,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            )
            final_url = str(resp.url)
            found = extract_pid(final_url)
            if not found and resp.text:
                found = extract_pid(resp.text)
            return found
    except Exception:
        return extract_pid(raw_url)

async def generate_coin_discount_response(product_id: str) -> Optional[Dict[str, Any]]:
    """Generates the exact discount message and s.click links shown in user screenshot."""
    try:
        api = AliexpressApi(
            ALIEXPRESS_AFFILIATE_APP_KEY,
            ALIEXPRESS_AFFILIATE_APP_SECRET,
            models.Language.EN,
            models.Currency.USD,
            ALIEXPRESS_AFFILIATE_TRACKING_ID
        )

        # 1. Fetch title & price
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

        # 2. Build promotional URLs
        target_urls = [
            f"https://m.aliexpress.com/p/coin-index/index.html?productIds={product_id}",
            f"https://www.aliexpress.com/item/{product_id}.html?sourceType=620&channel=coin",
            f"https://www.aliexpress.com/ssr/300000512/BundleDeals2?productIds={product_id}",
            f"https://www.aliexpress.com/item/{product_id}.html?sourceType=680",
            f"https://www.aliexpress.com/item/{product_id}.html?sourceType=562",
        ]

        # 3. Generate s.click affiliate links
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

        coin_link_1 = aff_map.get(target_urls[0], target_urls[0])
        coin_link_2 = aff_map.get(target_urls[1], target_urls[1])
        bundle_link = aff_map.get(target_urls[2], target_urls[2])
        super_link = aff_map.get(target_urls[3], target_urls[3])
        limited_link = aff_map.get(target_urls[4], target_urls[4])

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

        reply_markup = {
            "inline_keyboard": [
                [
                    {"text": "📢 مجموعتنا على Telegram", "url": "https://t.me/DzAliexpress0"},
                ],
                [
                    {
                        "text": "🔄 مشاركة البوت مع أصدقائك",
                        "url": "https://t.me/share/url?url=https://t.me/Alilo07BOT&text=بوت زيادة تخفيض العملات في علي اكسبرس 🪙🔥"
                    }
                ]
            ]
        }

        return {
            "text": message_text,
            "reply_markup": reply_markup
        }

    except Exception as e:
        return None

async def handle_update(update: Dict[str, Any]) -> bool:
    message = update.get("message") or update.get("edited_message")
    if not message:
        return False

    chat_id = message.get("chat", {}).get("id")
    text = (message.get("text") or "").strip()
    if not chat_id:
        return False

    if text.startswith("/start"):
        await send_msg(chat_id, WELCOME_TEXT)
        return True

    urls = extract_urls(text)
    if not urls:
        if text.isdigit() and len(text) >= 10:
            pid = text
        else:
            help_msg = (
                "⚠️ الرجاء إرسال رابط صحيح لمنتج من AliExpress.\n\n"
                "مثال:\n"
                "https://a.aliexpress.com/_c4ttSySh\n"
                "أو\n"
                "https://www.aliexpress.com/item/1005006533038973.html"
            )
            await send_msg(chat_id, help_msg)
            return True
    else:
        pid = await resolve_ali_url(urls[0])

    if not pid:
        err_msg = "❌ تعذر استخراج كود المنتج من الرابط. يرجى التأكد من الرابط والمحاولة مجدداً."
        await send_msg(chat_id, err_msg)
        return False

    # Send typing status
    async with httpx.AsyncClient(timeout=5.0) as client:
        await client.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendChatAction",
            json={"chat_id": chat_id, "action": "typing"}
        )

    res = await generate_coin_discount_response(pid)
    if not res:
        err_msg = "❌ تعذر توليد روابط التخفيض لهذا المنتج حالياً. يرجى المحاولة بعد قليل."
        await send_msg(chat_id, err_msg)
        return False

    await send_msg(chat_id, res["text"], res["reply_markup"])
    return True

async def send_msg(chat_id: int, text: str, reply_markup: Optional[Dict] = None):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "disable_web_page_preview": False
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    async with httpx.AsyncClient(timeout=10.0) as client:
        await client.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json=payload
        )
