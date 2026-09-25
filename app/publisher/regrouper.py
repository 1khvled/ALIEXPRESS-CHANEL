"""
Auto-Regrouping Bulletin Algorithm
Automatically aggregates published deals of the exact same category (e.g. 4+ Phones, 4+ Mice, 4+ Keyboards)
into a high-converting index bulletin linking back to the channel's own posts.
Strict Rule: Minimum 4 items required. Anything less than 4 is ignored.
"""
import os
import json
import re
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Tuple, Optional
import httpx
from sqlalchemy import select

from app.config.settings import settings
from app.db.session import db_context
from app.db.models import Deal, TelegramPost
from app.utils.logger import logger

TARGET_CHANNEL_ID = os.getenv("TARGET_CHANNEL_ID", "@DzAliexpress0")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8900887118:AAFuAFcxS1Xa2K4g0tlpD_YutPrsco3Y-Vo")
ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN", "8708965924:AAGi9HgLDxKsvaOzPOnCDRhI4c9WAfUvkOk")

# Persistence tracking for already regrouped deals so we don't repeat the exact same bulletin
_REGROUP_STATE_FILE = "/tmp/regrouped_deals.json" if os.path.exists("/tmp") else os.path.join(os.path.dirname(__file__), "regrouped_deals.json")

CATEGORIES_CONFIG = {
    "phones": {
        "header": "⚡⚡ الهواتف الذكية الأكثر طلباً ومبيعاً 📱⚡⚡",
        "keywords": [
            "phone", "smartphone", "هاتف", "جوال", "موبايل", "poco", "redmi",
            "realme", "honor", "samsung", "infinix", "oppo", "vivo", "iphone",
            "nubia", "zte", "motorola", "iqoo"
        ],
        "negative_keywords": [
            "headset", "earphone", "case", "cover", "holder", "charger",
            "cable", "cooler", "mousepad", "screen protector"
        ]
    },
    "mice": {
        "header": "⚡⚡ أفضل صيدات الماوسات القيمنق 🖱️⚡⚡",
        "keywords": [
            "mouse", "mice", "ماوس", "فأرة", "فارة", "attack shark x3",
            "attack shark r1", "attack shark x1", "ajazz aj", "vxe r1", "scyrox"
        ],
        "negative_keywords": [
            "mousepad", "mouse pad", "pad", "باد", "باد ماوس"
        ]
    },
    "keyboards": {
        "header": "⚡⚡ أقوى عروض الكيبوردات الميكانيكية ⌨️⚡⚡",
        "keywords": [
            "keyboard", "كيبورد", "لوحة مفاتيح", "ak820", "rainy75", "hi75",
            "crush80", "aula f75", "aula f87", "mechanical keyboard"
        ],
        "negative_keywords": []
    },
    "headsets": {
        "header": "⚡⚡ أقوى عروض السماعات القيمنق والصوتيات 🎧⚡⚡",
        "keywords": [
            "headset", "headphone", "earbuds", "earphone", "tws",
            "سماعة", "سماعات", "سماعة محيطية", "attack shark l90", "attack shark l80"
        ],
        "negative_keywords": []
    },
    "tablets": {
        "header": "⚡⚡ أفضل عروض أجهزة التابلت والايباد 📟⚡⚡",
        "keywords": [
            "tablet", "tab", "pad", "ipad", "تابلت", "ايباد", "لوحي",
            "xiaomi pad", "redmi pad", "realme pad"
        ],
        "negative_keywords": [
            "mousepad", "mouse pad", "thermal pad", "ptm7950"
        ]
    },
    "pc_parts": {
        "header": "⚡⚡ أقوى عروض قطع البي سي والعتاد 🖥️⚡⚡",
        "keywords": [
            "ram", "ssd", "nvme", "gpu", "graphics card", "cooler", "thermal pad",
            "ptm7950", "كارت شاشة", "كرت شاشة", "معالج", "مشتت", "رام", "ddr4", "ddr5"
        ],
        "negative_keywords": []
    },
    "smartwatches": {
        "header": "⚡⚡ أفضل عروض الساعات الذكية ⌚⚡⚡",
        "keywords": [
            "smartwatch", "smart watch", "smart band", "ساعة ذكية", "ساعة",
            "سوار ذكي", "colmi", "zeblaze", "amazfit"
        ],
        "negative_keywords": []
    }
}

