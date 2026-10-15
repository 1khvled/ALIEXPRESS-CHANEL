"""
CLI Runner to publish website promotional marketing posts to Telegram channels.
Usage:
    python scripts/post_website_promo.py --channel both
    python scripts/post_website_promo.py --channel dz
    python scripts/post_website_promo.py --channel fr
"""
import sys
import argparse
import asyncio
from pathlib import Path

# Configure utf-8 stdout for Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Add repo root to sys.path
repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))

from app.publisher.website_promo import publish_website_promo

async def main():
    parser = argparse.ArgumentParser(description="Publish DealScout DZ website marketing to Telegram")
    parser.add_argument(
        "--channel",
        choices=["dz", "fr", "both"],
        default="both",
        help="Target channel: dz (@DzAliexpress0), fr (@francedealsdz), or both"
    )
    args = parser.parse_args()

    print(f"🚀 Publishing DealScout DZ marketing campaign to channel(s): {args.channel}...")
    results = await publish_website_promo(channel=args.channel)
    print("\n📊 Campaign Results:")
    for ch, res in results.items():
        if res.get("status") == "success":
            print(f"  ✅ [{ch.upper()}] Successfully published to {res.get('channel')}: {res.get('link')}")
        else:
            print(f"  ❌ [{ch.upper()}] Failed: {res}")

if __name__ == "__main__":
    asyncio.run(main())
