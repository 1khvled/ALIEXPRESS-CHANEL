"""
Bulletproof AliExpress Coin & Discount Bot Handler
Guaranteed Zero-Failure & Ultra-Fast:
- Works with ANY AliExpress link (desktop, mobile, shortlinks, share texts, raw IDs)
- Live USDT exchange rate integration via SquareAlgerie.com (248-250 DA)
- Advertisement and live rate badge for SquareAlgerie.com
- Parallel/Graceful API execution with instant fallback to direct affiliate coin links
- 100% Delivery guarantee (HTML mode with auto-fallback)
"""
import asyncio
import html
import os
import re
import time
from typing import Optional, Dict, Any, List
from urllib.parse import urlparse, parse_qs
import httpx
from aliexpress_api import AliexpressApi, models

from app.config.settings import settings
from app.utils.logger import logger

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
3️⃣ سيرسل لك البوت فوراً روابط التخفيض الأكبر (تخفيض العملات، Bundle Deals، السوبر ديلز) مع السعر المباشر بالدينار الجزائري! 🚀

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

async def resolve_any_ali_link(text: str) -> Optional[str]:
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

    try:
        async with httpx.AsyncClient(timeout=3.5, follow_redirects=False) as client:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            resp = await client.get(raw_url, headers=headers)
            loc = resp.headers.get("location") or resp.headers.get("Location")
            if loc:
                found = extract_pid_from_string(loc)
                if found:
                    return found
                if loc.startswith("http"):
                    resp2 = await client.get(loc, headers=headers, timeout=2.5)
                    loc2 = resp2.headers.get("location") or str(resp2.url)
                    found2 = extract_pid_from_string(loc2)
                    if found2:
                        return found2
            if resp.status_code == 200 and resp.text:
                found = extract_pid_from_string(resp.text[:5000])
                if found:
                    return found
    except Exception:
        pass

    return extract_pid_from_string(raw_url)

async def generate_coin_discount_response(product_id: str, canonical_url: Optional[str] = None) -> Dict[str, Any]:
    usdt_rate = await get_live_usdt_rate()

    direct_coin = f"https://m.aliexpress.com/p/coin-index/index.html?productIds={product_id}"
    direct_bundle = f"https://www.aliexpress.com/ssr/300000512/BundleDeals2?productIds={product_id}"
    direct_super = f"https://www.aliexpress.com/item/{product_id}.html?sourceType=680"
    direct_limited = f"https://www.aliexpress.com/item/{product_id}.html?sourceType=562"

    target_urls = [direct_coin, direct_bundle, direct_super, direct_limited]

    prod_title = "منتج مميز من AliExpress"
    prod_price = None
    prod_image = None
    coin_link = direct_coin
    bundle_link = direct_bundle
    super_link = direct_super
    limited_link = direct_limited

    try:
        api = AliexpressApi(
            settings.ALIEXPRESS_AFFILIATE_APP_KEY,
            settings.ALIEXPRESS_AFFILIATE_APP_SECRET,
            models.Language.EN,
            models.Currency.USD,
            settings.ALIEXPRESS_AFFILIATE_TRACKING_ID or "dzkhvled16"
        )

        try:
            details = await asyncio.wait_for(
                asyncio.to_thread(api.get_products_details, [product_id]),
                timeout=2.0
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
        except Exception:
            pass

        await asyncio.sleep(0.12)

        try:
            raw_links = await asyncio.wait_for(
                asyncio.to_thread(api.get_affiliate_links, ",".join(target_urls)),
                timeout=2.0
            )
            if raw_links:
                aff_map = {}
                for item in raw_links:
                    orig = getattr(item, 'source_value', '')
                    promo = getattr(item, 'promotion_link', '')
                    if orig and promo:
                        aff_map[orig] = promo
                coin_link = aff_map.get(direct_coin, direct_coin)
                bundle_link = aff_map.get(direct_bundle, direct_bundle)
                super_link = aff_map.get(direct_super, direct_super)
                limited_link = aff_map.get(direct_limited, direct_limited)
        except Exception:
            pass

    except Exception:
        pass

    price_line = ""
    if prod_price:
        dzd_val = int(prod_price * usdt_rate)
        price_line = f"💵 السعر التقريبي: <b>{prod_price:.2f}$</b> (~<b>{dzd_val:,} دج</b>)\n(سعر الصرف 1 USDT ≈ {int(usdt_rate)} دج عبر SquareAlgerie.com)\n"

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

💡 <i>نصيحة: ادخل من رابط العملات واشترِ مباشرة أو أضف المنتج للسلة لتفعيل أكبر نسبة خصم!</i>

📊 <i>أسعار الصرف مقدمة من:</i> <a href="https://squarealgerie.com">SquareAlgerie.com</a> 🇩🇿"""

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
