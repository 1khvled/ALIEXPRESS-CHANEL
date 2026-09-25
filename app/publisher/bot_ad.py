"""
Daily 24-Hour Bot Advertisement Poster
Publishes high-converting promotional posts for @Alilo07BOT to the channel.
Automatically throttled to post once every 24 hours.
"""
import asyncio
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional, Tuple
import json
import httpx
from sqlalchemy import select

from app.config.settings import settings
from app.db.session import db_context
from app.db.models import Deal, TelegramPost, SourceMessage
from app.utils.logger import logger, record_system_log

AD_CAPTION = """🪙 <b>طريقة الشراء بأرخص سعر من AliExpress عبر العملات (Coins) 💸</b>

الكثير من المتسوقين لا يعلمون أن تطبيق AliExpress يمنحك تخفيضات إضافية ضخمة عبر <b>العملات الذهبية (Coins)</b> قد تصل إلى أكثر من <b>50% إلى 70% خصم إضافي</b> على أي منتج! 🤑

🤔 <b>كيف تفعّل هذا التخفيض الأكبر وتجمع العملات يومياً مجاناً؟</b>
وفرنا لكم أداتين حصريتين مجانيتين لمتابعي القناة:

1️⃣ 🤖 <b>بوت تخفيض الروابط الفوري (@Alilo07BOT):</b>
أرسل له أي رابط منتج من AliExpress وسيحوله لك فوراً لأقصى خصم عملات وسوبر ديلز! 🚀

2️⃣ ⚡ <b>جامع العملات التلقائي اليومي (Daily Coin Collector):</b>
سكريبت مجاني يجمع لك 70 إلى 100 قطعة نقدية يومياً في الخلفية من حاسوبك دون تعب!
🔗 رابط المشروع على GitHub: https://github.com/1khvled/COIN-BOT-

🇰🇷 <b>نصيحة ذهبية:</b> لا تنس تحويل دولة التطبيق إلى كندا 🇨🇦 أو كوريا 🇰🇷 لتفعيل أكبر نسب تخفيض بالعملات!

💡 <i>الأدوات مجانية 100% لمتابعي قناتنا. جربها الآن ووفر في كل طلبية!</i> 👇"""

async def post_bot_advertisement(force: bool = False) -> Tuple[bool, Optional[str]]:
    """
    Publishes the @Alilo07BOT advertisement to the Telegram channel.
    Enforces a strict 24-hour interval unless force=True.
    """
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=24)

    async with db_context() as session:
        # Check when the last bot ad was published
        last_ad_deal = (await session.execute(
            select(Deal).where(Deal.product_id == "BOT_PROMO_AD").order_by(Deal.created_at.desc()).limit(1)
        )).scalar_one_or_none()

        if not force and last_ad_deal and last_ad_deal.created_at:
            # Handle tz-aware vs naive
            ad_time = last_ad_deal.created_at
            if ad_time.tzinfo is None:
                ad_time = ad_time.replace(tzinfo=timezone.utc)
            if ad_time > cutoff:
                remaining = (ad_time + timedelta(hours=24)) - now
                hours_left = max(0.1, remaining.total_seconds() / 3600.0)
                return False, f"Daily bot ad already posted. Next ad in {hours_left:.1f} hours."

        # Prepare banner image
        banner_path = settings.BASE_DIR / "assets" / "bot_promo_banner.jpg"
        if not banner_path.exists():
            banner_path = settings.BASE_DIR / "assets" / "logo.png"

        bot_token = settings.TELEGRAM_BOT_TOKEN
        target_channel = settings.TARGET_CHANNEL_ID
        if not bot_token or not target_channel:
            return False, "Bot credentials not configured"

        # Prepare inline keyboard
        reply_markup = {
            "inline_keyboard": [
                [
                    {"text": "🪙 جرب بوت تخفيض العملات @Alilo07BOT", "url": "https://t.me/Alilo07BOT"}
                ],
                [
                    {"text": "⚡ كود جامع العملات اليومي (GitHub)", "url": "https://github.com/1khvled/COIN-BOT-"}
                ],
                [
                    {
                        "text": "🔄 شارك البوت والقناة مع أصدقائك",
                        "url": "https://t.me/share/url?url=https://t.me/DzAliexpress0&text=أقوى عروض وتخفيضات AliExpress بالعملات 🪙🔥"
                    }
                ]
            ]
        }
        reply_markup_json = json.dumps(reply_markup)

        # Send to Telegram
        api_url = f"https://api.telegram.org/bot{bot_token}"
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                if banner_path.exists():
                    with open(banner_path, "rb") as f:
                        data = {
                            "chat_id": target_channel,
                            "caption": AD_CAPTION,
                            "parse_mode": "HTML",
                            "reply_markup": reply_markup_json
                        }
                        files = {"photo": f}
                        resp = await client.post(f"{api_url}/sendPhoto", data=data, files=files)
                else:
                    data = {
                        "chat_id": target_channel,
                        "text": AD_CAPTION,
                        "parse_mode": "HTML",
                        "reply_markup": reply_markup_json
                    }
                    resp = await client.post(f"{api_url}/sendMessage", data=data)

                result = resp.json()
                if resp.status_code == 200 and result.get("ok"):
                    msg_id = result.get("result", {}).get("message_id")

                    # Record in DB
                    deal = Deal(
                        product_id="BOT_PROMO_AD",
                        original_url="https://t.me/Alilo07BOT",
                        normalized_url="https://t.me/Alilo07BOT",
                        affiliate_url="https://t.me/Alilo07BOT",
                        title="إعلان بوت تخفيض العملات @Alilo07BOT",
                        quality_score=100,
                        status="PUBLISHED"
                    )
                    session.add(deal)
                    await session.flush()

                    post = TelegramPost(
                        deal_id=deal.id,
                        telegram_message_id=msg_id,
                        channel_id=str(target_channel),
                        status="PUBLISHED",
                        published_at=now,
                        permalink=f"https://t.me/{str(target_channel).lstrip('@')}/{msg_id}"
                    )
                    session.add(post)
                    await session.commit()

                    logger.info(f"Published daily @Alilo07BOT advertisement to {target_channel} (msg #{msg_id})")
                    await record_system_log("INFO", "publisher", f"Published daily bot ad to {target_channel} (msg #{msg_id})")
                    return True, None
                else:
                    err = result.get("description", f"HTTP {resp.status_code}")
                    logger.error(f"Failed to publish bot ad: {err}")
                    return False, err

        except Exception as e:
            logger.exception(f"Exception publishing bot ad: {e}")
            return False, str(e)
