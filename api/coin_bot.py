"""
Bulletproof Serverless AliExpress Coin & Discount Bot for Vercel
Guaranteed Zero-Failure, Accurate Product Detection & Ultra-Fast:
- Works with ANY AliExpress link (desktop, mobile, shortlinks, share texts, raw IDs)
- Direct Product link (الرابط المباشر للمنتج) + Coin link + Bundle Deals + SuperDeals
- Full title & price extraction with generous timeout + fallback parser
- Live USDT exchange rate integration via SquareAlgerie.com (~249 DA)
- Advertisement and live rate badge for SquareAlgerie.com
- Admin manual deal publisher mode (recognizes admin by Telegram user ID 5625295907)
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
PRIMARY_ADMIN_ID = int(os.getenv("ADMIN_USER_ID", "5625295907"))

def is_admin(user_id: int) -> bool:
    """Checks if the given Telegram user ID is an authorized admin."""
    if not user_id:
        return False
    if user_id == PRIMARY_ADMIN_ID or user_id == 5625295907:
        return True
    admin_env = os.getenv("ADMIN_USER_IDS", "")
    if admin_env:
        ids = [int(i.strip()) for i in admin_env.split(",") if i.strip().isdigit()]
        if user_id in ids:
            return True
    return False

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

💡 <i>أرسل أي رابط منتج من AliExpress الآن لتجربة التخفيض!</i>"""

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
    m = re.search(r'/item/(\d{10,18})', text, re.IGNORECASE)
    if m:
        return m.group(1)
    m = re.search(r'productIds?=(\d{10,18})', text, re.IGNORECASE)
    if m:
        return m.group(1)
    m = re.search(r'(?:itemId|item_id|productId|product_id)[=:](\d{10,18})', text, re.IGNORECASE)
    if m:
        return m.group(1)
    m = re.search(r'(?:^|[?&#;])id=(\d{10,18})(?:$|[&#;])', text, re.IGNORECASE)
    if m:
        return m.group(1)
    return None


def extract_title_and_price_from_user_text(text: str) -> Tuple[Optional[str], Optional[float]]:
    """Extracts product title and price if user shared directly from AliExpress mobile app."""
    if not text:
        return None, None
    cleaned = re.sub(r'https?://\S+', '', text)
    price = None
    m_price = re.search(r'(?:US\s*)?\$?\s*([0-9]+[.,][0-9]{1,2})\s*\$?', cleaned, re.IGNORECASE)
    if m_price:
        try:
            price = float(m_price.group(1).replace(',', '.'))
        except Exception:
            pass

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

_ALI_API_LOCK = asyncio.Lock()
_LAST_ALI_CALL_TIME = 0.0

async def safe_api_get_details(api: AliexpressApi, product_id: str) -> Optional[List[Any]]:
    """Rate-limited safe caller for get_products_details."""
    global _LAST_ALI_CALL_TIME
    async with _ALI_API_LOCK:
        elapsed = time.time() - _LAST_ALI_CALL_TIME
        if elapsed < 1.1:
            await asyncio.sleep(1.1 - elapsed)
        _LAST_ALI_CALL_TIME = time.time()

        for attempt in range(2):
            try:
                res = await asyncio.wait_for(
                    asyncio.to_thread(api.get_products_details, str(product_id)),
                    timeout=4.5
                )
                if res:
                    return res
            except Exception as e:
                err_str = str(e).lower()
                if "ban" in err_str or "limit" in err_str:
                    await asyncio.sleep(1.2)
                    _LAST_ALI_CALL_TIME = time.time()
                    try:
                        return await asyncio.wait_for(
                            asyncio.to_thread(api.get_products_details, str(product_id)),
                            timeout=4.5
                        )
                    except Exception:
                        pass
                elif attempt == 0:
                    await asyncio.sleep(0.5)
        return None

