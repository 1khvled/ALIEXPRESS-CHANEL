import sys
import json
import asyncio
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import httpx
from app.config.settings import settings
from app.publisher.regrouper import (
    get_recent_published_deals_for_roundup,
    build_category_bulletin_text,
    get_telegram_visible_len,
    record_deals_regrouped
)
from app.publisher.state_tracker import load_persistent_state, record_post_published

async def main():
    token = getattr(settings, "TELEGRAM_BOT_TOKEN", "")
    target = getattr(settings, "TARGET_CHANNEL_ID", "@DzAliexpress0")
    clean_target = str(target).lstrip("@")

    print(f"Target Channel: {target}")
    deals = get_recent_published_deals_for_roundup(max_age_hours=48.0)
    pc_deals = [d for d in deals if d.get('category') == 'pc_parts']
    print(f"Found {len(pc_deals)} published PC deals on {target}")

    bulletin_text, used_items = build_category_bulletin_text('pc_parts', pc_deals, clean_target)
    vis_len = get_telegram_visible_len(bulletin_text)
    print(f"Bulletin visible length: {vis_len} chars (limit 1024)")
    print(f"Items included: {len(used_items)}")

    banner_path = Path("D:/Projects/TELEGRAM_REPO/storage/assets/tajmi3at_banner.png")
    if not banner_path.exists():
        banner_path = Path("D:/Projects/TELEGRAM_REPO/assets/tajmi3at_banner.png")
    print(f"Banner exists: {banner_path.exists()} ({banner_path})")

    reply_markup = {
        "inline_keyboard": [
            [
                {"text": "🪙 فتح بوت تخفيض العملات", "url": "https://t.me/Alilo07BOT"}
            ],
            [
                {"text": "📢 قناة الصفقات المعتمدة", "url": f"https://t.me/{clean_target}"}
            ]
        ]
    }

    api_url = f"https://api.telegram.org/bot{token}"
    async with httpx.AsyncClient(timeout=30.0) as client:
        sent_data = None
        if banner_path.exists() and vis_len <= 1024:
            print("Sending as sendPhoto with banner...")
            with open(banner_path, "rb") as bf:
                resp = await client.post(
                    f"{api_url}/sendPhoto",
                    data={
                        "chat_id": target,
                        "caption": bulletin_text,
                        "parse_mode": "HTML",
                        "reply_markup": json.dumps(reply_markup)
                    },
                    files={"photo": (banner_path.name, bf, "image/png")}
                )
                sent_data = resp.json()
        
        if not sent_data or not sent_data.get("ok"):
            print(f"sendPhoto failed or skipped ({sent_data}). Fallback to sendMessage...")
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

        print("Telegram API response:", sent_data)
        if sent_data and sent_data.get("ok"):
            new_msg_id = sent_data["result"]["message_id"]
            print(f"\n SUCCESS! Published native Tajmi3a bulletin as message #{new_msg_id} on {target}!")
            used_ids = [it["channel_msg_id"] for it in used_items]
            record_deals_regrouped(used_ids)
            record_post_published(
                channel_username=clean_target,
                message_id=new_msg_id,
                product_id=f"TAJMI3A_PC_PARTS_{new_msg_id}",
                title="فهرس عروض قطع وعتاد البي سي",
                channel_msg_id=new_msg_id
            )
            return new_msg_id
        else:
            print(f"\n Failed to publish: {sent_data}")
            return None

if __name__ == "__main__":
    res = asyncio.run(main())
    print("Done. Message ID:", res)
