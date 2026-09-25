import re
from typing import Optional
from app.config.settings import settings
from app.ai.prompts import POST_SYSTEM_PROMPT
from app.utils.logger import logger

class DealCaptionGenerator:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.model = model or settings.AI_MODEL

    def _format_deterministic(
        self,
        title: str,
        usd_price: float,
        eur_price: float,
        affiliate_url: str,
        coupon_code: Optional[str] = None,
        has_points_discount: bool = False
    ) -> str:
        """
        Builds the exact Arabic Telegram post format deterministically with zero hallucination.
        """
        lines = [
            "العرض مستمر 🚨",
            f"تخفيض لـ {title}",
            f"السعر : {usd_price:.2f}$ ({eur_price:.2f}€)🔥",
            f"رابط {affiliate_url}"
        ]

        if coupon_code:
            lines.append(f"كوبون : {coupon_code}")

        if has_points_discount:
            lines.append("خصم النقاط")

        lines.append("")
        lines.append("لا تنسى استخدام البوت للشراء بأقل الأسعار")

        return "\n".join(lines)

    async def generate(
        self,
        title: str,
        usd_price: float,
        eur_price: float,
        affiliate_url: str,
        coupon_code: Optional[str] = None,
        has_points_discount: bool = False
    ) -> str:
        """
        Generates clean Arabic Telegram caption matching project requirements.
        Uses OpenAI when configured to optimize title clarity, otherwise uses deterministic builder.
        """
        clean_title = title.strip() if title else "منتج مميز"

        # If OpenAI is configured, we can clean up bloated AliExpress product titles
        if self.api_key:
            try:
                import httpx
                payload = {
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "Clean and shorten this product title into a concise, attractive name (English or Arabic, max 6 words). Return only the cleaned title, nothing else."},
                        {"role": "user", "content": clean_title}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 50
                }
                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers={"Authorization": f"Bearer {self.api_key}"},
                        json=payload
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        refined = data["choices"][0]["message"]["content"].strip().strip('"\'')
                        if len(refined) >= 3:
                            clean_title = refined
            except Exception as e:
                logger.warning(f"AI title optimization failed, using original title: {e}")

        return self._format_deterministic(
            title=clean_title,
            usd_price=usd_price,
            eur_price=eur_price,
            affiliate_url=affiliate_url,
            coupon_code=coupon_code,
            has_points_discount=has_points_discount
        )

caption_generator = DealCaptionGenerator()
