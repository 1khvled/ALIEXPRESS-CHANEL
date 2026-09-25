"""
Dedicated Telegram Admin Scout & Publisher Bot
Controls publishing directly to @DzAliexpress0 for Admin User ID 5625295907.
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

from api.coin_bot import (
    resolve_any_ali_link,
    generate_coin_discount_response,
    get_live_usdt_rate,
    is_admin,
    ALIEXPRESS_AFFILIATE_APP_KEY,
    ALIEXPRESS_AFFILIATE_APP_SECRET,
    ALIEXPRESS_AFFILIATE_TRACKING_ID,
    TARGET_CHANNEL_ID,
    PRIMARY_ADMIN_ID
)

ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN", "8708965924:AAGi9HgLDxKsvaOzPOnCDRhI4c9WAfUvkOk")
PUBLIC_BOT_USERNAME = "Alilo07BOT"

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

async def send_admin_photo(chat_id: int, photo_url: str, caption: str, reply_markup: Optional[Dict] = None) -> bool:
    payload = {
        "chat_id": chat_id,
        "photo": photo_url,
        "caption": caption[:1024],
        "parse_mode": "HTML"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.post(
                f"https://api.telegram.org/bot{ADMIN_BOT_TOKEN}/sendPhoto",
                json=payload
            )
            return resp.status_code == 200 and resp.json().get("ok")
    except Exception:
        return False

async def publish_deal_post(product_id: str, raw_user_text: str = "") -> Tuple[bool, Optional[str], Optional[int]]:
    """Publishes deal post to @DzAliexpress0 using ADMIN_BOT_TOKEN."""
    res = await generate_coin_discount_response(product_id, raw_user_text=raw_user_text)

    prod_title = res.get("title") or "منتج مميز من AliExpress"
    prod_price = res.get("price") or 0.0
    eur_price = round(prod_price * 0.92, 2)
    product_link = res.get("product_link") or f"https://www.aliexpress.com/item/{product_id}.html"
    image_url = res.get("image_url")

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
        f"رابط {product_link}",
        "خصم النقاط (العملات)",
        "",
        f"🪙 استخدم بوت DealScoutDz للشراء بأقل سعر: @{PUBLIC_BOT_USERNAME}"
    ]
    caption = "\n".join(caption_lines)

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
    # 1. Callback Query (e.g. 1-tap publish button)
    if "callback_query" in update:
        cb = update["callback_query"]
        cb_id = cb.get("id")
        cb_data = cb.get("data") or ""
        msg = cb.get("message")
        user = cb.get("from", {})
        user_id = user.get("id")
        chat_id = msg.get("chat", {}).get("id") if msg else None

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

        if cb_data.startswith("pub_"):
            target_pid = cb_data.replace("pub_", "").strip()
            await send_admin_msg(chat_id, f"⏳ جاري نشر المنتج <code>{target_pid}</code> في القناة @DzAliexpress0...")
            success, err, msg_id = await publish_deal_post(target_pid)
            if success:
                ch_clean = str(TARGET_CHANNEL_ID).lstrip("@")
                post_url = f"https://t.me/{ch_clean}/{msg_id}"
                confirm_text = (
                    f"🎉 <b>تم نشر العرض بنجاح في القناة!</b>\n\n"
                    f"🔗 <b>رابط المنشور:</b> <a href=\"{post_url}\">{post_url}</a>\n"
                    f"🆔 <b>رقم المنتج:</b> <code>{target_pid}</code>"
                )
                await send_admin_msg(chat_id, confirm_text)
            else:
                await send_admin_msg(chat_id, f"❌ فشل النشر في القناة:\n<code>{err}</code>\n\nتأكد أن البوت مشرف (Admin) في القناة @DzAliexpress0 وله صلاحية نشر الرسائل.")
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
            "1️⃣ <b>أرسل أي رابط</b> لأي منتج من AliExpress (رابط تطبيق، رابط متصفح، رابط مختصر، أو نص مشاركة).\n"
            "2️⃣ سيعطيك البوت معاينة شاملة للمنشور مع الصورة والسعر بالدولار والدينار.\n"
            "3️⃣ اضغط زر <b>[ 📢 نشر هذا المنشور في القناة الآن 🚀 ]</b> وسينشر فوراً في القناة!\n\n"
            "⚡ <b>أوامر سريعة:</b>\n"
            "• <code>/post &lt;رابط&gt;</code> - للنشر الفوري في القناة دون معاينة.\n"
            "• <code>/rate</code> - لمعرفة سعر الـ USDT الحالي من SquareAlgerie.\n"
            "• <code>/id</code> - لمعرفة معرف التيليجرام الخاص بك."
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

        await send_admin_msg(chat_id, f"⏳ جاري نشر المنتج <code>{target_pid}</code> في القناة...")
        success, err, msg_id = await publish_deal_post(target_pid, raw_user_text=sub_text)
        if success:
            ch_clean = str(TARGET_CHANNEL_ID).lstrip("@")
            post_url = f"https://t.me/{ch_clean}/{msg_id}"
            await send_admin_msg(chat_id, f"✅ <b>تم النشر بنجاح!</b>\n🔗 <a href=\"{post_url}\">{post_url}</a>")
        else:
            await send_admin_msg(chat_id, f"❌ فشل النشر: {err}")
        return True

    # Deal Scouting: Resolve Link
    pid = await resolve_any_ali_link(text)
    if not pid:
        # Check if s.click link had attached text without space
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

    await send_admin_msg(chat_id, f"🔍 <b>تم العثور على المنتج ({pid}):</b>\n⏳ جاري جلب التفاصيل والصورة وحساب الأسعار...")

    res = await generate_coin_discount_response(pid, raw_user_text=text)

    prod_title = res.get("title") or "منتج مميز من AliExpress"
    prod_price = res.get("price") or 0.0
    image_url = res.get("image_url")
    product_link = res.get("product_link") or f"https://www.aliexpress.com/item/{pid}.html"
    coin_link = res.get("coin_link") or product_link

    usdt_rate = await get_live_usdt_rate()
    dzd_val = int(prod_price * usdt_rate) if prod_price else 0

    preview_text = (
        f"📋 <b>معاينة العرض لقناتك @DzAliexpress0:</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🛍️ <b>{html.escape(prod_title)}</b>\n\n"
        f"💵 السعر: <b>{prod_price:.2f}$</b> (~<b>{dzd_val:,} دج</b>)\n"
        f"🛒 <b>رابط الشراء:</b> {product_link}\n"
        f"🪙 <b>رابط العملات:</b> {coin_link}\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"اضغط الزر أدناه لنشر هذا المنشور في القناة فوراً 🚀"
    )

    admin_keyboard = {
        "inline_keyboard": [
            [
                {"text": "📢 نشر هذا العرض في القناة الآن 🚀", "callback_data": f"pub_{pid}"}
            ],
            [
                {"text": "🛒 فحص رابط الشراء المباشر", "url": product_link},
                {"text": "🪙 فحص رابط العملات", "url": coin_link}
            ],
            [
                {"text": "📈 سعر الصرف عبر SquareAlgerie.com 🇩🇿", "url": "https://squarealgerie.com"}
            ]
        ]
    }

    if image_url:
        sent = await send_admin_photo(chat_id, image_url, preview_text, admin_keyboard)
        if sent:
            return True

    await send_admin_msg(chat_id, preview_text, admin_keyboard)
    return True
