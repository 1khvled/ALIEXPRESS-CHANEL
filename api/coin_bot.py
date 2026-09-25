"""
Bulletproof Serverless AliExpress Coin & Discount Bot for Vercel
Guaranteed Zero-Failure, Accurate Product Detection & Ultra-Fast:
- Works with ANY AliExpress link (desktop, mobile, shortlinks, share texts, raw IDs)
- Direct Product link (الرابط المباشر للمنتج) + Coin link + Bundle Deals + SuperDeals
- Full title & price extraction with generous timeout + fallback parser
- Live USDT exchange rate integration via SquareAlgerie.com (~249 DA)
- Advertisement and live rate badge for SquareAlgerie.com
- 100% Delivery guarantee (HTML mode with auto-fallback)
"""
import asyncio
import html
import os
import re
import time
from typing import Optional, Dict, Any, List, Tuple
from urllib.parse import urlparse, parse_qs
import httpx
from aliexpress_api import AliexpressApi, models

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8900887118:AAFuAFcxS1Xa2K4g0tlpD_YutPrsco3Y-Vo")
ALIEXPRESS_AFFILIATE_APP_KEY = os.getenv("ALIEXPRESS_AFFILIATE_APP_KEY", "538348")
ALIEXPRESS_AFFILIATE_APP_SECRET = os.getenv("ALIEXPRESS_AFFILIATE_APP_SECRET", "7z5QlJZAxNka2zBrgzCWrUNusBXJGHYx")
ALIEXPRESS_AFFILIATE_TRACKING_ID = os.getenv("ALIEXPRESS_AFFILIATE_TRACKING_ID", "dzkhvled16")
TARGET_CHANNEL_ID = os.getenv("TARGET_CHANNEL_ID", "@DzAliexpress0")

# Cache for SquareAlgerie live USDT rate
_CACHED_USDT_RATE = 249.0
_CACHED_USDT_TIME = 0.0

async def get_live_usdt_rate() -> float:
    """Fetches live USDT rate from SquareAlgerie.com with memory caching and 249.0 DA fallback."""
    global _CACHED_USDT_RATE, _CACHED_USDT_TIME
    now = time.time()
    if now - _CACHED_USDT_TIME < 1800.0 and _CACHED_USDT_RATE > 0:
        return _CACHED_USDT_RATE

    try:
        async with httpx.AsyncClient(timeout=2.5) as client:
            resp = await client.get("https://squarealgerie.com/api/rates")
            if resp.status_code == 200:
                data = resp.json()
                for c in data.get("currencies", []):
                    if c.get("code") == "USDT" and c.get("buy"):
                        rate = float(c["buy"])
                        if 220.0 <= rate <= 280.0:
                            _CACHED_USDT_RATE = rate
                            _CACHED_USDT_TIME = now
                            return _CACHED_USDT_RATE
    except Exception:
        pass

    _CACHED_USDT_RATE = 249.0
    _CACHED_USDT_TIME = now
    return _CACHED_USDT_RATE

WELCOME_TEXT = """👋 <b>مرحباً بك في بوت DealScoutDz لزيادة تخفيض العملات!</b> 🪙

هذا البوت يعمل على <b>زيادة نسبة التخفيض بالعملات (النقاط)</b> من 1%~5% إلى نسبة عالية تصل حتى <b>70%</b> في معظم منتجات AliExpress 🤑

📌 <b>طريقة الاستخدام بكل بساطة:</b>
1️⃣ انسخ رابط أي منتج تريده من تطبيق أو موقع AliExpress.
2️⃣ أرسل الرابط هنا في المحادثة.
3️⃣ سيرسل لك البوت فوراً روابط التخفيض الأكبر (تخفيض العملات، Bundle Deals، السوبر ديلز، والرابط المباشر) مع السعر المباشر بالدينار الجزائري! 🚀

📊 أسعار الصرف الحية مقدمة لكم بشراكة مع: <a href="https://squarealgerie.com">SquareAlgerie.com</a> 🇩🇿"""

