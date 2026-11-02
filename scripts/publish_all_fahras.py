import sys
import os
import json
import asyncio
import argparse
from datetime import datetime, timezone
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
from app.publisher.state_tracker import (
    load_persistent_state,
    save_persistent_state,
    record_post_published
)

async def publish_bulletin(client, api_url, target, banner_path, bulletin_text, reply_markup, category_name):
    vis_len = get_telegram_visible_len(bulletin_text)
    print(f"\n--- Publishing {category_name} (vis_len: {vis_len}) ---")
    
    sent_data = None
    if banner_path and banner_path.exists() and vis_len <= 1024:
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
        new_id = sent_data["result"]["message_id"]
        print(f"✅ Published {category_name} -> #{new_id}")
        return new_id
    else:
        print(f"❌ Failed to publish {category_name}: {sent_data}")
        return None

async def main():
    parser = argparse.ArgumentParser(description="Publish category Fahras / Tajmi3at bulletins")
    parser.add_argument("--category", choices=["all", "phones", "headsets", "pc_parts", "chargers"], default="all")
    parser.add_argument("--force", "-f", action="store_true", help="Force publication bypassing 12h cooldown")
    args = parser.parse_args()

    token = getattr(settings, "TELEGRAM_BOT_TOKEN", "") or os.getenv("TELEGRAM_BOT_TOKEN", "")
    target = getattr(settings, "TARGET_CHANNEL_ID", "@DzAliexpress0") or os.getenv("TARGET_CHANNEL_ID", "@DzAliexpress0")
    clean_target = str(target).lstrip("@")
    api_url = f"https://api.telegram.org/bot{token}"

    base_dir = Path(__file__).resolve().parent.parent
    banner_path = base_dir / "storage" / "assets" / "tajmi3at_banner.png"
    if not banner_path.exists():
        banner_path = base_dir / "assets" / "tajmi3at_banner.png"

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

    state = load_persistent_state()
    fahras_history = state.get("daily_fahras_history", {})
    now_ts = datetime.now(timezone.utc).timestamp()
    cooldown_sec = 12 * 3600 # 12 hours cooldown per bulletin

    deals = get_recent_published_deals_for_roundup(max_age_hours=48.0, min_msg_id=1411)
    print(f"Found {len(deals)} published deals (all >= #1411)")

    bulletins_to_post = []

    # 1. PHONES
    if args.category in ("all", "phones"):
        phones = [d for d in deals if d.get('category') == 'phones']
        p1_text, used_p1 = build_category_bulletin_text('phones', phones, clean_target, part=1, total_parts=2)
        used_p1_ids = {it['channel_msg_id'] for it in used_p1}
        remaining_phones = [p for p in phones if p['channel_msg_id'] not in used_p1_ids]
        p2_text, used_p2 = build_category_bulletin_text('phones', remaining_phones, clean_target, part=2, total_parts=2)
        if used_p1:
            bulletins_to_post.append(("Phones Part 1", p1_text, used_p1))
        if used_p2:
            bulletins_to_post.append(("Phones Part 2", p2_text, used_p2))

    # 2. HEADSETS / AUDIO GEAR
    if args.category in ("all", "headsets"):
        headsets = [d for d in deals if d.get('category') == 'headsets']
        h_text, used_h = build_category_bulletin_text('headsets', headsets, clean_target)
        if used_h:
            bulletins_to_post.append(("Headsets & Audio", h_text, used_h))

    # 3. PC PARTS
    if args.category in ("all", "pc_parts"):
        pc_parts = [d for d in deals if d.get('category') == 'pc_parts']
        pc_text, used_pc = build_category_bulletin_text('pc_parts', pc_parts, clean_target)
        if used_pc:
            bulletins_to_post.append(("PC Parts & CPUs", pc_text, used_pc))

    # 4. CHARGERS & POWER
    if args.category in ("all", "chargers"):
        chargers = [d for d in deals if d.get('category') == 'chargers_cables']
        ch_text, used_ch = build_category_bulletin_text('chargers_cables', chargers, clean_target)
        if used_ch:
            bulletins_to_post.append(("Chargers & Power", ch_text, used_ch))

    async with httpx.AsyncClient(timeout=30.0) as client:
        for name, text, used_items in bulletins_to_post:
            norm_key = name.lower().replace(" ", "_")
            last_pub = fahras_history.get(norm_key, 0)
            if (now_ts - last_pub) < cooldown_sec and not args.force:
                print(f"⏩ Skipping {name}: already published {int((now_ts - last_pub)/60)}m ago (cooldown 12h). Use --force to override.")
                continue

            msg_id = await publish_bulletin(client, api_url, target, banner_path, text, reply_markup, name)
            if msg_id:
                fahras_history[norm_key] = now_ts
                state["daily_fahras_history"] = fahras_history
                save_persistent_state(state)

                used_ids = [it['channel_msg_id'] for it in used_items]
                record_deals_regrouped(used_ids)
                record_post_published(
                    channel_username=clean_target,
                    message_id=msg_id,
                    product_id=f"FAHRAS_{name.upper().replace(' ', '_')}_{msg_id}",
                    title=f"فهرس {name}",
                    channel_msg_id=msg_id
                )
            await asyncio.sleep(2.0)

if __name__ == "__main__":
    asyncio.run(main())