def _load_regrouped_ids() -> set:
    try:
        if os.path.exists(_REGROUP_STATE_FILE):
            with open(_REGROUP_STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return set(data)
    except Exception:
        pass
    return set()

def _save_regrouped_ids(ids: set):
    try:
        with open(_REGROUP_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(list(ids), f)
    except Exception:
        pass

def classify_deal_category(title: str, text: str = "") -> Optional[str]:
    """Strictly classifies a deal into a primary homogeneous product category using word boundaries."""
    if not title:
        return None

    # Exclude multi-accessory combo packs (e.g. بوشات / كابل / ماوس / قلم)
    if title.count("/") >= 3:
        return None

    combined = f"{title or ''} {text or ''}".lower()

    # Prioritize specific devices (tablets first before phones so 'realme pad' is tablet)
    priority_order = ["tablets", "keyboards", "mice", "headsets", "phones", "pc_parts", "smartwatches"]

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
    return t[:48]

async def check_and_publish_regrouped_bulletins(bot_token: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Checks recent published channel posts.
    If 4 or more deals belong to the EXACT SAME category and haven't been regrouped yet,
    publishes a clean roundup bulletin matching the reference design.
    """
    token = bot_token or ADMIN_BOT_TOKEN or TELEGRAM_BOT_TOKEN
    target = TARGET_CHANNEL_ID
    regrouped_ids = _load_regrouped_ids()

    # 1. Fetch recent published deals with their channel message IDs
    deals_by_category: Dict[str, List[Dict[str, Any]]] = {k: [] for k in CATEGORIES_CONFIG.keys()}

    async with db_context() as s:
        # Get last 50 published deals with TelegramPost records
        query = (
            select(Deal, TelegramPost)
            .join(TelegramPost, Deal.id == TelegramPost.deal_id)
            .where(TelegramPost.telegram_message_id.isnot(None))
            .where(TelegramPost.telegram_message_id > 0)
            .order_by(Deal.id.desc())
            .limit(60)
        )
        results = (await s.execute(query)).all()

        for deal, post in results:
            if deal.id in regrouped_ids:
                continue

            msg_id = post.telegram_message_id
            if not msg_id or msg_id <= 0:
                continue

            category = classify_deal_category(deal.title or "")
            if not category:
                continue

            deals_by_category[category].append({
                "deal_id": deal.id,
                "title": clean_item_title(deal.title),
                "price": deal.current_price or 0.0,
                "message_id": msg_id,
                "channel_url": f"https://t.me/{str(target).lstrip('@')}/{msg_id}"
            })

    # 2. Check each category: STRICT RULE -> ONLY IF >= 4 items
    published_bulletins = []

    for cat_name, items in deals_by_category.items():
        if len(items) < 4:
            # "anything less then 4 dont do it it must be same thing"
            continue

        # Take up to 7 items of the exact same category
        selected_items = items[:7]
        cat_config = CATEGORIES_CONFIG[cat_name]

        # 3. Build Bulletin post matching user screenshot format
        lines = [
            cat_config["header"],
            "━━━━━━━━━━━━━━━━━"
        ]

        for item in selected_items:
            price_str = f"${int(item['price'])}" if item['price'].is_integer() else f"${item['price']:.2f}"
            lines.append(f"🔻 <b>{item['title']}</b> بسعر <b>{price_str}</b>")
            lines.append(f"🔗 {item['channel_url']}\n")

        lines.append("━━━━━━━━━━━━━━━━━")
        lines.append("💡 <i>اضغط على روابط المنتجات أعلاه للشراء بأقل سعر.</i>")
        lines.append("🪙 استخدم بوت DealScoutDz لزيادة تخفيض العملات: @Alilo07BOT")

        bulletin_text = "\n".join(lines)

        reply_markup = {
            "inline_keyboard": [
                [
                    {"text": "🪙 بوت تخفيض العملات DealScoutDz", "url": "https://t.me/Alilo07BOT"}
                ],
                [
                    {"text": "📢 تابع أحدث العروض @DzAliexpress0", "url": "https://t.me/DzAliexpress0"}
                ]
            ]
        }

        # 4. Publish to channel
        api_url = f"https://api.telegram.org/bot{token}"
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
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
                data = resp.json()
                if resp.status_code == 200 and data.get("ok"):
                    bulletin_msg_id = data["result"]["message_id"]
                    # Mark these deal IDs as regrouped
                    for it in selected_items:
                        regrouped_ids.add(it["deal_id"])
                    _save_regrouped_ids(regrouped_ids)

                    logger.info(f"Published {cat_name} regrouped bulletin #{bulletin_msg_id} with {len(selected_items)} items to {target}")
                    published_bulletins.append({
                        "category": cat_name,
                        "message_id": bulletin_msg_id,
                        "count": len(selected_items)
                    })
                else:
                    logger.error(f"Failed to publish regrouped bulletin for {cat_name}: {data}")
        except Exception as e:
            logger.exception(f"Error publishing {cat_name} bulletin: {e}")

    return published_bulletins