HELP_TEXT = """💡 <b>دليل استخدام تخفيض العملات بأقصى نسبة:</b>

1️⃣ <b>كيف تفعل الخصم الأكبر؟</b>
عند فتح رابط العملات، لا تشترِ من الصفحة العادية! اضغط على زر <b>"شراء الآن"</b> مباشرة من صفحة العملات، أو أضف المنتج إلى السلة من داخل صفحة العملات لتخصم لك كل النقاط المتاحة.

2️⃣ <b>تحويل الدولة إلى كوريا 🇰🇷:</b>
لا تنسى تحويل دولة التطبيق إلى كوريا 🇰🇷 📍 من إعدادات AliExpress للحصول على أسعار أقل وتخفيض عملات إضافي على الكثير من الأجهزة والعتاد!

3️⃣ <b>كيف تجمع العملات يومياً؟</b>
ادخل يومياً لتطبيق AliExpress واضغط على أيقونة <b>Coins / العملات</b> واجمع العملات المجانية اليومية (يمكنك جمع 70 إلى 150 عملة يومياً مجاناً).

4️⃣ <b>أسعار الصرف في الجزائر:</b>
تابع أسعار صرف السكوار والـ USDT لحظة بلحظة عبر: <a href="https://squarealgerie.com">SquareAlgerie.com</a> 🇩🇿

📢 للمزيد من العروض اليومية، انضم لقناتنا: @DzAliexpress0"""

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