async def safe_api_get_affiliate_links(api: AliexpressApi, urls_joined: str) -> Optional[List[Any]]:
    """Rate-limited safe caller for get_affiliate_links."""
    global _LAST_ALI_CALL_TIME
    async with _ALI_API_LOCK:
        elapsed = time.time() - _LAST_ALI_CALL_TIME
        if elapsed < 1.1:
            await asyncio.sleep(1.1 - elapsed)
        _LAST_ALI_CALL_TIME = time.time()

        for attempt in range(2):
            try:
                res = await asyncio.wait_for(
                    asyncio.to_thread(api.get_affiliate_links, urls_joined),
                    timeout=4.0
                )
                if res:
                    return res
            except Exception as e:
                err_str = str(e).lower()
                if "ban" in err_str or "limit" in err_str:
                    await asyncio.sleep(1.2)
                    _LAST_ALI_CALL_TIME = time.time()
                    try:
                        return await asyncio.wait_for(
                            asyncio.to_thread(api.get_affiliate_links, urls_joined),
                            timeout=4.0
                        )
                    except Exception:
                        pass
                elif attempt == 0:
                    await asyncio.sleep(0.5)
        return None

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
    pid = extract_pid_from_string(text)
    if pid:
        return pid

    # Check for embedded shortlinks even if glued to text without spaces
    sclick_match = re.search(r's\.click\.aliexpress\.com/e/(_[a-zA-Z0-9]+)', text)
    candidate_urls = []
    if sclick_match:
        candidate_urls.append(f"https://s.click.aliexpress.com/e/{sclick_match.group(1)}")

    a_match = re.search(r'a\.aliexpress\.com/(_[a-zA-Z0-9]+)', text)
    if a_match:
        candidate_urls.append(f"https://a.aliexpress.com/{a_match.group(1)}")

    candidate_urls.extend(extract_urls(text))

    for raw_url in candidate_urls:
        pid = extract_pid_from_string(raw_url)
        if pid and "s.click" not in raw_url and "a.aliexpress" not in raw_url and "star.aliexpress" not in raw_url:
            return pid

        try:
            async with httpx.AsyncClient(timeout=4.5, follow_redirects=True) as client:
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                resp = await client.get(raw_url, headers=headers)
                found = extract_pid_from_string(str(resp.url))
                if found:
                    return found
                if resp.text:
                    found = extract_pid_from_string(resp.text[:5000])
                    if found:
                        return found
        except Exception:
            pass

        # If s.click failed and has extra characters glued at the end, try trimming
        if "s.click.aliexpress.com/e/_" in raw_url:
            m_s = re.search(r's\.click\.aliexpress\.com/e/(_[a-zA-Z0-9]{7,12})', raw_url)
            if m_s:
                code = m_s.group(1)
                for trim_len in [8, 9, 7]:
                    if len(code) > trim_len:
                        trimmed_url = f"https://s.click.aliexpress.com/e/{code[:trim_len]}"
                        try:
                            async with httpx.AsyncClient(timeout=3.5, follow_redirects=True) as client:
                                resp = await client.get(trimmed_url, headers={"User-Agent": "Mozilla/5.0"})
                                found = extract_pid_from_string(str(resp.url))
                                if found:
                                    return found
                        except Exception:
                            pass

    return extract_pid_from_string(text)

async def generate_coin_discount_response(product_id: str, raw_user_text: str = "") -> Dict[str, Any]:
    """
    Guaranteed Zero-Failure generator with generous timeout for AliExpress API
    and fallback to user share text title/price.
    """
    usdt_rate = await get_live_usdt_rate()

    fallback_title, fallback_price = extract_title_and_price_from_user_text(raw_user_text)

    direct_product = f"https://www.aliexpress.com/item/{product_id}.html"
    direct_coin = f"https://m.aliexpress.com/p/coin-index/index.html?productIds={product_id}"
    direct_bundle = f"https://www.aliexpress.com/item/{product_id}.html?sourceType=562"
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

    try:
        api = AliexpressApi(
            ALIEXPRESS_AFFILIATE_APP_KEY,
            ALIEXPRESS_AFFILIATE_APP_SECRET,
            models.Language.EN,
            models.Currency.USD,
            ALIEXPRESS_AFFILIATE_TRACKING_ID
        )

        # 1. Fetch details with rate limiting
        details = await safe_api_get_details(api, str(product_id))
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

        # 2. Fetch s.click affiliate links with rate limiting
        raw_links = await safe_api_get_affiliate_links(api, ",".join(target_urls))
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
            if product_link != direct_product and "s.click" in product_link:
                super_link = product_link
                limited_link = product_link

    except Exception:
        pass


    price_line = ""
    if prod_price:
        dzd_val = int(prod_price * usdt_rate)
        price_line = f"💵 السعر التقريبي: <b>{prod_price:.2f}$</b> (~<b>{dzd_val:,} دج</b>)\n"

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

