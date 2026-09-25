"""
Dedicated Telegram Admin Scout & Publisher Bot
Controls publishing directly to @DzAliexpress0 for Admin User ID 5625295907.
Features:
- Accurately parses user's manual price, coupon code, coins discount, and title from message text
- Exact match with channel auto-posting format (DealCaptionGenerator)
- Serverless persistent state via /tmp storage so image cycling NEVER fails
- Multi-seller image fallback & 1-tap interactive switcher
- 1-tap instant publishing to channel with channel affiliate buttons
"""
import asyncio
import html
import json
import os
import re
import time
from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path
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

_caption_generator = DealCaptionGenerator()

# ── Serverless State Persistence Helpers (/tmp) ─────────────────
TMP_DIR = Path("/tmp")

def save_deal_state(product_id: str, data: Dict[str, Any]):
    """Persists deal metadata & candidate images to disk for serverless persistence."""
    try:
        if TMP_DIR.exists():
            fpath = TMP_DIR / f"deal_{product_id}.json"
            fpath.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass

def load_deal_state(product_id: str) -> Optional[Dict[str, Any]]:
    """Loads deal metadata & candidate images from disk."""
    try:
        if TMP_DIR.exists():
            fpath = TMP_DIR / f"deal_{product_id}.json"
            if fpath.exists():
                return json.loads(fpath.read_text(encoding="utf-8"))
    except Exception:
        pass
    return None

# ── User Deal Text Parser ───────────────────────────────────────
def parse_user_deal_submission(raw_text: str) -> Dict[str, Any]:
    """
    Intelligently extracts deal metadata provided by the human scout in their message:
    - User's exact price (USD)
    - Coupon / Promo codes
    - Coins discount percentage or notes
    - Custom Arabic title
    - Preferred country setting
    """
    data: Dict[str, Any] = {
        "user_price": None,
        "coupon": None,
        "coins_text": None,
        "custom_title": None,
        "country": None
    }
    if not raw_text:
        return data

    text = raw_text.strip()

    # 1. Price extraction (e.g. السعر : $ 23.01 | السعر: 23.01$ | $23.01 | 23.01$ | Price: 23.01)
    price_patterns = [
        r'(?:السعــــ?ر|السعر|Price|price)\s*[:💲]*\s*\$?\s*([0-9]+[.,][0-9]{1,2})\s*\$?',
        r'(?:بـ|بـ\s*\$)\s*([0-9]+[.,][0-9]{1,2})\s*\$?',
        r'\$\s*([0-9]+[.,][0-9]{1,2})\b',
        r'\b([0-9]+[.,][0-9]{1,2})\s*\$'
    ]
    for pat in price_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            try:
                data["user_price"] = float(m.group(1).replace(',', '.'))
                break
            except Exception:
                pass

    # 2. Coupon Code extraction
    coupon_patterns = [
        r'(?:كوبون|كود|قسيمة|Coupon|coupon|Code|code)\s*(?:[^\n:0-9]*[0-9]+/[0-9]+\$?)?\s*[:\-\s]\s*([A-Za-z0-9_]{3,20})',
        r'<code>([A-Za-z0-9_]{3,20})</code>',
        r'(?:كود|كوبون)\s+([A-Za-z0-9_]{4,15})'
    ]
    for pat in coupon_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            code = m.group(1).strip()
            if code.lower() not in ["aliexpress", "http", "https", "item", "deal", "deals", "coins"]:
                data["coupon"] = code
                break

    # 3. Coins Info extraction
    coin_match = re.search(r'(?:خصم\s*(?:النقاط|العملات)|تحتاج\s*(?:الى|إلى)?\s*العملات|عملات|coins?)\s*([0-9]{1,2}\s*%)?', text, re.IGNORECASE)
    if coin_match:
        pct = coin_match.group(1)
        if pct:
            data["coins_text"] = f"خصم النقاط (العملات) {pct.strip()}"
        else:
            data["coins_text"] = "خصم النقاط (العملات)"

    # 4. Country extraction
    if "كوريا" in text or "korea" in text.lower():
        data["country"] = "كوريا 🇰🇷"
    elif "كندا" in text or "canada" in text.lower():
        data["country"] = "كندا 🇨🇦"
    elif "فرنسا" in text or "france" in text.lower():
        data["country"] = "فرنسا 🇫🇷"
    elif "إسبانيا" in text or "spain" in text.lower():
        data["country"] = "إسبانيا 🇪🇸"

    # 5. Custom Title extraction (e.g. تخفيض لـــ : ...)
    m_title = re.search(r'تخفيض\s*لـ+[\s:]*([^\n\r]+)', text)
    if m_title:
        candidate_title = m_title.group(1).strip()
        # Clean inline price, coupon, and coins keywords if they were on the same line
        candidate_title = re.sub(r'(?:السعــــ?ر|السعر|Price|price)\s*[:💲]*\s*\$?[0-9]+[.,]?[0-9]*\s*\$?', '', candidate_title, flags=re.IGNORECASE)
        candidate_title = re.sub(r'\$?[0-9]+[.,][0-9]{1,2}\s*\$?', '', candidate_title)
        candidate_title = re.sub(r'(?:كوبون|كود|قسيمة)\s*[:\-]?\s*[A-Za-z0-9_]+', '', candidate_title, flags=re.IGNORECASE)
        candidate_title = re.sub(r'(?:خصم\s*(?:النقاط|العملات)|عملات|coins?).*', '', candidate_title, flags=re.IGNORECASE)
        candidate_title = re.sub(r'https?://\S+', '', candidate_title).strip()
        candidate_title = re.sub(r'[|؛:,\-_~]+$', '', candidate_title).strip()
        if len(candidate_title) >= 5:
            data["custom_title"] = candidate_title

    return data

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
            other_sellers = await asyncio.to_thread(api.get_products, keywords=keywords, page_size=8)
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