📢 تابع قناتنا للمزيد: @DzAliexpress0"""

URL_REGEX = re.compile(r'(https?://[^\s<>"\',;]+)', re.IGNORECASE)

def extract_urls(text: str) -> List[str]:
    if not text:
        return []
    urls = URL_REGEX.findall(text)
    return [u.rstrip(".,;!?:)]}\"'>") for u in urls if u.startswith("http")]

def extract_pid_from_string(text: str) -> Optional[str]:
    """Instant regex extraction of AliExpress product ID from any string or URL."""
    if not text:
        return None
    clean = text.strip()
    if clean.isdigit() and len(clean) >= 10:
        return clean
    m = re.search(r'/item/(\d+)', text, re.IGNORECASE)
    if m:
        return m.group(1)
    m = re.search(r'productIds?=(\d+)', text, re.IGNORECASE)
    if m:
        return m.group(1)
    m = re.search(r'(?:itemId|item_id|productId|product_id|id)=(\d+)', text, re.IGNORECASE)
    if m:
        return m.group(1)
    return None

def extract_title_and_price_from_user_text(text: str) -> Tuple[Optional[str], Optional[float]]:
    """Extracts product title and price if user shared directly from AliExpress mobile app."""
    if not text:
        return None, None
    cleaned = re.sub(r'https?://\S+', '', text)
    # Price
    price = None
    m_price = re.search(r'(?:US\s*)?\$?\s*([0-9]+[.,][0-9]{1,2})\s*\$?', cleaned, re.IGNORECASE)
    if m_price:
        try:
            price = float(m_price.group(1).replace(',', '.'))
        except Exception:
            pass

    # Title
    cleaned = re.sub(r'(?:US\s*)?\$?\s*[0-9]+[.,][0-9]{1,2}\s*\$?', '', cleaned)
    cleaned = re.sub(
        r'Just found this amazing item on AliExpress\.?|Check it out!?|لقيت هذا المنتج|شوف هذا العرض|علي اكسبرس|AliExpress',
        '',
        cleaned,
        flags=re.IGNORECASE
    )
    cleaned = re.sub(r'[|؛:,\-_~]+', ' ', cleaned).strip()
    title = cleaned[:90] if len(cleaned) >= 8 else None
    return title, price

async def resolve_any_ali_link(text: str) -> Optional[str]:
    """
    Bulletproof resolver for ANY AliExpress link:
    - Desktop URLs
    - Mobile app share messages with surrounding text
    - a.aliexpress.com shortlinks
    - s.click.aliexpress.com shortlinks
    - star.aliexpress.com share links
    - Raw product IDs
    """
    # 1. Check if PID is already in the text or URL directly (instant 0ms)
    pid = extract_pid_from_string(text)
    if pid:
        return pid

    urls = extract_urls(text)
    if not urls:
        return None

    raw_url = urls[0]
    pid = extract_pid_from_string(raw_url)
    if pid and "s.click" not in raw_url and "a.aliexpress" not in raw_url and "star.aliexpress" not in raw_url:
        return pid

    # 2. Fast 1-hop / 2-hop 302 Location header check (super fast, no body download)
    try:
        async with httpx.AsyncClient(timeout=3.5, follow_redirects=False) as client:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            resp = await client.get(raw_url, headers=headers)
            loc = resp.headers.get("location") or resp.headers.get("Location")
            if loc:
                found = extract_pid_from_string(loc)
                if found:
                    return found
                # Hop 2
                if loc.startswith("http"):
                    resp2 = await client.get(loc, headers=headers, timeout=2.5)
                    loc2 = resp2.headers.get("location") or str(resp2.url)
                    found2 = extract_pid_from_string(loc2)
                    if found2:
                        return found2
            # Check body snippet if returned 200
            if resp.status_code == 200 and resp.text:
                found = extract_pid_from_string(resp.text[:5000])
                if found:
                    return found
    except Exception:
        pass

    return extract_pid_from_string(raw_url)

async def generate_coin_discount_response(product_id: str, raw_user_text: str = "") -> Dict[str, Any]:
    """
    Guaranteed Zero-Failure generator with generous timeout for AliExpress API
    and fallback to user share text title/price.
    """
    usdt_rate = await get_live_usdt_rate()

    fallback_title, fallback_price = extract_title_and_price_from_user_text(raw_user_text)

    # Base direct links
    direct_product = f"https://www.aliexpress.com/item/{product_id}.html"
    direct_coin = f"https://m.aliexpress.com/p/coin-index/index.html?productIds={product_id}"
    direct_bundle = f"https://www.aliexpress.com/ssr/300000512/BundleDeals2?productIds={product_id}"
    direct_super = f"https://www.aliexpress.com/item/{product_id}.html?sourceType=680"
    direct_limited = f"https://www.aliexpress.com/item/{product_id}.html?sourceType=562"

    target_urls = [direct_product, direct_coin, direct_bundle]

    prod_title = fallback_title or "منتج مميز من AliExpress"
    prod_price = fallback_price
    prod_image = None
    product_link = direct_product
    coin_link = direct_coin
    bundle_link = direct_bundle
    super_link = direct_super
    limited_link = direct_limited

    # Try AliExpress Open Platform API with generous timeout
    try:
        api = AliexpressApi(
            ALIEXPRESS_AFFILIATE_APP_KEY,
            ALIEXPRESS_AFFILIATE_APP_SECRET,
            models.Language.EN,
            models.Currency.USD,
            ALIEXPRESS_AFFILIATE_TRACKING_ID
        )

        # 1. Fetch details (generous 4.5s timeout with retry)
        for attempt in range(2):
            try:
                details = await asyncio.wait_for(
                    asyncio.to_thread(api.get_products_details, str(product_id)),
                    timeout=4.5
                )
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
                    break
            except Exception:
                await asyncio.sleep(0.2)

        # 2. Fetch s.click affiliate links
        try:
            raw_links = await asyncio.wait_for(
                asyncio.to_thread(api.get_affiliate_links, ",".join(target_urls)),
                timeout=3.5
            )
            if raw_links:
                aff_map = {}
                for item in raw_links:
                    orig = getattr(item, 'source_value', '')
                    promo = getattr(item, 'promotion_link', '')
                    if orig and promo:
                        aff_map[orig] = promo
                product_link = aff_map.get(direct_product, direct_product)
                coin_link = aff_map.get(direct_coin, direct_coin)
                bundle_link = aff_map.get(direct_bundle, direct_bundle)
                # Build SuperDeals and Limited from affiliate product link if available
                if product_link != direct_product and "s.click" in product_link:
                    super_link = product_link
                    limited_link = product_link
        except Exception:
            pass

    except Exception:
        pass

    price_line = ""
    if prod_price:
        dzd_val = int(prod_price * usdt_rate)
        price_line = f"💵 السعر: <b>{prod_price:.2f}$</b> (~<b>{dzd_val:,} دج</b>)\n(سعر الصرف 1 USDT ≈ {int(usdt_rate)} دج عبر SquareAlgerie.com)\n"

    safe_title = html.escape(prod_title)

    message_text = f"""🛍️ <b>{safe_title}</b>
{price_line}
🛒 <b>الرابط المباشر للمنتج:</b>
🔗 {product_link}

