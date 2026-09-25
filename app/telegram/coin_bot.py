"""
AliExpress Coin & Discount Bot Handler
Processes incoming user messages with AliExpress links and generates:
1. Maximum Coins Discount Page URL (سعر تخفيض العملات)
2. Bundle Deals URL (سعر عرض bundle deal)
3. Super Deals URL (سعر السوبر ديلز)
4. Limited Offer / Big Save URL (سعر العرض المحدود)
With product photo, DZD estimation, inline buttons, and affiliate tracking.
"""
import asyncio
import os
import re
from typing import Optional, Dict, Any, List
from urllib.parse import urlparse, parse_qs
import httpx
from aliexpress_api import AliexpressApi, models

from app.config.settings import settings
from app.aliexpress.urls import extract_all_urls, extract_product_id_from_url
from app.aliexpress.resolver import url_resolver
from app.utils.logger import logger

DZD_USD_RATE = 240.0

WELCOME_TEXT = """👋 مرحباً بك في بوت DealScoutDz لزيادة تخفيض العملات! 🪙

هذا البوت يعمل على **زيادة نسبة التخفيض بالعملات (النقاط)** من 1%~5% إلى نسبة عالية تصل حتى **70%** في معظم منتجات AliExpress 🤑

📌 **طريقة الاستخدام بكل بساطة:**
1️⃣ انسخ رابط أي منتج تريده من تطبيق أو موقع AliExpress.
2️⃣ أرسل الرابط هنا في المحادثة.
3️⃣ سيرسل لك البوت فوراً صورة المنتج وروابط التخفيض الأكبر (تخفيض العملات، Bundle Deals، السوبر ديلز) مع أزرار شراء سريعة! 🚀
"""

HELP_TEXT = """💡 **دليل استخدام تخفيض العملات بأقصى نسبة:**

1️⃣ **كيف تفعل الخصم الأكبر؟**
عند فتح رابط العملات، لا تشترِ من الصفحة العادية! اضغط على زر **"شراء الآن"** مباشرة من صفحة العملات، أو أضف المنتج إلى السلة من داخل صفحة العملات لتخصم لك كل النقاط المتاحة.

2️⃣ **تحويل الدولة إلى كوريا 🇰🇷:**
لا تنسى تحويل دولة التطبيق إلى كوريا 🇰🇷 📍 من إعدادات AliExpress للحصول على أسعار أقل وتخفيض عملات إضافي على الكثير من الأجهزة والعتاد!

3️⃣ **كيف تجمع العملات يومياً؟**
ادخل يومياً لتطبيق AliExpress واضغط على أيقونة **Coins / العملات** واجمع العملات المجانية اليومية (يمكنك جمع 70 إلى 150 عملة يومياً مجاناً).

4️⃣ **الكوبونات الإضافية:**
يمكنك دمج تخفيض العملات مع كودات التخفيض للحصول على أقل سعر ممكن عالمياً!

📢 للمزيد من العروض اليومية، انضم لقناتنا: @DzAliexpress0
"""

COUPONS_TEXT = """🎟️ **أحدث كودات التخفيض من AliExpress لشهر أكتوبر 🔥**
━━━━━━━━━━━━━━━━━
🎯 **تخفيضات Choice Day (1 - 7 أكتوبر):**
▫️ خصم 3$ عند الشراء بـ 29$+ ⬅️ كود: `CDDZ03`
▫️ خصم 6$ عند الشراء بـ 49$+ ⬅️ كود: `CDDZ06`
▫️ خصم 10$ عند الشراء بـ 79$+ ⬅️ كود: `CDDZ10`
▫️ خصم 20$ عند الشراء بـ 159$+ ⬅️ كود: `CDDZ20`
▫️ خصم 40$ عند الشراء بـ 299$+ ⬅️ كود: `CDDZ40`
━━━━━━━━━━━━━━━━━
💡 يمكنك إدخال الكود في صفحة الدفع والاستفادة من خصم العملات في نفس الوقت!

📢 تابع قناتنا للمزيد: @DzAliexpress0
"""

async def resolve_product_from_text(text: str) -> Optional[Dict[str, Any]]:
    """Extracts AliExpress product ID and details from user text."""
    urls = extract_all_urls(text)
    if not urls:
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

        prod_title = "منتج مميز من AliExpress"
        prod_price = None
        prod_image = None

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
                    img = getattr(info, 'product_main_image_url', None)
                    if img and ("alicdn.com" in img or "aliexpress-media.com" in img):
                        prod_image = img
                break
            except Exception as e:
                if "ApiCallLimit" in str(e) or "frequency exceeds" in str(e):
                    await asyncio.sleep(1.5)
                else:
                    break

        target_urls = [
            f"https://m.aliexpress.com/p/coin-index/index.html?productIds={product_id}",
            f"https://www.aliexpress.com/item/{product_id}.html?sourceType=620&channel=coin",
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

        coin_link_1 = aff_map.get(target_urls[0], target_urls[0])
        coin_link_2 = aff_map.get(target_urls[1], target_urls[1])
        bundle_link = aff_map.get(target_urls[2], target_urls[2])
        super_link = aff_map.get(target_urls[3], target_urls[3])
        limited_link = aff_map.get(target_urls[4], target_urls[4])

        price_line = ""
        if prod_price:
            dzd_val = int(prod_price * DZD_USD_RATE)
            price_line = f"💵 السعر: {prod_price:.2f}$ (~{dzd_val:,} دج) 🔥\n"

        message_text = f"""🛍️ {prod_title}
{price_line}
🪙 **سعر تخفيض العملات (Coins):**
🔗 {coin_link_1}

📦 **عروض الحزم (Bundle Deals):**
🔗 {bundle_link}

⚡ **عروض السوبر ديلز (SuperDeals):**
🔗 {super_link}

⏳ **العرض المحدود (Limited Offer):**
🔗 {limited_link}

💡 *نصيحة: ادخل من رابط العملات واشترِ مباشرة أو أضف المنتج للسلة لتفعيل أكبر نسبة خصم!*"""

        reply_markup = {
            "inline_keyboard": [
                [
                    {"text": "🪙 شراء بتخفيض العملات المباشر", "url": coin_link_1}
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

    except Exception as e:
        logger.exception(f"Error generating coin discount response: {e}")
        return None