async def build_exact_deal_caption(
    title: str,
    price: Optional[float],
    affiliate_url: str,
    coupon_code: Optional[str] = None,
    coins_text: Optional[str] = None,
    country: Optional[str] = None
) -> str:
    """Builds caption matching the channel's exact auto-posting format with user overrides."""
    country_name = country or "كوريا 🇰🇷"
    eur_price = round(price * 0.92, 2) if price else 0.0

    lines = [
        f"لا تنسى تحويل دولة التطبيق إلى {country_name} 📍"
    ]

    # Select smart situational hook
    hook = _caption_generator._select_smart_hook(
        title=title,
        usd_price=price or 0.0,
        has_points_discount=bool(coins_text),
        has_coupon=bool(coupon_code)
    )
    lines.append(hook)

    safe_title = html.escape(title)
    lines.append(f"تخفيض لـ {safe_title}")

    if price and price > 0:
        lines.append(f"السعر : {price:.2f}$ ({eur_price:.2f}€)🔥")
    else:
        lines.append("سعر مميز وتخفيض عملات 🔥")

    lines.append(f"رابط {affiliate_url}")

    if coupon_code:
        lines.append(f"كوبون : <code>{html.escape(coupon_code)}</code>")

    lines.append(coins_text or "خصم النقاط (العملات)")

    lines.append("")
    lines.append(f"🪙 استخدم بوت DealScoutDz للشراء بأقل سعر: @{PUBLIC_BOT_USERNAME}")

    return "\n".join(lines)

