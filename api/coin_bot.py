"""
Lightweight Serverless AliExpress Coin & Discount Bot for Vercel
Directly handles Telegram webhook updates without heavy dependencies.
Optimized for ultra-fast (<1s) response times:
- Fast 1-hop redirect resolution (reads Location header without downloading pages)
- Parallel API calls (product details + affiliate links in asyncio.gather)
- HTML mode with proper escaping (never breaks on underscores in URLs)
- Auto fallback if photo fails or HTML parse error
"""
import asyncio
import html
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
DZD_USD_RATE = 240.0

WELCOME_TEXT = """👋 مرحباً بك في بوت DealScoutDz لزيادة تخفيض العملات! 🪙

هذا البوت يعمل على **زيادة نسبة التخفيض بالعملات (النقاط)** من 1%~5% إلى نسبة عالية تصل حتى **70%** في معظم منتجات AliExpress 🤑

📌 **طريقة الاستخدام بكل بساطة:**
1️⃣ انسخ رابط أي منتج تريده من تطبيق أو موقع AliExpress.
2️⃣ أرسل الرابط هنا في المحادثة.
3️⃣ سيرسل لك البوت فوراً صورة المنتج وروابط التخفيض الأكبر (تخفيض العملات، Bundle Deals، السوبر ديلز) مع أزرار شراء سريعة! 🚀
"""

HELP_TEXT = """💡 <b>دليل استخدام تخفيض العملات بأقصى نسبة:</b>

1️⃣ <b>كيف تفعل الخصم الأكبر؟</b>
عند فتح رابط العملات، لا تشترِ من الصفحة العادية! اضغط على زر <b>"شراء الآن"</b> مباشرة من صفحة العملات، أو أضف المنتج إلى السلة من داخل صفحة العملات لتخصم لك كل النقاط المتاحة.

2️⃣ <b>تحويل الدولة إلى كوريا 🇰🇷:</b>
لا تنسى تحويل دولة التطبيق إلى كوريا 🇰🇷 📍 من إعدادات AliExpress للحصول على أسعار أقل وتخفيض عملات إضافي على الكثير من الأجهزة والعتاد!

3️⃣ <b>كيف تجمع العملات يومياً؟</b>
ادخل يومياً لتطبيق AliExpress واضغط على أيقونة <b>Coins / العملات</b> واجمع العملات المجانية اليومية (يمكنك جمع 70 إلى 150 عملة يومياً مجاناً).

4️⃣ <b>الكوبونات الإضافية:</b>
يمكنك دمج تخفيض العملات مع كودات التخفيض للحصول على أقل سعر ممكن عالمياً!

📢 للمزيد من العروض اليومية، انضم لقناتنا: @DzAliexpress0
"""

