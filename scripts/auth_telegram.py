import asyncio
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from telethon import TelegramClient
from app.config.settings import settings

async def main():
    print("=" * 60)
    print("Telegram MTProto Collector Authentication Helper")
    print("=" * 60)

    api_id = settings.TELEGRAM_API_ID
    api_hash = settings.TELEGRAM_API_HASH

    if not api_id or not api_hash:
        print("\nERROR: TELEGRAM_API_ID and TELEGRAM_API_HASH must be set in your .env file.")
        print("You can get them from: https://my.telegram.org/apps\n")
        return

    session_path = str(settings.SESSIONS_DIR / settings.TELEGRAM_SESSION_NAME)
    print(f"\nTarget session path: {session_path}.session")

    client = TelegramClient(session_path, api_id, api_hash)
    await client.start(phone=settings.TELEGRAM_PHONE)

    me = await client.get_me()
    print(f"\n[SUCCESS] Successfully logged in as: {me.first_name} (@{me.username}) [ID: {me.id}]")
    print("Session file has been saved. The background collector can now access channels.\n")

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
