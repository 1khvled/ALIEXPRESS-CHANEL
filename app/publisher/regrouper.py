"""
Daily Tajmi3at & Auto-Regrouping Bulletin Algorithm
Automatically aggregates published deals of the exact same category (e.g. 4+ Phones, 4+ Mice, 4+ Keyboards)
into high-converting index bulletins linking back to the channel's own posts at the end of each day (~10:00 PM UTC+1).
Strict Rule: Minimum 4 items required for category bulletins. If no category reaches 4, builds a Master Daily Roundup.
"""
import os
import sys
import json
import re
import asyncio
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Tuple, Optional, Set
from pathlib import Path
import httpx

try:
    from sqlalchemy import select
    from app.db.session import db_context
    from app.db.models import Deal, TelegramPost
    HAS_DB = True
except (ImportError, Exception):
    HAS_DB = False

from app.config.settings import settings
from app.utils.logger import logger
from app.publisher.state_tracker import (
    load_persistent_state,
    save_persistent_state,
    is_tajmi3at_time_window,
    is_daily_tajmi3at_eligible,
    record_daily_tajmi3at_published,
    get_regrouped_channel_msg_ids,
    record_deals_regrouped,
    TARGET_CHANNEL_ID
)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8900887118:AAELbFHyV2joUO-4EJ0fPSoZurkQNuENbfY")
ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN", "8708965924:AAH7SoSX7VV3Nx_yI_J39VzWjlsc-XPgXAQ")

CATEGORIES_CONFIG = {
    "phones": {
        "header": "📱 <b>تجميعة أقوى عروض الهواتف الذكية لنهار اليوم 🇩🇿🔥</b>",
        "tag": "#تجميعة_الهواتف",
        "keywords": [
            "phone", "phones", "smartphone", "smartphones", "هاتف", "جوال", "موبايل", "poco", "redmi",
            "realme", "honor", "samsung", "infinix", "oppo", "vivo", "iphone",
            "nubia", "zte", "motorola", "iqoo"
        ],
        "negative_keywords": [
            "headset", "earphone", "case", "cover", "holder", "charger",
            "cable", "cooler", "mousepad", "screen protector", "glass", "film",
            "watch", "band", "ساعة", "سوار", "smartwatch", "قلم", "stylus",
            "بوشات", "زجاج", "واقي"
        ]
    },
    "mice": {
        "header": "🖱️ <b>تجميعة ماوسات القيمنق الاحترافية لنهار اليوم 🇩🇿🔥</b>",
        "tag": "#تجميعة_الماوسات",
        "keywords": [
            "mouse", "mice", "ماوس", "فأرة", "فارة", "attack shark x3",
            "attack shark r1", "attack shark x1", "attack shark x11", "ajazz aj",
            "vxe r1", "scyrox", "wireless mouse", "gaming mouse", "zaopin", "delux"
        ],
        "negative_keywords": [
            "mousepad", "mouse pad", "pad", "باد", "باد ماوس"
        ]
    },
    "keyboards": {
        "header": "⌨️ <b>تجميعة الكيبوردات الميكانيكية لنهار اليوم 🇩🇿🔥</b>",
        "tag": "#تجميعة_الكيبوردات",
        "keywords": [
            "keyboard", "keyboards", "كيبورد", "لوحة مفاتيح", "ak820", "rainy75", "hi75",
            "crush80", "aula f75", "aula f87", "mechanical keyboard", "ajazz ak"
        ],
        "negative_keywords": [
            "keycap", "keycaps", "switch", "switches"
        ]
    },
    "headsets": {
        "header": "🎧 <b>تجميعة أفضل السماعات والصوتيات لنهار اليوم 🇩🇿🔥</b>",
        "tag": "#تجميعة_السماعات",
        "keywords": [
            "headset", "headsets", "headphone", "headphones", "earbuds", "earbud", "earphone", "earphones", "tws", "iem",
            "سماعة", "سماعات", "سماعة محيطية", "attack shark l90", "attack shark l80",
            "moondrop", "qcy", "lenovo xt", "kz edx", "monster maxstar"
        ],
        "negative_keywords": [
            "case", "cover", "cable", "كابل"
        ]
    },
    "tablets": {
        "header": "📟 <b>تجميعة أجهزة التابلت واللوحيات لنهار اليوم 🇩🇿🔥</b>",
        "tag": "#تجميعة_التابلت",
        "keywords": [
            "tablet", "tablets", "tab", "pad", "ipad", "تابلت", "ايباد", "لوحي",
            "xiaomi pad", "redmi pad", "realme pad", "blackview pad", "blackview link"
        ],
        "negative_keywords": [
            "mousepad", "mouse pad", "thermal pad", "ptm7950", "case", "cover",
            "holder", "stand", "screen protector", "بوشات"
        ]
    },
    "pc_parts": {
        "header": "🖥️ <b>تجميعة عتاد وقطع البي سي لنهار اليوم 🇩🇿🔥</b>",
        "tag": "#تجميعة_البي_سي",
        "keywords": [
            "ram", "ssd", "nvme", "gpu", "graphics card", "cooler", "thermal pad",
            "ptm7950", "كارت شاشة", "كرت شاشة", "معالج", "مشتت", "رام", "ddr4", "ddr5",
            "ryzen", "somnambulist", "cpu"
        ],
        "negative_keywords": []
    },
    "smartwatches": {
        "header": "⌚ <b>تجميعة الساعات الذكية المعتمدة لنهار اليوم 🇩🇿🔥</b>",
        "tag": "#تجميعة_الساعات",
        "keywords": [
            "smartwatch", "smart watch", "smart band", "ساعة ذكية", "ساعة",
            "سوار ذكي", "watch", "colmi", "zeblaze", "amazfit", "choice watch",
            "watch x", "watch 2", "watch 3", "watch 4", "watch 5", "watch pro",
            "cmf watch", "btalk"
        ],
        "negative_keywords": [
            "strap", "حزام", "screen protector", "حماية", "charger", "cable"
        ]
    }
}