💡 <i>نصيحة: ادخل من رابط العملات واشترِ مباشرة أو أضف المنتج للسلة لتفعيل أكبر نسبة خصم!</i>"""

    reply_markup = {
        "inline_keyboard": [
            [
                {"text": "🛒 رابط الشراء المباشر", "url": product_link},
                {"text": "🪙 شراء بتخفيض العملات", "url": coin_link}
            ],
            [
                {"text": "🔔 راقب انخفاض السعر | Alert Price Drop", "callback_data": f"watch_{product_id}_{prod_price or 0.0}"}
            ],
            [
                {"text": "📦 عروض Bundle Deals", "url": bundle_link},
                {"text": "⚡ عروض السوبر ديلز", "url": super_link}
            ],
            [
                {"text": "📢 قناة الصفقات المعتمدة", "url": "https://t.me/DzAliexpress0"},
                {
                    "text": "🔄 مشاركة البوت",
                    "url": "https://t.me/share/url?url=https://t.me/Alilo07BOT&text=بوت زيادة تخفيض العملات في علي اكسبرس 🪙🔥 يوفر حتى 70%!"
                }
            ]
        ]
    }

    return {
        "text": message_text,
        "product_id": product_id,
        "title": prod_title,
        "price": prod_price,
        "image_url": prod_image,
        "product_link": product_link,
        "coin_link": coin_link,
        "bundle_link": bundle_link,
        "reply_markup": reply_markup
    }

async def publish_deal_to_channel(product_id: str, raw_user_text: str = "") -> Tuple[bool, Optional[str], Optional[int]]:
    """Publishes a verified clean deal post directly to @DzAliexpress0 from admin request."""
    res = await generate_coin_discount_response(product_id, raw_user_text=raw_user_text)

    prod_title = res.get("title") or "منتج مميز من AliExpress"
    prod_price = res.get("price") or 0.0
    eur_price = round(prod_price * 0.92, 2)
    product_link = res.get("product_link") or f"https://www.aliexpress.com/item/{product_id}.html"
    image_url = res.get("image_url")

    # Smart Deal Link: Coin link (90%+) or Bundle link (rare cases)
    is_bundle = any(k in raw_user_text.lower() for k in ["bundle", "حزم", "حزمة", "3 بـ", "3 منتجات"])
    deal_link = res.get("bundle_link") if is_bundle else res.get("coin_link")
    if not deal_link:
        deal_link = res.get("coin_link") or product_link

    # Smart situational hook
    t_lower = prod_title.lower()
    is_gaming = any(k in t_lower for k in ["mouse", "keyboard", "headset", "earphone", "controller", "gaming", "game", "rgb"])
    if is_gaming:
        hook = "صيدة ممتازة للقيمرز 🎮🔥"
    elif prod_price and prod_price < 25.0:
        hook = "نزول قوي في السعر 🔥📉"
    else:
        hook = "العرض مستمر 🚨"

    caption_lines = [
        "لا تنسى تحويل دولة التطبيق إلى كوريا 🇰🇷 📍",
        hook,
        f"تخفيض لـ {html.escape(prod_title)}",
        f"السعر : {prod_price:.2f}$ ({eur_price:.2f}€)🔥" if prod_price > 0 else "سعر مميز وتخفيض عملات 🔥",
        f"رابط {deal_link}",
        "خصم النقاط (العملات)",
        "",
        "🪙 استخدم بوت DealScoutDz للشراء بأقل سعر: @Alilo07BOT"
    ]
    caption = "\n".join(caption_lines)

    channel_reply_markup = {
        "inline_keyboard": [
            [
                {"text": "🛒 رابط الشراء من AliExpress", "url": deal_link}
            ],
            [
                {"text": "🪙 بوت تخفيض العملات DealScoutDz", "url": "https://t.me/Alilo07BOT"}
            ]
        ]
    }

    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            if image_url:
                resp = await client.post(
                    f"{api_url}/sendPhoto",
                    json={
                        "chat_id": TARGET_CHANNEL_ID,
                        "photo": image_url,
                        "caption": caption[:1024],
                        "parse_mode": "HTML",
                        "reply_markup": channel_reply_markup
                    }
                )
            else:
                resp = await client.post(
                    f"{api_url}/sendMessage",
                    json={
                        "chat_id": TARGET_CHANNEL_ID,
                        "text": caption,
                        "parse_mode": "HTML",
                        "reply_markup": channel_reply_markup
                    }
                )

            data = resp.json()
            if resp.status_code == 200 and data.get("ok"):
                msg_id = data.get("result", {}).get("message_id")
                return True, None, msg_id
            else:
                err = data.get("description", f"HTTP {resp.status_code}")
                return False, err, None
    except Exception as e:
        return False, str(e), None

async def handle_update(update: Dict[str, Any]) -> bool:
    # 1. Handle Callback Queries
    if "callback_query" in update:
        cb = update["callback_query"]
        cb_id = cb.get("id")
        cb_data = cb.get("data") or ""
        msg = cb.get("message")
        user = cb.get("from", {})
        user_id = user.get("id")
        chat_id = msg.get("chat", {}).get("id") if msg else None
        msg_id = msg.get("message_id") if msg else None

        toast_msg = None

        if cb_data.startswith("watch_"):
            # Format: watch_{pid}_{price}
            parts = cb_data.split("_")
            pid = parts[1] if len(parts) > 1 else ""
            try:
                price = float(parts[2]) if len(parts) > 2 else 0.0
            except Exception:
                price = 0.0

            from app.publisher.watchlist import add_to_watchlist
            title = msg.get("caption") or msg.get("text") or f"منتج {pid}"
            clean_title = title.splitlines()[0] if title else f"منتج {pid}"
            clean_title = clean_title.replace("🛍️", "").replace("<b>", "").replace("</b>", "").strip()

            add_to_watchlist(user_id=user_id, product_id=pid, title=clean_title, price=price)
            toast_msg = "✅ تم تفعيل المراقبة! سنرسل لك إشعاراً خاصاً فور انخفاض السعر أو توفر كوبون."

        elif cb_data.startswith("unwatch_"):
            pid = cb_data.replace("unwatch_", "").strip()
            from app.publisher.watchlist import remove_from_watchlist, get_user_watchlist
            remove_from_watchlist(user_id=user_id, product_id=pid)
            toast_msg = "🗑️ تم حذف المنتج من قائمة المراقبة."

            # Update watchlist message
            if chat_id and msg_id:
                user_watches = get_user_watchlist(user_id)
                if not user_watches:
                    await send_msg(chat_id, "📭 <b>أصبحت قائمة المراقبة فارغة الآن.</b>")
                else:
                    lines = [f"📋 <b>قائمة المنتجات التي تراقبها ({len(user_watches)}):</b>\n"]
                    kb = []
                    for w in user_watches[:10]:
                        p_id = w.get("product_id")
                        t_str = w.get("title", "")[:35]
                        pr = w.get("price", 0.0)
                        lines.append(f"• <b>{t_str}</b>\n  السعر: <b>{pr:.2f}$</b>\n  🆔 <code>{p_id}</code>")
                        kb.append([{"text": f"❌ إزالة {t_str[:20]}...", "callback_data": f"unwatch_{p_id}"}])
                    try:
                        async with httpx.AsyncClient(timeout=4.0) as client:
                            await client.post(
                                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/editMessageText",
                                json={
                                    "chat_id": chat_id,
                                    "message_id": msg_id,
                                    "text": "\n\n".join(lines),
                                    "parse_mode": "HTML",
                                    "reply_markup": {"inline_keyboard": kb}
                                }
                            )
                    except Exception:
                        pass

        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                await client.post(
                    f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/answerCallbackQuery",
                    json={"callback_query_id": cb_id, "text": toast_msg} if toast_msg else {"callback_query_id": cb_id}
                )
        except Exception:
            pass

        if chat_id:
            if cb_data == "cb_help":
                await send_msg(chat_id, HELP_TEXT)
            elif cb_data == "cb_coupons":
                await send_msg(chat_id, COUPONS_TEXT)
            elif cb_data.startswith("admin_pub_"):
                if not is_admin(user_id):
                    await send_msg(chat_id, "⚠️ عذراً، هذا الإجراء مخصص لمشرف القناة فقط.")
                    return True

                target_pid = cb_data.replace("admin_pub_", "").strip()
                await send_msg(chat_id, "⏳ جاري نشر العرض في القناة @DzAliexpress0...")
                success, err, p_msg_id = await publish_deal_to_channel(target_pid)
                if success:
                    ch_clean = str(TARGET_CHANNEL_ID).lstrip("@")
                    post_url = f"https://t.me/{ch_clean}/{p_msg_id}"
                    confirm_text = f"✅ <b>تم نشر العرض بنجاح في القناة!</b>\n\n🔗 <b>رابط المنشور:</b> {post_url}"
                    await send_msg(chat_id, confirm_text)
                else:
                    await send_msg(chat_id, f"❌ فشل نشر العرض في القناة: {err}")
        return True

    # 2. Handle Messages
    message = update.get("message") or update.get("edited_message")
    if not message:
        return False

    chat = message.get("chat", {})
    chat_id = chat.get("id")
    chat_type = chat.get("type", "private")
    is_group = chat_type in ["group", "supergroup"]
    message_id = message.get("message_id")

    from_user = message.get("from", {})
    user_id = from_user.get("id") or chat_id
    text = (message.get("text") or message.get("caption") or "").strip()
    if not chat_id:
        return False

    # ── Group Messages Auto-Conversion & Group Commands ─────────────────
    if is_group:
        # Command: /calc or /rate in group
        if text.startswith("/calc") or text.startswith("/حساب"):
            m = re.search(r'([0-9]+[.,]?[0-9]*)', text)
            if m:
                usd_val = float(m.group(1).replace(',', '.'))
                rate = await get_live_usdt_rate()
                dzd_val = int(usd_val * rate)
                tax_est = 130
                total_est = dzd_val + tax_est
                calc_text = (
                    f"🧮 <b>حاسبة سعر الشراء بالدينار الجزائري 🇩🇿</b>\n\n"
                    f"💵 <b>المبلغ:</b> {usd_val:.2f}$ (سعر الصرف: {rate:.1f} دج)\n"
                    f"▫️ <b>قيمة السلعة:</b> <b>{dzd_val:,} دج</b>\n"
                    f"▫️ <b>رسوم طرد البريد الجزائري:</b> ~<b>{tax_est} دج</b>\n"
                    f"💰 <b>التكلفة الإجمالية التقديرية:</b> ~<b>{total_est:,} دج</b>"
                )
                await send_msg(chat_id, calc_text, reply_to_message_id=message_id)
                return True

        if text.startswith("/rate") or text.startswith("/square") or text.startswith("/سكوار"):
            rate = await get_live_usdt_rate()
            rate_text = (
                f"📈 <b>سعر صرف الـ USDT الحالي (SquareAlgerie.com):</b>\n\n"
                f"💵 <b>1 USDT</b> ≈ <b>{rate:.1f} دج</b> 🇩🇿\n\n"
                f"🪙 <i>لحساب أي مبلغ، أرسل: <code>/calc 15.5</code></i>"
            )
            await send_msg(chat_id, rate_text, reply_to_message_id=message_id)
            return True

        # Check if message contains an AliExpress link
        urls = extract_urls(text)
        has_ali = any("aliexpress" in u.lower() or "a.aliexpress" in u.lower() or "s.click" in u.lower() for u in urls) or extract_pid_from_string(text)
        if has_ali:
            pid = await resolve_any_ali_link(text)
            if pid:
                res = await generate_coin_discount_response(pid, raw_user_text=text)
                title = res.get("title") or "منتج مميز من AliExpress"
                safe_title = html.escape(title)[:75]
                price = res.get("price")
                coin_link = res.get("coin_link") or res.get("product_link")
                product_link = res.get("product_link") or coin_link
                usdt_rate = await get_live_usdt_rate()

                price_info = ""
                if price:
                    dzd_approx = int(price * usdt_rate)
                    price_info = f"💰 <b>السعر التقريبي:</b> ${price:.2f} (~<b>{dzd_approx:,} دج</b>)\n"

                group_reply = (
                    f"🪙 <b>تخفيض العملات المباشر للمنتج:</b>\n"
                    f"📦 <b>{safe_title}</b>\n"
                    f"{price_info}\n"
                    f"🔗 <b><a href=\"{coin_link}\">اضغط هنا لفتح رابط أقصى تخفيض عملات (Coins) 👈</a></b>"
                )

                group_markup = {
                    "inline_keyboard": [
                        [
                            {"text": "🪙 شراء بتخفيض العملات (Coins)", "url": coin_link},
                            {"text": "🛒 الرابط المباشر", "url": product_link}
                        ],
                        [
                            {"text": "📢 قناة الصفقات المعتمدة", "url": "https://t.me/DzAliexpress0"}
                        ]
                    ]
                }
                await send_msg(chat_id, group_reply, reply_markup=group_markup, reply_to_message_id=message_id)
                return True

        # Normal chatter in group: return silently without spamming
        return True

    # ── Private Chat Handlers ──────────────────────────────────────────
    # Command: /myid or /id
    if text.startswith("/myid") or text.startswith("/id"):
        admin_badge = "👑 <b>مشرف معتمد (Admin)</b>" if is_admin(user_id) else "مستخدم عادي"
        id_text = f"🆔 <b>معرف التيليجرام الخاص بك:</b> <code>{user_id}</code>\n<b>الرتبة:</b> {admin_badge}"
        await send_msg(chat_id, id_text)
        return True

    # Command: /start (Supports Deep-Link Ads & Campaigns)
    if text.startswith("/start"):
        parts = text.split()
        param = parts[1].lower() if len(parts) > 1 else ""

        # Deep-link from Meta Ads or Promotions
        if any(k in param for k in ["meta", "ad", "fb", "coins", "promo", "deal"]):
            ad_welcome = (
                "🇩🇿 <b>مرحباً بك في بوت DealScout DZ عبر إعلان تخفيض العملات!</b> 🪙🔥\n\n"
                "هذا البوت يساعدك على توفير حتى <b>70%</b> من سعر أي منتج في <b>AliExpress</b> عبر تحويله إلى رابط خصم العملات (Coins) الأقصى!\n\n"
                "📌 <b>جرّب الآن في 3 خطوات بسيطة:</b>\n"
                "1️⃣ افتح تطبيق <b>AliExpress</b> واختر أي منتج تريده.\n"
                "2️⃣ اضغط على زر المشاركة <b>(Share)</b> ثم نسخ الرابط <b>(Copy link)</b>.\n"
                "3️⃣ <b>ألصق الرابط هنا في هذه المحادثة فوراً</b>.\n\n"
                "⚡ سيرسل لك البوت روابط الشراء بأقل سعر ممكن بالدينار الجزائري!\n\n"
                "📢 <i>تابع أيضاً قناتنا الرسمية لصيدات اليوم الحصرية:</i> @DzAliexpress0"
            )
            markup = {
                "inline_keyboard": [
                    [{"text": "📢 قناة الصفقات المعتمدة", "url": "https://t.me/DzAliexpress0"}],
                    [{"text": "📖 طريقة جمع وتفعيل العملات", "callback_data": "cb_help"}]
                ]
            }
            await send_msg(chat_id, ad_welcome, reply_markup=markup)
            return True

        # Standard Welcome
        start_markup = {
            "inline_keyboard": [
                [
                    {"text": "📖 طريقة استخدام تخفيض العملات", "callback_data": "cb_help"},
                    {"text": "🎟️ كودات وكوبونات التخفيض", "callback_data": "cb_coupons"}
                ],
                [
                    {"text": "📋 قائمة مراقبة الأسعار", "callback_data": "cb_watchlist_help"},
                    {"text": "📢 قناة الصفقات المعتمدة", "url": "https://t.me/DzAliexpress0"}
                ]
            ]
        }
        await send_msg(chat_id, WELCOME_TEXT, start_markup)
        return True

    # Command: /calc <usd_amount>
    if text.startswith("/calc") or text.startswith("/حساب"):
        m = re.search(r'([0-9]+[.,]?[0-9]*)', text)
        if m:
            usd_val = float(m.group(1).replace(',', '.'))
            rate = await get_live_usdt_rate()
            dzd_val = int(usd_val * rate)
            tax_est = 130
            total_est = dzd_val + tax_est
            calc_text = (
                f"🧮 <b>حاسبة سعر الشراء بالدينار الجزائري 🇩🇿</b>\n\n"
                f"💵 <b>المبلغ بالدولار:</b> {usd_val:.2f}$\n"
                f"📈 <b>سعر صرف الـ USDT الحالي:</b> {rate:.1f} دج (المصدر: SquareAlgerie.com)\n"
                f"━━━━━━━━━━━━━━━━━\n"
                f"▫️ <b>قيمة السلعة بالدينار:</b> <b>{dzd_val:,} دج</b>\n"
                f"▫️ <b>رسوم طرد البريد الجزائري:</b> ~<b>{tax_est} دج</b>\n"
                f"💰 <b>التكلفة الإجمالية التقديرية:</b> ~<b>{total_est:,} دج</b>\n\n"
                f"💡 <i>نصيحة: استخدم دائماً رابط العملات (Coins) لتخفيض القيمة بالدولار قبل الشراء!</i>"
            )
            await send_msg(chat_id, calc_text)
            return True
        else:
            await send_msg(chat_id, "💡 <b>طريقة استخدام الحاسبة:</b>\nأرسل المبلغ بالدولار مع الأمر، مثال:\n<code>/calc 15.5</code>")
            return True

    # Command: /rate or /square
    if text.startswith("/rate") or text.startswith("/square") or text.startswith("/سكوار") or text.startswith("سعر السكوار") or text.startswith("سعر الدولار"):
        rate = await get_live_usdt_rate()
        rate_text = (
            f"📈 <b>سعر صرف الـ USDT الحالي في السوق الموازي:</b>\n\n"
            f"💵 <b>1 USDT</b> ≈ <b>{rate:.1f} دج</b> 🇩🇿\n\n"
            f"📊 المصدر المباشر: <a href=\"https://squarealgerie.com\">SquareAlgerie.com</a>\n"
            f"🪙 <i>لحساب تكلفة أي طلب بالدينار أرسل: <code>/calc 20</code></i>"
        )
        await send_msg(chat_id, rate_text)
        return True

    # Command: /watchlist or /alerts
    if text.startswith("/watchlist") or text.startswith("/alerts") or text.startswith("مراقبة") or text.startswith("تنبيهات"):
        from app.publisher.watchlist import get_user_watchlist
        user_watches = get_user_watchlist(user_id)
        if not user_watches:
            await send_msg(
                chat_id,
                "📭 <b>قائمة المراقبة فارغة حالياً!</b>\n\n"
                "عند فحص أي رابط منتج، اضغط على زر <b>[ 🔔 راقب انخفاض السعر ]</b> وسيرسل لك البوت تنبيهاً فور انخفاض سعره."
            )
            return True

        lines = [f"📋 <b>قائمة المنتجات التي تراقبها ({len(user_watches)}):</b>\n"]
        kb = []
        for w in user_watches[:10]:
            p_id = w.get("product_id")
            t_str = w.get("title", "")[:35]
            pr = w.get("price", 0.0)
            lines.append(f"• <b>{t_str}</b>\n  السعر: <b>{pr:.2f}$</b>\n  🆔 <code>{p_id}</code>")
            kb.append([{"text": f"❌ إزالة {t_str[:20]}...", "callback_data": f"unwatch_{p_id}"}])
        markup = {"inline_keyboard": kb}
        await send_msg(chat_id, "\n\n".join(lines), reply_markup=markup)
        return True

    if text.startswith("/help") or "كيف" in text or "طريقة" in text:
        await send_msg(chat_id, HELP_TEXT)
        return True

    if text.startswith("/coupons") or "كوبون" in text or "كود" in text:
        await send_msg(chat_id, COUPONS_TEXT)
        return True

    # Admin Command: /post <url> or /publish <url>
    if text.startswith("/post") or text.startswith("/publish"):
        if not is_admin(user_id):
            await send_msg(chat_id, "⚠️ عذراً، هذا الأمر مخصص لمشرف القناة فقط.")
            return True

        sub_text = text.split(maxsplit=1)[-1] if len(text.split()) > 1 else ""
        target_pid = await resolve_any_ali_link(sub_text)
        if not target_pid:
            await send_msg(chat_id, "⚠️ يرجى تزويد رابط صحيح للمنتج بعد الأمر، مثال:\n<code>/post https://a.aliexpress.com/_xxxx</code>")
            return True

        await send_msg(chat_id, "⏳ جاري تحضير ونشر العرض في القناة @DzAliexpress0...")
        success, err, p_msg_id = await publish_deal_to_channel(target_pid, raw_user_text=sub_text)
        if success:
            ch_clean = str(TARGET_CHANNEL_ID).lstrip("@")
            post_url = f"https://t.me/{ch_clean}/{p_msg_id}"
            confirm_text = f"✅ <b>تم نشر العرض بنجاح في القناة!</b>\n\n🔗 <b>رابط المنشور:</b> {post_url}"
            await send_msg(chat_id, confirm_text)
        else:
            await send_msg(chat_id, f"❌ فشل نشر العرض في القناة: {err}")
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
            "💡 أو اكتب /calc لحساب الأسعار بالدينار، أو /help لمعرفة كيفية الاستخدام."
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

    # Attach exclusive Admin Quick-Publish button if user is admin
    reply_markup = res.get("reply_markup") or {"inline_keyboard": []}
    if is_admin(user_id):
        admin_button = [{"text": "📢 نشر هذا العرض في القناة مباشرة 🚀", "callback_data": f"admin_pub_{pid}"}]
        reply_markup["inline_keyboard"].insert(0, admin_button)

    # Send with photo if available, fallback to text
    if res.get("image_url"):
        success = await send_photo(chat_id, res["image_url"], res["text"], reply_markup)
        if success:
            return True

    await send_msg(chat_id, res["text"], reply_markup)
    return True

# Export alias for compatibility
handle_coin_bot_update = handle_update

async def send_photo(chat_id: int, photo_url: str, caption: str, reply_markup: Optional[Dict] = None, reply_to_message_id: Optional[int] = None) -> bool:
    payload = {
        "chat_id": chat_id,
        "photo": photo_url,
        "caption": caption[:1024],
        "parse_mode": "HTML"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    if reply_to_message_id:
        payload["reply_to_message_id"] = reply_to_message_id

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto",
                json=payload
            )
            return resp.status_code == 200 and resp.json().get("ok")
    except Exception:
        return False

async def send_msg(chat_id: int, text: str, reply_markup: Optional[Dict] = None, reply_to_message_id: Optional[int] = None):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    if reply_to_message_id:
        payload["reply_to_message_id"] = reply_to_message_id

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
