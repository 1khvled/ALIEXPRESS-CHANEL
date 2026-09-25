"""
Dedicated Telegram Admin Scout & Publisher Bot
Controls publishing directly to @DzAliexpress0 for Admin User ID 5625295907.
Features:
- Exact match with auto-posting format (DealCaptionGenerator)
- Automatic fallback to other sellers' images if photo is missing or low quality
- 1-tap interactive button to cycle/switch photos from alternative sellers
- 1-tap instant publishing to channel with channel buttons
"""
import asyncio
import html
import os
import re
import time
from typing import Optional, Dict, Any, List, Tuple
import httpx
from aliexpress_api import AliexpressApi, models

from app.ai.generator import DealCaptionGenerator
from api.coin_bot import (
    resolve_any_ali_link,
    generate_coin_discount_response,
    get_live_usdt_rate,
    is_admin,
    safe_api_get_details,
    ALIEXPRESS_AFFILIATE_APP_KEY,
    ALIEXPRESS_AFFILIATE_APP_SECRET,
    ALIEXPRESS_AFFILIATE_TRACKING_ID,
    TARGET_CHANNEL_ID,
    PRIMARY_ADMIN_ID
)

ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN", "8708965924:AAGi9HgLDxKsvaOzPOnCDRhI4c9WAfUvkOk")
PUBLIC_BOT_USERNAME = "Alilo07BOT"

# Memory cache for candidate images per product: {pid: [url1, url2, ...]}
_PRODUCT_IMAGES_CACHE: Dict[str, List[str]] = {}
_PRODUCT_DATA_CACHE: Dict[str, Dict[str, Any]] = {}

_caption_generator = DealCaptionGenerator()

def extract_search_keywords(title: str) -> str:
    """Extracts 3-4 clean search keywords to find other sellers selling the exact same item."""
    cleaned = re.sub(r'[\(\)\[\],.;:!?/\\|\-_~+]+', ' ', title)
    stop_words = {'for', 'with', 'and', 'the', 'new', 'hot', 'original', 'inch', 'piece', 'pcs', 'pro', 'max', 'livan', 'auto'}
    words = [w for w in cleaned.split() if len(w) > 2 and w.lower() not in stop_words]
    return ' '.join(words[:4])

async def collect_product_images(api: AliexpressApi, product_id: str, title: str, main_img: Optional[str], small_imgs: Optional[List[str]]) -> List[str]:
    """
    Collects photos for the deal:
    1. Seller's main image
    2. Seller's secondary gallery photos (often cleaner studio angles)
    3. Photos from other top sellers selling the exact same item (fallback & alternatives)
    """
    images: List[str] = []
    if main_img and ("alicdn.com" in main_img or "aliexpress-media.com" in main_img):
        images.append(main_img)

    if small_imgs:
        for img in small_imgs:
            if img and ("alicdn.com" in img or "aliexpress-media.com" in img) and img not in images:
                images.append(img)

    # Search other sellers for the same item
    keywords = extract_search_keywords(title)
    if keywords:
        try:
            other_sellers = await asyncio.to_thread(api.get_products, keywords=keywords, page_size=5)
            if other_sellers and hasattr(other_sellers, "products") and other_sellers.products:
                for prod in other_sellers.products:
                    if str(getattr(prod, "product_id", "")) != str(product_id):
                        alt_img = getattr(prod, "product_main_image_url", None)
                        if alt_img and ("alicdn.com" in alt_img or "aliexpress-media.com" in alt_img) and alt_img not in images:
                            images.append(alt_img)
        except Exception:
            pass

    return images

async def send_admin_msg(chat_id: int, text: str, reply_markup: Optional[Dict] = None) -> bool:
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.post(
                f"https://api.telegram.org/bot{ADMIN_BOT_TOKEN}/sendMessage",
                json=payload
            )
            if resp.status_code != 200 or not resp.json().get("ok"):
                payload["parse_mode"] = None
                await client.post(
                    f"https://api.telegram.org/bot{ADMIN_BOT_TOKEN}/sendMessage",
                    json=payload
                )
            return True
    except Exception:
        return False

async def send_admin_photo(chat_id: int, photo_url: str, caption: str, reply_markup: Optional[Dict] = None) -> Optional[int]:
    payload = {
        "chat_id": chat_id,
        "photo": photo_url,
        "caption": caption[:1024],
        "parse_mode": "HTML"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"https://api.telegram.org/bot{ADMIN_BOT_TOKEN}/sendPhoto",
                json=payload
            )
            data = resp.json()
            if resp.status_code == 200 and data.get("ok"):
                return data.get("result", {}).get("message_id")
            return None
    except Exception:
        return None

