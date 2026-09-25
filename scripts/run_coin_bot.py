"""
Standalone AliExpress Coin & Discount Bot Runner (Long-Polling Mode)
Run this script to test or host the bot locally on your PC.
"""
import asyncio
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

import httpx
from app.config.settings import settings
from app.telegram.coin_bot import handle_telegram_update

async def run_bot():
    token = settings.TELEGRAM_BOT_TOKEN
    if not token:
        print("[!] Error: TELEGRAM_BOT_TOKEN is not configured!")
        return

    print("=" * 60)
    print("ALIEXPRESS COIN & DISCOUNT BOT (LONG-POLLING)")
    print(f"Tracking ID: {settings.ALIEXPRESS_AFFILIATE_TRACKING_ID}")
    print("=" * 60)

    # Get bot info
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(f"https://api.telegram.org/bot{token}/getMe")
        if r.status_code == 200:
            bot_info = r.json().get("result", {})
            print(f"[*] Connected as @{bot_info.get('username')} ({bot_info.get('first_name')})")
        else:
            print(f"[!] Failed to connect: {r.text}")
            return

        # Delete any existing webhook to enable long-polling
        await client.post(f"https://api.telegram.org/bot{token}/deleteWebhook")

    offset = 0
    print("[*] Bot is listening for messages... Press Ctrl+C to stop.")

    async with httpx.AsyncClient(timeout=35.0) as client:
        while True:
            try:
                resp = await client.get(
                    f"https://api.telegram.org/bot{token}/getUpdates",
                    params={"offset": offset, "timeout": 25}
                )
                if resp.status_code == 200:
                    data = resp.json()
                    for update in data.get("result", []):
                        offset = update["update_id"] + 1
                        msg = update.get("message", {})
                        user = msg.get("from", {}).get("first_name", "User")
                        text = msg.get("text", "")
                        print(f"--> Received message from {user}: {text[:50]}")
                        asyncio.create_task(handle_telegram_update(update))
                else:
                    await asyncio.sleep(2.0)
            except httpx.TimeoutException:
                continue
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"[!] Polling error: {e}")
                await asyncio.sleep(3.0)

if __name__ == "__main__":
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        print("\n[*] Bot stopped by user.")