🪙 <b>سعر تخفيض العملات (Coins):</b>
🔗 {coin_link}

📦 <b>عروض الحزم (Bundle Deals):</b>
🔗 {bundle_link}

⚡ <b>عروض السوبر ديلز (SuperDeals):</b>
🔗 {super_link}

⏳ <b>العرض المحدود (Limited Offer):</b>
🔗 {limited_link}

💡 <i>نصيحة: ادخل من رابط العملات واشترِ مباشرة أو أضف المنتج للسلة لتفعيل أكبر نسبة خصم!</i>

📊 <i>أسعار الصرف مقدمة من:</i> <a href="https://squarealgerie.com">SquareAlgerie.com</a> 🇩🇿"""

    reply_markup = {
        "inline_keyboard": [
            [
                {"text": "🛒 رابط الشراء المباشر", "url": product_link},
                {"text": "🪙 شراء بتخفيض العملات", "url": coin_link}
            ],
            [
                {"text": "📦 عروض Bundle Deals", "url": bundle_link},
                {"text": "⚡ عروض السوبر ديلز", "url": super_link}
            ],
            [
                {"text": "📈 أسعار الصرف الحية SquareAlgerie.com 🇩🇿", "url": "https://squarealgerie.com"}
            ],
            [
                {"text": "📢 قناتنا للعروض @DzAliexpress0", "url": "https://t.me/DzAliexpress0"},
                {
                    "text": "🔄 مشاركة البوت",
                    "url": "https://t.me/share/url?url=https://t.me/Alilo07BOT&text=بوت زيادة تخفيض العملات في علي اكسبرس 🪙🔥 يوفر حتى 70%!"
                }
            ]
        ]
    }

    return {
        "text": message_text,
        "image_url": prod_image,
        "reply_markup": reply_markup
    }

async def handle_update(update: Dict[str, Any]) -> bool:
    # 1. Handle Callback Queries
    if "callback_query" in update:
        cb = update["callback_query"]
        cb_id = cb.get("id")
        cb_data = cb.get("data")
        msg = cb.get("message")
        chat_id = msg.get("chat", {}).get("id") if msg else None

        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                await client.post(
                    f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/answerCallbackQuery",
                    json={"callback_query_id": cb_id}
                )
        except Exception:
            pass

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
                    {"text": "📈 أسعار الصرف الحية SquareAlgerie.com 🇩🇿", "url": "https://squarealgerie.com"}
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

    # 3. Resolve Product ID from ANY AliExpress Link or Text
    pid = await resolve_any_ali_link(text)
    if not pid:
        help_msg = (
            "⚠️ <b>الرجاء إرسال رابط صحيح لمنتج من AliExpress.</b>\n\n"
            "📌 <b>يدعم البوت جميع الروابط:</b>\n"
            "• روابط التطبيق: <code>https://a.aliexpress.com/_xxxx</code>\n"
            "• روابط المتصفح: <code>https://aliexpress.com/item/100500...html</code>\n"
            "• كود المنتج مباشرة: <code>1005007458498882</code>\n\n"
            "💡 أو اكتب /help لمعرفة كيفية الاستخدام."
        )
        await send_msg(chat_id, help_msg)
        return True

    # Send typing action in background
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            await client.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendChatAction",
                json={"chat_id": chat_id, "action": "typing"}
            )
    except Exception:
        pass

    # Guaranteed response generation with raw text fallback
    res = await generate_coin_discount_response(pid, raw_user_text=text)

    # Send with photo if available, fallback to text
    if res.get("image_url"):
        success = await send_photo(chat_id, res["image_url"], res["text"], res.get("reply_markup"))
        if success:
            return True

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
                payload["parse_mode"] = None
                await client.post(
                    f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                    json=payload
                )
    except Exception:
        pass