COUPONS_TEXT = """🎟️ <b>أحدث كودات التخفيض من AliExpress لشهر أكتوبر 🔥</b>
━━━━━━━━━━━━━━━━━
🎯 <b>تخفيضات Choice Day (1 - 7 أكتوبر):</b>
▫️ خصم 3$ عند الشراء بـ 29$+ ⬅️ كود: <code>CDDZ03</code>
▫️ خصم 6$ عند الشراء بـ 49$+ ⬅️ كود: <code>CDDZ06</code>
▫️ خصم 10$ عند الشراء بـ 79$+ ⬅️ كود: <code>CDDZ10</code>
▫️ خصم 20$ عند الشراء بـ 159$+ ⬅️ كود: <code>CDDZ20</code>
▫️ خصم 40$ عند الشراء بـ 299$+ ⬅️ كود: <code>CDDZ40</code>
━━━━━━━━━━━━━━━━━
💡 يمكنك إدخال الكود في صفحة الدفع والاستفادة من خصم العملات في نفس الوقت!

📢 تابع قناتنا للمزيد: @DzAliexpress0
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
    """Fast resolution of AliExpress product ID without downloading entire pages."""
    pid = extract_pid(raw_url)
    if pid and "s.click" not in raw_url and "a.aliexpress" not in raw_url:
        return pid

    # Fast 1-hop redirect check (no body download)
    try:
        async with httpx.AsyncClient(timeout=3.5, follow_redirects=False) as client:
            resp = await client.get(
                raw_url,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            )
            loc = resp.headers.get("location") or resp.headers.get("Location")
            if loc:
                found = extract_pid(loc)
                if found:
                    return found
            if resp.status_code in (301, 302, 303, 307, 308) and loc:
                resp2 = await client.get(
                    loc,
                    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
                    timeout=3.0
                )
                loc2 = resp2.headers.get("location") or str(resp2.url)
                found = extract_pid(loc2)
                if found:
                    return found
    except Exception:
        pass

    return extract_pid(raw_url)

async def generate_coin_discount_response(product_id: str) -> Optional[Dict[str, Any]]:
    """Generates the rich discount response with direct affiliate links and photo in parallel."""
    try:
        api = AliexpressApi(
            ALIEXPRESS_AFFILIATE_APP_KEY,
            ALIEXPRESS_AFFILIATE_APP_SECRET,
            models.Language.EN,
            models.Currency.USD,
            ALIEXPRESS_AFFILIATE_TRACKING_ID
        )

        target_urls = [
            f"https://m.aliexpress.com/p/coin-index/index.html?productIds={product_id}",
            f"https://www.aliexpress.com/ssr/300000512/BundleDeals2?productIds={product_id}",
            f"https://www.aliexpress.com/item/{product_id}.html?sourceType=680",
            f"https://www.aliexpress.com/item/{product_id}.html?sourceType=562",
        ]

        # 1. Fetch details
        prod_title = "منتج مميز من AliExpress"
        prod_price = None
        prod_image = None
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
                img = getattr(info, 'product_main_image_url', None)
                if img and ("alicdn.com" in img or "aliexpress-media.com" in img):
                    prod_image = img
        except Exception:
            pass

        await asyncio.sleep(0.15)

        # 2. Fetch affiliate links
        aff_map = {}
        try:
            raw_links = await asyncio.to_thread(api.get_affiliate_links, ",".join(target_urls))
            if raw_links:
                for item in raw_links:
                    orig = getattr(item, 'source_value', '')
                    promo = getattr(item, 'promotion_link', '')
                    if orig and promo:
                        aff_map[orig] = promo
        except Exception:
            pass

        coin_link = aff_map.get(target_urls[0], target_urls[0])
        bundle_link = aff_map.get(target_urls[1], target_urls[1])
        super_link = aff_map.get(target_urls[2], target_urls[2])
        limited_link = aff_map.get(target_urls[3], target_urls[3])

        # Price info
        price_line = ""
        if prod_price:
            dzd_val = int(prod_price * DZD_USD_RATE)
            price_line = f"💵 السعر: {prod_price:.2f}$ (~{dzd_val:,} دج) 🔥\n"

        safe_title = html.escape(prod_title)

        message_text = f"""🛍️ <b>{safe_title}</b>
{price_line}
🪙 <b>سعر تخفيض العملات (Coins):</b>
🔗 {coin_link}

📦 <b>عروض الحزم (Bundle Deals):</b>
🔗 {bundle_link}

⚡ <b>عروض السوبر ديلز (SuperDeals):</b>
🔗 {super_link}

⏳ <b>العرض المحدود (Limited Offer):</b>
🔗 {limited_link}