def classify_deal_category(title: str, text: str = "") -> Optional[str]:
    """Strictly classifies a deal into a primary homogeneous product category using word boundaries."""
    if not title:
        return None

    # Exclude multi-accessory combo packs (e.g. بوشات / كابل / ماوس / قلم)
    if title.count("/") >= 3:
        return None

    combined = f"{title or ''} {text or ''}".lower()

    # Priority order: specific items first (tablets, smartwatches) before generic phone brands
    priority_order = ["tablets", "keyboards", "mice", "headsets", "smartwatches", "phones", "pc_parts"]

    for cat_name in priority_order:
        config = CATEGORIES_CONFIG[cat_name]

        # Check negative keywords first
        has_negative = False
        for neg in config["negative_keywords"]:
            if re.search(rf'(?:\b|_){re.escape(neg)}(?:\b|_)', combined) or neg in combined:
                has_negative = True
                break
        if has_negative:
            continue

        # Check positive keywords with word boundaries
        for kw in config["keywords"]:
            if any(ord(char) > 127 for char in kw):
                if kw in combined:
                    return cat_name
            else:
                if re.search(rf'\b{re.escape(kw)}\b', combined):
                    return cat_name

    return None

def clean_item_title(raw_title: str) -> str:
    """Produces clean, readable title for the bulletin line."""
    t = raw_title or "منتج مميز"
    t = re.sub(r'[\$€].*$', '', t).strip()
    t = re.sub(r'^[❗️🔖📌🔥🚨⚡💥✨📦🛒🎁📢✅💎💰🔻ـ\s\-:]+', '', t).strip()
    # Strip long noise words
    t = re.sub(r'(\s*-\s*AliExpress.*$|\s*\|\s*AliExpress.*$)', '', t).strip()
    return t[:48].strip()