async def build_auto_posting_caption(prod_title: str, prod_price: Optional[float], affiliate_url: str) -> str:
    """Uses DealCaptionGenerator to produce the EXACT auto posting format."""
    eur_price = round(prod_price * 0.92, 2) if prod_price else 0.0
    return await _caption_generator.generate(
        title=prod_title,
        usd_price=prod_price or 0.0,
        eur_price=eur_price,
        affiliate_url=affiliate_url,
        coupon_code=None,
        has_points_discount=True,
        country_info="كوريا 🇰🇷"
    )

async def publish_deal_post(product_id: str, chosen_image: Optional[str] = None, raw_user_text: str = "") -> Tuple[bool, Optional[str], Optional[int]]:
    """Publishes deal post to @DzAliexpress0 using the EXACT auto-posting format."""
    cached = _PRODUCT_DATA_CACHE.get(product_id)
    if not cached:
        cached = await generate_coin_discount_response(product_id, raw_user_text=raw_user_text)

    prod_title = cached.get("title") or "منتج مميز من AliExpress"
    prod_price = cached.get("price") or 0.0
    product_link = cached.get("product_link") or f"https://www.aliexpress.com/item/{product_id}.html"

    # Exact auto-posting format caption
    caption = await build_auto_posting_caption(prod_title, prod_price, product_link)

    image_url = chosen_image or cached.get("image_url")
    if not image_url:
        imgs = _PRODUCT_IMAGES_CACHE.get(product_id, [])
        if imgs:
            image_url = imgs[0]

    channel_reply_markup = {
        "inline_keyboard": [
            [
                {"text": "🛒 رابط الشراء من AliExpress", "url": product_link}
            ],
            [
                {"text": "🪙 بوت تخفيض العملات DealScoutDz", "url": f"https://t.me/{PUBLIC_BOT_USERNAME}"}
            ]
        ]
    }

    api_url = f"https://api.telegram.org/bot{ADMIN_BOT_TOKEN}"
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

