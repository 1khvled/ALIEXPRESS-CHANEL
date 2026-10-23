import os
import re
from typing import Optional, Tuple, Dict, Any
import httpx
from app.config.settings import settings
from app.utils.logger import logger, record_system_log


class FacebookPublisher:
    """
    Automated Facebook Page Publisher via Meta Graph API v21.0.
    Supports photo posts with rich formatted captions and feed link posts.
    """
    GRAPH_API_VERSION = "v21.0"
    GRAPH_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

    def __init__(
        self,
        page_id: Optional[str] = None,
        access_token: Optional[str] = None,
        app_id: Optional[str] = None,
        app_secret: Optional[str] = None,
        auto_post_enabled: Optional[bool] = None
    ):
        self.page_id = (
            page_id
            or getattr(settings, "FACEBOOK_PAGE_ID", None)
            or os.getenv("FACEBOOK_PAGE_ID", "")
        )
        self.access_token = (
            access_token
            or getattr(settings, "FACEBOOK_PAGE_ACCESS_TOKEN", None)
            or os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN", "")
        )
        self.app_id = (
            app_id
            or getattr(settings, "FACEBOOK_APP_ID", None)
            or os.getenv("FACEBOOK_APP_ID", "")
        )
        self.app_secret = (
            app_secret
            or getattr(settings, "FACEBOOK_APP_SECRET", None)
            or os.getenv("FACEBOOK_APP_SECRET", "")
        )
        self.auto_post_enabled = (
            auto_post_enabled
            if auto_post_enabled is not None
            else getattr(settings, "FACEBOOK_AUTO_POST_ENABLED", False)
        )

    def is_configured(self) -> bool:
        """Returns True if Page ID and Access Token are configured."""
        return bool(self.page_id and self.access_token)

    def format_caption_for_facebook(
        self,
        caption: str,
        deal_link: Optional[str] = None,
        price: Optional[float] = None
    ) -> str:
        """
        Converts Telegram HTML formatting into a clean, engaging Facebook post format:
        - Strips Telegram-specific HTML tags (<blockquote>, <b>, <code>)
        - Ensures purchase link is prominently visible and clickable
        - Appends relevant shopping and deal hashtags
        """
        if not caption:
            return ""

        text = caption

        # 1. Format blockquotes with a clean visual border
        text = re.sub(r'<blockquote>\s*', '✨ ', text, flags=re.IGNORECASE)
        text = re.sub(r'\s*</blockquote>', '\n', text, flags=re.IGNORECASE)

        # 2. Convert <code> tags to uppercase standout
        text = re.sub(r'<code>(.*?)</code>', r'[\1]', text, flags=re.IGNORECASE)

        # 3. Strip bold / italic / underline tags
        text = re.sub(r'</?(?:b|strong|i|em|u|s|strike)>', '', text, flags=re.IGNORECASE)

        # 4. Convert HTML links <a href="URL">text</a> to "text: URL" or "URL"
        def _replace_a(match):
            href = match.group(1)
            link_text = match.group(2).strip()
            if link_text and link_text != href:
                return f"{link_text} 👉 {href}"
            return href

        text = re.sub(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', _replace_a, text, flags=re.IGNORECASE)

        # Strip any other residual HTML tags
        text = re.sub(r'<[^>]+>', '', text)

        # Remove redundant multiple blank lines
        text = re.sub(r'\n{3,}', '\n\n', text).strip()

        # Ensure deal purchase link is clearly visible if provided and not already present
        if deal_link and deal_link not in text:
            text += f"\n\n🛒 رابط الشراء والتخفيض المباشر:\n{deal_link}"

        # Append high-converting Facebook hashtags for Algerian tech & deals
        hashtags = "\n\n#AliExpress #تخفيضات #عروض #الجزائر #تسوق_أونلاين #AliexpressDZ #ShoppingDZ"
        if "#aliexpress" not in text.lower():
            text += hashtags

        return text.strip()

    async def verify_page_token(self) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """
        Verifies credentials against the Meta Graph API and returns page metadata.
        """
        if not self.is_configured():
            return False, "Facebook Page ID or Access Token is missing.", None

        url = f"{self.GRAPH_URL}/{self.page_id}"
        params = {
            "fields": "id,name,link,can_post,tasks",
            "access_token": self.access_token
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(url, params=params)
                data = resp.json()

                if resp.status_code == 200 and "id" in data:
                    logger.info(f"[FACEBOOK] Page token verified successfully: '{data.get('name')}' (ID: {data.get('id')})")
                    return True, None, data
                else:
                    err_msg = data.get("error", {}).get("message", f"HTTP {resp.status_code}")
                    err_type = data.get("error", {}).get("type", "OAuthException")
                    logger.warning(f"[FACEBOOK] Verification failed: [{err_type}] {err_msg}")
                    return False, f"[{err_type}] {err_msg}", data
        except Exception as e:
            logger.error(f"[FACEBOOK] Error verifying page token: {e}")
            return False, str(e), None

    async def exchange_for_long_lived_token(self, short_token: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Exchanges a short-lived user/page access token for a long-lived access token (60 days or permanent).
        Requires FACEBOOK_APP_ID and FACEBOOK_APP_SECRET.
        """
        if not self.app_id or not self.app_secret:
            return False, None, "App ID or App Secret is required to exchange for a long-lived token."

        url = f"{self.GRAPH_URL}/oauth/access_token"
        params = {
            "grant_type": "fb_exchange_token",
            "client_id": self.app_id,
            "client_secret": self.app_secret,
            "fb_exchange_token": short_token
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(url, params=params)
                data = resp.json()
                if resp.status_code == 200 and "access_token" in data:
                    long_lived = data["access_token"]
                    logger.info("[FACEBOOK] Successfully exchanged short-lived token for long-lived token.")
                    return True, long_lived, None
                else:
                    err = data.get("error", {}).get("message", str(data))
                    return False, None, err
        except Exception as e:
            return False, None, str(e)

    async def publish_deal(
        self,
        caption: str,
        deal_link: Optional[str] = None,
        image_url: Optional[str] = None,
        price: Optional[float] = None,
        title: Optional[str] = None
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Publishes a deal post to the Facebook Page:
        - If image_url is provided and valid, posts to /{PAGE_ID}/photos with image + caption.
        - Otherwise, posts to /{PAGE_ID}/feed with message + link.

        Returns: (success: bool, post_id: Optional[str], error_message: Optional[str])
        """
        if not self.is_configured():
            return False, None, "Facebook Publisher is not configured (missing Page ID or Page Access Token)."

        fb_message = self.format_caption_for_facebook(caption, deal_link=deal_link, price=price)

        async with httpx.AsyncClient(timeout=20.0) as client:
            # 1. Image post if image_url is available
            if image_url and image_url.startswith("http"):
                photo_url = f"{self.GRAPH_URL}/{self.page_id}/photos"
                payload = {
                    "url": image_url,
                    "caption": fb_message,
                    "access_token": self.access_token
                }
                try:
                    resp = await client.post(photo_url, data=payload)
                    data = resp.json()

                    if resp.status_code in (200, 201) and ("id" in data or "post_id" in data):
                        post_id = data.get("post_id") or data.get("id")
                        logger.info(f"[FACEBOOK] Published photo deal successfully! Post ID: {post_id}")
                        record_system_log("INFO", f"Published deal to Facebook Page (Photo ID: {post_id})")
                        return True, str(post_id), None
                    else:
                        err_data = data.get("error", {})
                        err_msg = err_data.get("message", f"HTTP {resp.status_code}: {resp.text}")
                        logger.warning(f"[FACEBOOK] Photo upload failed, falling back to feed post. Reason: {err_msg}")
                        # Fallback to feed post with link if image upload failed
                except Exception as e:
                    logger.warning(f"[FACEBOOK] Exception during photo post ({e}), falling back to feed post.")

            # 2. Feed post fallback (Text + Link)
            feed_url = f"{self.GRAPH_URL}/{self.page_id}/feed"
            payload = {
                "message": fb_message,
                "access_token": self.access_token
            }
            if deal_link and deal_link.startswith("http"):
                payload["link"] = deal_link

            try:
                resp = await client.post(feed_url, data=payload)
                data = resp.json()

                if resp.status_code in (200, 201) and "id" in data:
                    post_id = data["id"]
                    logger.info(f"[FACEBOOK] Published feed deal successfully! Post ID: {post_id}")
                    record_system_log("INFO", f"Published deal to Facebook Page (Feed ID: {post_id})")
                    return True, str(post_id), None
                else:
                    err_data = data.get("error", {})
                    err_msg = err_data.get("message", f"HTTP {resp.status_code}: {resp.text}")
                    err_code = err_data.get("code")
                    logger.error(f"[FACEBOOK] Feed post failed: [{err_code}] {err_msg}")
                    return False, None, f"[{err_code}] {err_msg}"
            except Exception as e:
                logger.error(f"[FACEBOOK] Network error during post: {e}")
                return False, None, str(e)


facebook_publisher = FacebookPublisher()