def get_recent_published_deals_for_roundup(max_age_hours: float = 24.0) -> List[Dict[str, Any]]:
    """
    Collects active deals published to @DzAliexpress0 within the last 24 hours.
    Merges persistent state tracking (published_state.json) and local SQLite (deals.db).
    """
    state = load_persistent_state()
    deals_dict = state.get("channel_published_deals", {})
    now = time_now = datetime.now(timezone.utc).timestamp()
    max_age_sec = max_age_hours * 3600

    collected: Dict[int, Dict[str, Any]] = {}

    # 1. Load from persistent state (primary in GitHub Actions & production)
    target_clean = str(TARGET_CHANNEL_ID).lstrip("@")
    for post_key, info in deals_dict.items():
        if info.get("status") == "DELETED":
            continue
        msg_id = info.get("channel_msg_id")
        if not msg_id or int(msg_id) <= 0:
            continue
        ts = info.get("timestamp", 0)
        if (now - ts) > max_age_sec:
            continue

        msg_id_int = int(msg_id)
        title = clean_item_title(info.get("title", ""))
        price = float(info.get("price") or 0.0)
        category = classify_deal_category(info.get("title", ""))

        collected[msg_id_int] = {
            "channel_msg_id": msg_id_int,
            "product_id": info.get("product_id"),
            "title": title,
            "price": price,
            "timestamp": ts,
            "category": category,
            "channel_url": f"https://t.me/{target_clean}/{msg_id_int}"
        }

    return list(collected.values())

def format_deal_line(item: Dict[str, Any], channel_username: str) -> str:
    """Formats a single product line for the bulletin with both $ and € and post link."""
    title = item.get("title") or "منتج مميز"
    price_val = float(item.get("price") or 0.0)
    eur_rate = float(getattr(settings, "EUR_USD_RATE", 0.92))
    eur_val = price_val * eur_rate

    if price_val > 0:
        if price_val.is_integer():
            price_str = f"${int(price_val)} ({eur_val:.2f}€)"
        else:
            price_str = f"${price_val:.2f} ({eur_val:.2f}€)"
    else:
        price_str = "سعر خاص ومخفض 🔥"

    post_url = item.get("channel_url") or f"https://t.me/{channel_username}/{item['channel_msg_id']}"
    return f"▫️ <b>{title}</b>\n   💰 <b>{price_str}</b> ▫️ <a href=\"{post_url}\">رابط المنشور 👈</a>\n"

def build_category_bulletin_text(category_name: str, items: List[Dict[str, Any]], channel_username: str) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Builds the caption for a category bulletin, dynamically fitting items
    to guarantee the total length strictly never exceeds 980 characters (Telegram photo caption limit: 1024).
    """
    cat_config = CATEGORIES_CONFIG.get(category_name, {
        "header": f"📦 <b>تجميعة عروض {category_name} لنهار اليوم 🇩🇿🔥</b>"
    })

    header_lines = [
        cat_config["header"],
        "━━━━━━━━━━━━━━━━━"
    ]
    footer_lines = [
        "━━━━━━━━━━━━━━━━━",
        "💡 <i>اضغط على (رابط المنشور) للانتقال مباشرة للعرض في القناة.</i>",
        "🪙 <b>تخفيض إضافي بالعملات:</b> أرسل رابط أي منتج للبوت @Alilo07BOT"
    ]
    footer_text = "\n".join(footer_lines)

    selected_items: List[Dict[str, Any]] = []
    body_lines: List[str] = []

    for item in items:
        line = format_deal_line(item, channel_username)
        # Check total hypothetical caption length
        candidate_text = "\n".join(header_lines + body_lines + [line, footer_text])
        if len(candidate_text) > 980:
            break
        body_lines.append(line)
        selected_items.append(item)

    full_caption = "\n".join(header_lines + body_lines + footer_lines)
    return full_caption, selected_items

def build_master_daily_roundup_text(deals: List[Dict[str, Any]], channel_username: str) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Builds the Master Daily Roundup when individual categories don't have >= 4 items.
    Selects top deals across diverse categories.
    """
    header_lines = [
        "🌙 <b>تجميعة أفضل صفقات وعروض اليوم على AliExpress 🇩🇿🔥</b>",
        "━━━━━━━━━━━━━━━━━"
    ]
    footer_lines = [
        "━━━━━━━━━━━━━━━━━",
        "💡 <i>أبرز صيدات وصفقات نهار اليوم المنشورة في القناة!</i>",
        "🪙 <b>تخفيض إضافي بالعملات:</b> أرسل رابط أي منتج للبوت @Alilo07BOT"
    ]
    footer_text = "\n".join(footer_lines)

    selected_items: List[Dict[str, Any]] = []
    body_lines: List[str] = []

    # Take deals with valid prices, prioritized
    sorted_deals = sorted(deals, key=lambda x: x.get("price", 0), reverse=True)

    for item in sorted_deals:
        line = format_deal_line(item, channel_username)
        candidate_text = "\n".join(header_lines + body_lines + [line, footer_text])
        if len(candidate_text) > 980:
            break
        body_lines.append(line)
        selected_items.append(item)

    full_caption = "\n".join(header_lines + body_lines + footer_lines)
    return full_caption, selected_items