async def publish_deal_post(product_id: str, chosen_image: Optional[str] = None, raw_user_text: str = "") -> Tuple[bool, Optional[str], Optional[int]]:
    """Publishes deal post to @DzAliexpress0 with exact user-specified price & attributes."""
    deal_state = load_deal_state(product_id)
    if not deal_state:
        # Fallback to generating fresh
        deal_state = await prepare_deal_state(product_id, raw_user_text)

    title = deal_state.get("title") or "منتج مميز من AliExpress"
    price = deal_state.get("price")
    product_link = deal_state.get("product_link") or f"https://www.aliexpress.com/item/{product_id}.html"
    deal_link = deal_state.get("primary_link") or deal_state.get("coin_link") or product_link
    coupon = deal_state.get("coupon")
    coins_text = deal_state.get("coins_text")
    country = deal_state.get("country")

    caption = await build_exact_deal_caption(
        title=title,
        price=price,
        affiliate_url=deal_link,
        coupon_code=coupon,
        coins_text=coins_text,
        country=country
    )

    image_url = chosen_image or deal_state.get("chosen_image") or deal_state.get("image_url")
    if not image_url:
        imgs = deal_state.get("images", [])
        if imgs:
            image_url = imgs[0]

    channel_reply_markup = {
        "inline_keyboard": [
            [
                {"text": "🛒 رابط الشراء من AliExpress", "url": deal_link}
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

async def prepare_deal_state(pid: str, raw_user_text: str = "") -> Dict[str, Any]:
    """Prepares and persists the full deal metadata incorporating all user inputs."""
    user_inputs = parse_user_deal_submission(raw_user_text)

    # 1. Fetch affiliate links & basic product details
    res = await generate_coin_discount_response(pid, raw_user_text=raw_user_text)

    # 2. Prioritize user inputs over API defaults
    title = user_inputs["custom_title"] or res.get("title") or "منتج مميز من AliExpress"
    price = user_inputs["user_price"] if user_inputs["user_price"] is not None else res.get("price")
    coupon = user_inputs["coupon"]
    coins_text = user_inputs["coins_text"]
    country = user_inputs["country"] or "كوريا 🇰🇷"
    product_link = res.get("product_link") or f"https://www.aliexpress.com/item/{pid}.html"
    coin_link = res.get("coin_link") or product_link
    bundle_link = res.get("bundle_link") or product_link

    # Determine deal type: 90%+ are coin deals, rare cases are bundle
    is_bundle = any(k in raw_user_text.lower() for k in ["bundle", "حزم", "حزمة", "3 بـ", "3 منتجات"])
    primary_link = bundle_link if is_bundle else coin_link

    # 3. Collect candidate images from original seller + other sellers
    main_image = res.get("image_url")
    small_imgs = []
    try:
        api = AliexpressApi(
            ALIEXPRESS_AFFILIATE_APP_KEY,
            ALIEXPRESS_AFFILIATE_APP_SECRET,
            models.Language.EN,
            models.Currency.USD,
            ALIEXPRESS_AFFILIATE_TRACKING_ID
        )
        details = await safe_api_get_details(api, pid)
        if details and len(details) > 0:
            small_imgs = getattr(details[0], "product_small_image_urls", []) or []

        candidate_images = await collect_product_images(api, pid, title, main_image, small_imgs)
    except Exception:
        candidate_images = [main_image] if main_image else []

    chosen_image = candidate_images[0] if candidate_images else None

    deal_state = {
        "product_id": pid,
        "title": title,
        "price": price,
        "coupon": coupon,
        "coins_text": coins_text,
        "country": country,
        "product_link": product_link,
        "coin_link": coin_link,
        "bundle_link": bundle_link,
        "primary_link": primary_link,
        "is_bundle": is_bundle,
        "images": candidate_images,
        "chosen_image": chosen_image,
        "raw_text": raw_user_text
    }

    save_deal_state(pid, deal_state)
    return deal_state

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

        if not is_admin(user_id):
            try:
                async with httpx.AsyncClient(timeout=3.0) as client:
                    await client.post(
                        f"https://api.telegram.org/bot{ADMIN_BOT_TOKEN}/answerCallbackQuery",
                        json={"callback_query_id": cb_id, "text": "⛔ هذا الإجراء مخصص لمشرف القناة فقط."}
                    )
            except Exception:
                pass
            return True

        # Callback: Publish to channel
        if cb_data.startswith("pub_"):
            parts = cb_data.split("_")
            target_pid = parts[1]
            img_idx = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0

            deal_state = load_deal_state(target_pid) or {}
            images = deal_state.get("images", [])
            chosen_img = images[img_idx] if img_idx < len(images) else deal_state.get("chosen_image")

            try:
                async with httpx.AsyncClient(timeout=3.0) as client:
                    await client.post(
                        f"https://api.telegram.org/bot{ADMIN_BOT_TOKEN}/answerCallbackQuery",
                        json={"callback_query_id": cb_id, "text": "🚀 جاري النشر في القناة..."}
                    )
            except Exception:
                pass

            await send_admin_msg(chat_id, "⏳ جاري نشر المنشور في القناة @DzAliexpress0...")
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

            # Load deal state from /tmp
            deal_state = load_deal_state(target_pid)
            if not deal_state or not deal_state.get("images"):
                # On-demand reconstruct
                deal_state = await prepare_deal_state(target_pid)

            images = deal_state.get("images", [])
            if not images:
                try:
                    async with httpx.AsyncClient(timeout=3.0) as client:
                        await client.post(
                            f"https://api.telegram.org/bot{ADMIN_BOT_TOKEN}/answerCallbackQuery",
                            json={"callback_query_id": cb_id, "text": "⚠️ لا توجد صور أخرى متاحة لهذا المنتج."}
                        )
                except Exception:
                    pass
                return True

            actual_idx = next_idx % len(images)
            new_image = images[actual_idx]
            deal_state["chosen_image"] = new_image
            save_deal_state(target_pid, deal_state)

            title = deal_state.get("title") or "منتج مميز من AliExpress"
            price = deal_state.get("price")
            product_link = deal_state.get("product_link") or f"https://www.aliexpress.com/item/{target_pid}.html"
            coin_link = deal_state.get("coin_link") or product_link
            deal_link = deal_state.get("primary_link") or coin_link
            coupon = deal_state.get("coupon")
            coins_text = deal_state.get("coins_text")
            country = deal_state.get("country")

            caption = await build_exact_deal_caption(
                title=title,
                price=price,
                affiliate_url=deal_link,
                coupon_code=coupon,
                coins_text=coins_text,
                country=country
            )

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

            # Answer callback with toast confirmation
            try:
                async with httpx.AsyncClient(timeout=3.0) as client:
                    await client.post(
                        f"https://api.telegram.org/bot{ADMIN_BOT_TOKEN}/answerCallbackQuery",
                        json={"callback_query_id": cb_id, "text": f"🖼️ تم اختيار الصورة ({actual_idx + 1}/{len(images)})"}
                    )
            except Exception:
                pass

            # Edit message media directly
            edit_success = False
            try:
                async with httpx.AsyncClient(timeout=8.0) as client:
                    resp = await client.post(
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
                    if resp.status_code == 200 and resp.json().get("ok"):
                        edit_success = True
            except Exception:
                pass

            if not edit_success:
                # Fallback: send fresh photo
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
            "1️⃣ <b>ألصق نص العرض أو الرابط</b> (مع السعر أو الكوبون أو نسبة العملات إن وجدت).\n"
            "2️⃣ سيعتمد البوت سعرك وكوبونك ونسبة العملات تلقائياً ويعطيك معاينة مطابقة 100% للقناة.\n"
            "3️⃣ إذا كانت الصورة غير مناسبة، اضغط <b>[ 🔄 تبديل الصورة ]</b> لاختيار صورة من بائع آخر!\n"
            "4️⃣ اضغط <b>[ 📢 نشر هذا المنشور في القناة الآن 🚀 ]</b> وسينشر فوراً في القناة!\n\n"
            "⚡ <b>أوامر سريعة:</b>\n"
            "• <code>/post &lt;نص أو رابط&gt;</code> - للنشر الفوري في القناة دون معاينة.\n"
            "• <code>/rate</code> - لمعرفة سعر الـ USDT الحالي من SquareAlgerie."
        )
        await send_admin_msg(chat_id, welcome_text)
        return True

    if text.startswith("/rate"):
        rate = await get_live_usdt_rate()
        await send_admin_msg(chat_id, f"📈 <b>سعر الـ USDT الحالي في السوق الموازي:</b>\n1 USDT ≈ <b>{rate:.1f} دج</b>\nالمصدر: <a href=\"https://squarealgerie.com\">SquareAlgerie.com</a> 🇩🇿")
        return True

    if text.startswith("/calendar") or text.startswith("/promo") or text.startswith("رزنامة") or text.startswith("تخفيضات"):
        await send_admin_msg(chat_id, "⏳ جاري نشر رزنامة التخفيضات الرسمية في القناة @DzAliexpress0...")
        try:
            from app.publisher.promo_calendar import publish_calendar_to_channel
            success, err, msg_id = await publish_calendar_to_channel(bot_token=ADMIN_BOT_TOKEN)
            if success:
                ch_clean = str(TARGET_CHANNEL_ID).lstrip("@")
                post_url = f"https://t.me/{ch_clean}/{msg_id}"
                await send_admin_msg(chat_id, f"✅ <b>تم نشر رزنامة التخفيضات بنجاح في القناة!</b>\n🔗 <a href=\"{post_url}\">{post_url}</a>")
            else:
                await send_admin_msg(chat_id, f"❌ فشل نشر الرزنامة: {err}")
        except Exception as e:
            await send_admin_msg(chat_id, f"❌ حدث خطأ: {e}")
        return True

    if text.startswith("/disclaimer") or text.startswith("/guide") or text.startswith("تنبيه") or text.startswith("شرح"):
        await send_admin_msg(chat_id, "⏳ جاري نشر وتثبيت تنبيه تغيير الدولة في القناة @DzAliexpress0...")
        try:
            from app.publisher.region_disclaimer import publish_and_pin_disclaimer
            success, err, msg_id = await publish_and_pin_disclaimer(bot_token=ADMIN_BOT_TOKEN)
            if success:
                ch_clean = str(TARGET_CHANNEL_ID).lstrip("@")
                post_url = f"https://t.me/{ch_clean}/{msg_id}"
                await send_admin_msg(chat_id, f"✅ <b>تم نشر وتثبيت تنبيه تغيير الدولة بنجاح في القناة!</b> 📌\n🔗 <a href=\"{post_url}\">{post_url}</a>")
            else:
                await send_admin_msg(chat_id, f"❌ فشل النشر: {err}")
        except Exception as e:
            await send_admin_msg(chat_id, f"❌ حدث خطأ: {e}")
        return True

    if text.startswith("/id") or text.startswith("/myid"):
        await send_admin_msg(chat_id, f"🆔 معرفك: <code>{user_id}</code> (مشرف معتمد 👑)")
        return True

    if text.startswith("/regroup") or text.startswith("تجميع") or text.startswith("تجميعة"):
        await send_admin_msg(chat_id, "⏳ جاري فحص العروض المنشورة لتجميع المنتجات المتشابهة (شرط 4 منتجات أو أكثر من نفس النوع)...")
        try:
            from app.publisher.regrouper import check_and_publish_regrouped_bulletins
            bulletins = await check_and_publish_regrouped_bulletins(bot_token=ADMIN_BOT_TOKEN)
            if bulletins:
                msg_lines = ["✅ <b>تم تجميع ونشر التجميعات التالية بنجاح في القناة:</b>\n"]
                ch_clean = str(TARGET_CHANNEL_ID).lstrip("@")
                for b in bulletins:
                    post_url = f"https://t.me/{ch_clean}/{b['message_id']}"
                    msg_lines.append(f"• <b>{b['category']}</b> ({b['count']} منتجات): <a href=\"{post_url}\">منشور #{b['message_id']}</a>")
                await send_admin_msg(chat_id, "\n".join(msg_lines))
            else:
                await send_admin_msg(chat_id, "ℹ️ <b>لا توجد حالياً 4 منتجات جديدة غير مجمعة من نفس الفئة المحددة</b> (هواتف، ماوسات، كيبوردات، سماعات، تابلت، بي سي، ساعات). سيتم التجميع فور وصول المنتج الرابع!")
        except Exception as e:
            await send_admin_msg(chat_id, f"❌ حدث خطأ أثناء التجميع: {e}")
        return True


    # Direct publish command: /post <url or full deal text>
    if text.startswith("/post") or text.startswith("/publish"):
        sub_text = text.split(maxsplit=1)[-1] if len(text.split()) > 1 else ""
        target_pid = await resolve_any_ali_link(sub_text)
        if not target_pid:
            await send_admin_msg(chat_id, "⚠️ يرجى تزويد رابط صحيح أو نص العرض بعد الأمر، مثال:\n<code>/post https://a.aliexpress.com/_xxxx 19.99$</code>")
            return True

        await send_admin_msg(chat_id, f"⏳ جاري تجهيز ونشر المنتج <code>{target_pid}</code> في القناة...")
        await prepare_deal_state(target_pid, raw_user_text=sub_text)
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

    await send_admin_msg(chat_id, f"🔍 <b>تم العثور على المنتج ({pid}):</b>\n⏳ جاري استخراج بياناتك والبحث عن أفضل الصور...")

    # Prepare deal state with all user-provided details (price, coupon, coins, title)
    deal_state = await prepare_deal_state(pid, raw_user_text=text)

    title = deal_state.get("title") or "منتج مميز من AliExpress"
    price = deal_state.get("price")
    product_link = deal_state.get("product_link") or f"https://www.aliexpress.com/item/{pid}.html"
    coin_link = deal_state.get("coin_link") or product_link
    deal_link = deal_state.get("primary_link") or coin_link
    coupon = deal_state.get("coupon")
    coins_text = deal_state.get("coins_text")
    country = deal_state.get("country")
    candidate_images = deal_state.get("images", [])
    chosen_img = deal_state.get("chosen_image")

    # Build exact matching channel caption
    caption = await build_exact_deal_caption(
        title=title,
        price=price,
        affiliate_url=deal_link,
        coupon_code=coupon,
        coins_text=coins_text,
        country=country
    )

    # Direct Channel Publication (Never repost or clutter admin chat)
    await send_admin_msg(chat_id, f"🚀 <b>جاري نشر العرض مباشرة في القناة @DzAliexpress0...</b>")
    success, err, post_msg_id = await publish_deal_post(pid, chosen_image=chosen_img, raw_user_text=text)

    if success:
        ch_clean = str(TARGET_CHANNEL_ID).lstrip("@")
        post_url = f"https://t.me/{ch_clean}/{post_msg_id}"
        has_multiple_images = len(candidate_images) > 1
        confirm_buttons = [
            [
                {"text": "🔗 فتح المنشور في القناة 🚀", "url": post_url}
            ]
        ]
        if has_multiple_images:
            confirm_buttons.append([
                {"text": f"🔄 تبديل الصورة (بائع آخر / زاوية) 🖼️ (1/{len(candidate_images)})", "callback_data": f"cycle_{pid}_1"}
            ])

        await send_admin_msg(
            chat_id,
            f"✅ <b>تم نشر العرض مباشرة في القناة!</b> 🚀\n\n"
            f"📌 <b>المنتج:</b> {html.escape(title)}\n"
            f"💵 <b>السعر:</b> {price or 0.0}$\n"
            f"📍 <b>الدولة:</b> {country or 'كندا 🇨🇦'}\n"
            f"🔗 <a href=\"{post_url}\">{post_url}</a>",
            {"inline_keyboard": confirm_buttons}
        )
    else:
        await send_admin_msg(chat_id, f"❌ فشل نشر العرض في القناة: {err}")

    return True