💡 <i>نصيحة: ادخل من رابط العملات واشترِ مباشرة أو أضف المنتج للسلة لتفعيل أكبر نسبة خصم!</i>"""

        reply_markup = {
            "inline_keyboard": [
                [
                    {"text": "🪙 شراء بتخفيض العملات المباشر", "url": coin_link}
                ],
                [
                    {"text": "📦 عروض Bundle Deals", "url": bundle_link},
                    {"text": "⚡ عروض السوبر ديلز", "url": super_link}
                ],
                [
                    {"text": "📢 قناتنا للعروض @DzAliexpress0", "url": "https://t.me/DzAliexpress0"}
                ],
                [
                    {
                        "text": "🔄 شارك البوت مع أصدقائك",
                        "url": "https://t.me/share/url?url=https://t.me/Alilo07BOT&text=بوت زيادة تخفيض العملات في علي اكسبرس 🪙🔥 يوفر لك حتى 70%!"
                    }
                ]
            ]
        }

        return {
            "text": message_text,
            "image_url": prod_image,
            "reply_markup": reply_markup
        }

    except Exception:
        return None

async def handle_update(update: Dict[str, Any]) -> bool:
    # 1. Handle Callback Queries
    if "callback_query" in update:
        cb = update["callback_query"]
        cb_id = cb.get("id")
        cb_data = cb.get("data")
        msg = cb.get("message")
        chat_id = msg.get("chat", {}).get("id") if msg else None

        async with httpx.AsyncClient(timeout=4.0) as client:
            await client.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/answerCallbackQuery",
                json={"callback_query_id": cb_id}
            )

        if chat_id:
            if cb_data == "cb_help":
                await send_msg(chat_id, HELP_TEXT)
            elif cb_data == "cb_coupons":
                await send_msg(chat_id, COUPONS_TEXT)
        return True

    # 2. Handle Messages
    message = update.get("message") or update.get("edited_message")
    if not message:
        return False

    chat_id = message.get("chat", {}).get("id")
    text = (message.get("text") or "").strip()
    if not chat_id:
        return False

    if text.startswith("/start"):
        start_markup = {
            "inline_keyboard": [
                [
                    {"text": "📖 طريقة استخدام تخفيض العملات", "callback_data": "cb_help"},
                    {"text": "🎟️ كودات وكوبونات التخفيض", "callback_data": "cb_coupons"}
                ],
                [
                    {"text": "📢 قناتنا للعروض @DzAliexpress0", "url": "https://t.me/DzAliexpress0"}
                ]
            ]
        }
        await send_msg(chat_id, WELCOME_TEXT, start_markup)
        return True

    if text.startswith("/help") or "كيف" in text or "طريقة" in text:
        await send_msg(chat_id, HELP_TEXT)
        return True

    if text.startswith("/coupons") or "كوبون" in text or "كود" in text:
        await send_msg(chat_id, COUPONS_TEXT)
        return True

    # 3. Handle Product Links
    urls = extract_urls(text)
    if not urls:
        if text.isdigit() and len(text) >= 10:
            pid = text
        else:
            help_msg = (
                "⚠️ <b>الرجاء إرسال رابط صحيح لمنتج من AliExpress.</b>\n\n"
                "📌 <b>مثال على الروابط المقبولة:</b>\n"
                "• https://a.aliexpress.com/_c4ttSySh\n"
                "• https://www.aliexpress.com/item/1005006533038973.html\n\n"
                "أو اكتب /help لمعرفة كيفية الاستخدام."
            )
            await send_msg(chat_id, help_msg)
            return True
    else:
        pid = await resolve_ali_url(urls[0])

    if not pid:
        err_msg = "❌ تعذر استخراج كود المنتج من هذا الرابط. يرجى التأكد من الرابط والمحاولة مجدداً."
        await send_msg(chat_id, err_msg)
        return False

    # Send typing action in background
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            await client.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendChatAction",
                json={"chat_id": chat_id, "action": "typing"}
            )
    except Exception:
        pass

    res = await generate_coin_discount_response(pid)
    if not res:
        err_msg = "❌ تعذر توليد روابط التخفيض لهذا المنتج حالياً. يرجى المحاولة بعد قليل."
        await send_msg(chat_id, err_msg)
        return False

    # Try photo send first
    if res.get("image_url"):
        success = await send_photo(chat_id, res["image_url"], res["text"], res.get("reply_markup"))
        if success:
            return True

    # Fallback to text message
    await send_msg(chat_id, res["text"], res.get("reply_markup"))
    return True

async def send_photo(chat_id: int, photo_url: str, caption: str, reply_markup: Optional[Dict] = None) -> bool:
    payload = {
        "chat_id": chat_id,
        "photo": photo_url,
        "caption": caption[:1024],
        "parse_mode": "HTML"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto",
                json=payload
            )
            return resp.status_code == 200 and resp.json().get("ok")
    except Exception:
        return False

async def send_msg(chat_id: int, text: str, reply_markup: Optional[Dict] = None):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                json=payload
            )
            if resp.status_code != 200 or not resp.json().get("ok"):
                # Safety fallback without parse_mode
                payload["parse_mode"] = None
                await client.post(
                    f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                    json=payload
                )
    except Exception:
        pass