async def handle_admin_update(update: Dict[str, Any]) -> bool:
    """Processes updates coming to the Admin Bot."""
    # 1. Callback Queries
    if "callback_query" in update:
        cb = update["callback_query"]
        cb_id = cb.get("id")
        cb_data = cb.get("data") or ""
        msg = cb.get("message", {})
        msg_id = msg.get("message_id")
        chat_id = msg.get("chat", {}).get("id")
        user = cb.get("from", {})
        user_id = user.get("id")

        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                await client.post(
                    f"https://api.telegram.org/bot{ADMIN_BOT_TOKEN}/answerCallbackQuery",
                    json={"callback_query_id": cb_id}
                )
        except Exception:
            pass

        if not is_admin(user_id):
            await send_admin_msg(chat_id, "⛔ هذا الإجراء مخصص لمشرف القناة فقط.")
            return True

        # Callback: Publish to channel
        if cb_data.startswith("pub_"):
            parts = cb_data.split("_")
            target_pid = parts[1]
            img_idx = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0

            images = _PRODUCT_IMAGES_CACHE.get(target_pid, [])
            chosen_img = images[img_idx] if img_idx < len(images) else None

            await send_admin_msg(chat_id, f"⏳ جاري نشر المنشور في القناة @DzAliexpress0...")
            success, err, post_msg_id = await publish_deal_post(target_pid, chosen_image=chosen_img)
            if success:
                ch_clean = str(TARGET_CHANNEL_ID).lstrip("@")
                post_url = f"https://t.me/{ch_clean}/{post_msg_id}"
                confirm_text = (
                    f"🎉 <b>تم نشر العرض بنجاح في القناة!</b>\n\n"
                    f"🔗 <b>رابط المنشور:</b> <a href=\"{post_url}\">{post_url}</a>\n"
                    f"🆔 <b>رقم المنتج:</b> <code>{target_pid}</code>"
                )
                await send_admin_msg(chat_id, confirm_text)
            else:
                await send_admin_msg(chat_id, f"❌ فشل النشر في القناة:\n<code>{err}</code>\n\nتأكد أن البوت مشرف (Admin) في القناة @DzAliexpress0 وله صلاحية نشر الرسائل.")
            return True

        # Callback: Cycle Image (from alternative sellers / gallery)
        if cb_data.startswith("cycle_"):
            parts = cb_data.split("_")
            target_pid = parts[1]
            next_idx = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0

            images = _PRODUCT_IMAGES_CACHE.get(target_pid, [])
            if not images:
                return True

            actual_idx = next_idx % len(images)
            new_image = images[actual_idx]

            cached = _PRODUCT_DATA_CACHE.get(target_pid, {})
            prod_title = cached.get("title") or "منتج مميز من AliExpress"
            prod_price = cached.get("price") or 0.0
            product_link = cached.get("product_link") or f"https://www.aliexpress.com/item/{target_pid}.html"
            coin_link = cached.get("coin_link") or product_link

            caption = await build_auto_posting_caption(prod_title, prod_price, product_link)

            next_cycle_idx = (actual_idx + 1) % len(images)
            switch_label = f"🔄 تبديل الصورة (بائع آخر / زاوية) 🖼️ ({actual_idx + 1}/{len(images)})"

            new_keyboard = {
                "inline_keyboard": [
                    [
                        {"text": "📢 نشر هذا المنشور في القناة الآن 🚀", "callback_data": f"pub_{target_pid}_{actual_idx}"}
                    ],
                    [
                        {"text": switch_label, "callback_data": f"cycle_{target_pid}_{next_cycle_idx}"}
                    ],
                    [
                        {"text": "🛒 رابط الشراء المباشر", "url": product_link},
                        {"text": "🪙 رابط العملات", "url": coin_link}
                    ]
                ]
            }

            # Edit message media
            try:
                async with httpx.AsyncClient(timeout=8.0) as client:
                    await client.post(
                        f"https://api.telegram.org/bot{ADMIN_BOT_TOKEN}/editMessageMedia",
                        json={
                            "chat_id": chat_id,
                            "message_id": msg_id,
                            "media": {
                                "type": "photo",
                                "media": new_image,
                                "caption": caption[:1024],
                                "parse_mode": "HTML"
                            },
                            "reply_markup": new_keyboard
                        }
                    )
            except Exception:
                # If editMessageMedia fails, send new photo
                await send_admin_photo(chat_id, new_image, caption, new_keyboard)
            return True

        return True

    # 2. Messages
    message = update.get("message")
    if not message:
        return False

    chat_id = message.get("chat", {}).get("id")
    from_user = message.get("from", {})
    user_id = from_user.get("id") or chat_id
    text = (message.get("text") or "").strip()
    if not chat_id:
        return False

    # Security check: only admin can use this bot
    if not is_admin(user_id):
        refusal = (
            "⛔ <b>عذراً، هذا البوت خاص بإدارة ونشر عروض القناة فقط.</b>\n\n"
            f"🪙 يمكنك استخدام بوت العملات المفتوح للجميع: @{PUBLIC_BOT_USERNAME}"
        )
        await send_admin_msg(chat_id, refusal)
        return True

    # Commands
    if text.startswith("/start") or text.startswith("/help"):
        welcome_text = (
            "👑 <b>مرحباً بك يا مدير في بوت DealScout Admin</b> 🚀\n\n"
            "هذا البوت مخصص لك كأدمن معتمد لإدارة عروض القناة @DzAliexpress0 بسهولة وسرعة فائقة.\n\n"
            "📌 <b>كيف تستخدم البوت:</b>\n"
            "1️⃣ <b>أرسل أي رابط</b> لأي منتج من AliExpress.\n"
            "2️⃣ سيعطيك البوت معاينة مطابقة 100% لمنشور القناة مع الصورة وسعر العملات.\n"
            "3️⃣ إذا كانت الصورة غير مناسبة، اضغط زر <b>[ 🔄 تبديل الصورة ]</b> لاختيار صورة من بائع آخر أو زاوية أفضل!\n"
            "4️⃣ اضغط <b>[ 📢 نشر هذا المنشور في القناة الآن 🚀 ]</b> وسينشر فوراً في القناة!\n\n"
            "⚡ <b>أوامر سريعة:</b>\n"
            "• <code>/post &lt;رابط&gt;</code> - للنشر الفوري في القناة دون معاينة.\n"
            "• <code>/rate</code> - لمعرفة سعر الـ USDT الحالي من SquareAlgerie."
        )
        await send_admin_msg(chat_id, welcome_text)
        return True

    if text.startswith("/rate"):
        rate = await get_live_usdt_rate()
        await send_admin_msg(chat_id, f"📈 <b>سعر الـ USDT الحالي في السوق الموازي:</b>\n1 USDT ≈ <b>{rate:.1f} دج</b>\nالمصدر: <a href=\"https://squarealgerie.com\">SquareAlgerie.com</a> 🇩🇿")
        return True

    if text.startswith("/id") or text.startswith("/myid"):
        await send_admin_msg(chat_id, f"🆔 معرفك: <code>{user_id}</code> (مشرف معتمد 👑)")
        return True

    # Direct publish command: /post <url>
    if text.startswith("/post") or text.startswith("/publish"):
        sub_text = text.split(maxsplit=1)[-1] if len(text.split()) > 1 else ""
        target_pid = await resolve_any_ali_link(sub_text)
        if not target_pid:
            await send_admin_msg(chat_id, "⚠️ يرجى تزويد رابط صحيح بعد الأمر، مثال:\n<code>/post https://a.aliexpress.com/_xxxx</code>")
            return True

        await send_admin_msg(chat_id, f"⏳ جاري تجهيز ونشر المنتج <code>{target_pid}</code> في القناة...")
        success, err, post_msg_id = await publish_deal_post(target_pid, raw_user_text=sub_text)
        if success:
            ch_clean = str(TARGET_CHANNEL_ID).lstrip("@")
            post_url = f"https://t.me/{ch_clean}/{post_msg_id}"
            await send_admin_msg(chat_id, f"✅ <b>تم النشر بنجاح!</b>\n🔗 <a href=\"{post_url}\">{post_url}</a>")
        else:
            await send_admin_msg(chat_id, f"❌ فشل النشر: {err}")
        return True

    # Deal Scouting: Resolve Link
    pid = await resolve_any_ali_link(text)
    if not pid:
        m = re.search(r's\.click\.aliexpress\.com/e/(_[a-zA-Z0-9]+)', text)
        if m:
            clean_short = f"https://s.click.aliexpress.com/e/{m.group(1)}"
            pid = await resolve_any_ali_link(clean_short)

    if not pid:
        await send_admin_msg(
            chat_id,
            "⚠️ <b>لم يتم التعرف على كود المنتج من الرابط.</b>\nيرجى التأكد من الرابط أو إرسال رقم المنتج (ID) مباشرة."
        )
        return True

    await send_admin_msg(chat_id, f"🔍 <b>تم العثور على المنتج ({pid}):</b>\n⏳ جاري جلب التفاصيل من البائع والبحث عن صور أفضل من بائعين آخرين...")

    res = await generate_coin_discount_response(pid, raw_user_text=text)
    _PRODUCT_DATA_CACHE[pid] = res

    prod_title = res.get("title") or "منتج مميز من AliExpress"
    prod_price = res.get("price") or 0.0
    main_image = res.get("image_url")
    product_link = res.get("product_link") or f"https://www.aliexpress.com/item/{pid}.html"
    coin_link = res.get("coin_link") or product_link

    # Discover candidate images (seller gallery + other sellers selling the exact same item)
    try:
        api = AliexpressApi(
            ALIEXPRESS_AFFILIATE_APP_KEY,
            ALIEXPRESS_AFFILIATE_APP_SECRET,
            models.Language.EN,
            models.Currency.USD,
            ALIEXPRESS_AFFILIATE_TRACKING_ID
        )
        small_imgs = []
        details = await safe_api_get_details(api, pid)
        if details and len(details) > 0:
            small_imgs = getattr(details[0], "product_small_image_urls", []) or []

        candidate_images = await collect_product_images(api, pid, prod_title, main_image, small_imgs)
    except Exception:
        candidate_images = [main_image] if main_image else []

    _PRODUCT_IMAGES_CACHE[pid] = candidate_images

    # Fallback to alternative seller photo if main seller photo is missing
    chosen_img = candidate_images[0] if candidate_images else None

    # Exact auto-posting format
    caption = await build_auto_posting_caption(prod_title, prod_price, product_link)

    # Build admin interactive keyboard
    has_multiple_images = len(candidate_images) > 1
    admin_buttons = [
        [
            {"text": "📢 نشر هذا المنشور في القناة الآن 🚀", "callback_data": f"pub_{pid}_0"}
        ]
    ]

    if has_multiple_images:
        admin_buttons.append([
            {"text": f"🔄 تبديل الصورة (بائع آخر / زاوية) 🖼️ (1/{len(candidate_images)})", "callback_data": f"cycle_{pid}_1"}
        ])

    admin_buttons.append([
        {"text": "🛒 رابط الشراء المباشر", "url": product_link},
        {"text": "🪙 رابط العملات", "url": coin_link}
    ])

    admin_keyboard = {"inline_keyboard": admin_buttons}

    if chosen_img:
        msg_id = await send_admin_photo(chat_id, chosen_img, caption, admin_keyboard)
        if msg_id:
            return True

    await send_admin_msg(chat_id, caption, admin_keyboard)
    return True