async def check_and_publish_regrouped_bulletins(
    bot_token: Optional[str] = None,
    force: bool = False,
    min_items: int = 4,
    max_bulletins: int = 4
) -> List[Dict[str, Any]]:
    """
    Daily 10:00 PM Tajmi3at (Roundups) Publisher.
    - If not forced: strictly verifies the ~10 PM window (21:30 - 22:45 UTC+1) and daily idempotency.
    - Collects deals published today on @DzAliexpress0.
    - Publishes category roundups for categories meeting min_items (default 4).
    - If no category reaches 4, publishes a Master Daily Roundup.
    - Attaches storage/assets/tajmi3at_banner.png.
    - Records daily completion to prevent duplicate postings.
    """
    token = bot_token or TELEGRAM_BOT_TOKEN or ADMIN_BOT_TOKEN
    target = TARGET_CHANNEL_ID
    target_clean = str(target).lstrip("@")

    # 1. Timing & Idempotency verification (unless forced)
    if not force:
        if not is_tajmi3at_time_window():
            logger.info("[TAJMI3AT] Current time is not within daily 10 PM window (21:30 - 22:45 Algiers time UTC+1). Skipping.")
            return []

        eligible, reason = is_daily_tajmi3at_eligible()
        if not eligible:
            logger.info(f"[TAJMI3AT] Daily tajmi3at not eligible: {reason}. Skipping.")
            return []

    logger.info("[TAJMI3AT] Starting Daily Tajmi3at roundup execution...")

    # 2. Fetch all active deals published to @DzAliexpress0 in the last 24h
    today_deals = get_recent_published_deals_for_roundup(max_age_hours=24.0)
    if not today_deals:
        logger.info("[TAJMI3AT] No deals published in the last 24h found in state. Skipping.")
        return []

    # 3. Filter out deals already regrouped (unless force)
    regrouped_ids = get_regrouped_channel_msg_ids()
    available_deals = [d for d in today_deals if d["channel_msg_id"] not in regrouped_ids] if not force else today_deals

    # 4. Group by category
    deals_by_category: Dict[str, List[Dict[str, Any]]] = {k: [] for k in CATEGORIES_CONFIG.keys()}
    other_deals: List[Dict[str, Any]] = []

    for d in available_deals:
        cat = d.get("category")
        if cat and cat in deals_by_category:
            deals_by_category[cat].append(d)
        else:
            other_deals.append(d)

    # 5. Check which categories meet the strict min_items threshold (default 4)
    qualifying_categories = [
        (cat, items) for cat, items in deals_by_category.items()
        if len(items) >= min_items
    ]
    # Sort by number of items descending (most abundant categories first)
    qualifying_categories.sort(key=lambda x: len(x[1]), reverse=True)

    published_bulletins: List[Dict[str, Any]] = []
    all_regrouped_msg_ids: List[int] = []

    banner_path = Path(settings.BASE_DIR) / "storage" / "assets" / "tajmi3at_banner.png"
    if not banner_path.exists():
        banner_path = Path(settings.BASE_DIR) / "assets" / "tajmi3at_banner.png"

    reply_markup = {
        "inline_keyboard": [
            [
                {"text": "🪙 فتح بوت تخفيض العملات", "url": "https://t.me/Alilo07BOT"}
            ],
            [
                {"text": "📢 قناة الصفقات المعتمدة", "url": f"https://t.me/{target_clean}"}
            ]
        ]
    }

    api_url = f"https://api.telegram.org/bot{token}"

    async with httpx.AsyncClient(timeout=25.0) as client:
        # CASE A: At least one category meets min_items (>= 4)
        if qualifying_categories:
            to_publish = qualifying_categories[:max_bulletins]
            for cat_name, cat_items in to_publish:
                bulletin_text, used_items = build_category_bulletin_text(cat_name, cat_items, target_clean)
                if not used_items:
                    continue

                sent_data = None
                # Send photo with caption
                if banner_path.exists() and len(bulletin_text) <= 1024:
                    with open(banner_path, "rb") as bf:
                        mime = "image/png" if banner_path.suffix.lower() == ".png" else "image/jpeg"
                        resp = await client.post(
                            f"{api_url}/sendPhoto",
                            data={
                                "chat_id": target,
                                "caption": bulletin_text,
                                "parse_mode": "HTML",
                                "reply_markup": json.dumps(reply_markup)
                            },
                            files={"photo": (banner_path.name, bf, mime)}
                        )
                        sent_data = resp.json()

                # Fallback to sendMessage if photo upload failed or text > 1024
                if not sent_data or not sent_data.get("ok"):
                    resp = await client.post(
                        f"{api_url}/sendMessage",
                        json={
                            "chat_id": target,
                            "text": bulletin_text,
                            "parse_mode": "HTML",
                            "disable_web_page_preview": True,
                            "reply_markup": reply_markup
                        }
                    )
                    sent_data = resp.json()

                if sent_data and sent_data.get("ok"):
                    b_msg_id = sent_data["result"]["message_id"]
                    used_ids = [it["channel_msg_id"] for it in used_items]
                    all_regrouped_msg_ids.extend(used_ids)

                    logger.info(f"[TAJMI3AT] Published {cat_name} bulletin #{b_msg_id} with {len(used_items)} items to {target}")
                    published_bulletins.append({
                        "category": cat_name,
                        "message_id": b_msg_id,
                        "count": len(used_items)
                    })
                    await asyncio.sleep(2.5)
                else:
                    logger.error(f"[TAJMI3AT] Failed to publish {cat_name} bulletin: {sent_data}")

        # CASE B: No single category reached 4 items, but we have >= 3 deals today
        elif len(available_deals) >= 3:
            logger.info(f"[TAJMI3AT] No category reached {min_items} items. Building Master Daily Roundup with {len(available_deals)} deals.")
            bulletin_text, used_items = build_master_daily_roundup_text(available_deals, target_clean)
            if used_items:
                sent_data = None
                if banner_path.exists() and len(bulletin_text) <= 1024:
                    with open(banner_path, "rb") as bf:
                        mime = "image/png" if banner_path.suffix.lower() == ".png" else "image/jpeg"
                        resp = await client.post(
                            f"{api_url}/sendPhoto",
                            data={
                                "chat_id": target,
                                "caption": bulletin_text,
                                "parse_mode": "HTML",
                                "reply_markup": json.dumps(reply_markup)
                            },
                            files={"photo": (banner_path.name, bf, mime)}
                        )
                        sent_data = resp.json()

                if not sent_data or not sent_data.get("ok"):
                    resp = await client.post(
                        f"{api_url}/sendMessage",
                        json={
                            "chat_id": target,
                            "text": bulletin_text,
                            "parse_mode": "HTML",
                            "disable_web_page_preview": True,
                            "reply_markup": reply_markup
                        }
                    )
                    sent_data = resp.json()

                if sent_data and sent_data.get("ok"):
                    b_msg_id = sent_data["result"]["message_id"]
                    used_ids = [it["channel_msg_id"] for it in used_items]
                    all_regrouped_msg_ids.extend(used_ids)

                    logger.info(f"[TAJMI3AT] Published Master Daily Roundup #{b_msg_id} with {len(used_items)} items to {target}")
                    published_bulletins.append({
                        "category": "master_roundup",
                        "message_id": b_msg_id,
                        "count": len(used_items)
                    })

    # 6. Record state & idempotency if any bulletin was published
    if published_bulletins:
        record_deals_regrouped(all_regrouped_msg_ids)
        record_daily_tajmi3at_published(bulletins_count=len(published_bulletins))
        logger.info(f"[TAJMI3AT] Successfully finished Daily Tajmi3at: {len(published_bulletins)} bulletin(s) published.")
    else:
        logger.info("[TAJMI3AT] No bulletins published during this cycle.")

    return published_bulletins

if __name__ == "__main__":
    force_mode = "--force" in sys.argv or "-f" in sys.argv
    print(f"Running check_and_publish_regrouped_bulletins(force={force_mode})...")
    res = asyncio.run(check_and_publish_regrouped_bulletins(force=force_mode))
    print(f"Result: {len(res)} bulletin(s) published: {res}")
