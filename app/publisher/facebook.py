import os
import re
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
import httpx
from app.config.settings import settings
from app.utils.logger import logger, record_system_log

try:
    from app.utils.network import enforce_ipv4
    enforce_ipv4()
except Exception:
    pass


def get_high_res_aliexpress_image(url: Optional[str]) -> Optional[str]:
    """
    Transforms any AliExpress image URL into its highest possible master resolution:
    - Strips thumbnail sizing suffixes: _50x50.jpg, _220x220.jpg, _350x350.jpg, _640x640.jpg, etc.
    - Strips WebP compression wrappers: _.webp, _Q90.jpg_, etc.
    - Preserves clean original JPG/PNG image from AliExpress/Alibaba CDN.
    """
    if not url or not isinstance(url, str):
        return None
    clean_url = url.strip()
    if not clean_url.startswith("http"):
        return clean_url

    # Check if this is an AliExpress / Alibaba CDN image
    if any(domain in clean_url for domain in ["alicdn.com", "aliexpress-media.com", "aliexpress.com"]):
        # Match base image ending in .jpg, .jpeg, or .png
        m = re.match(r'^(https?://[^?#]+?\.(?:jpg|jpeg|png))', clean_url, flags=re.IGNORECASE)
        if m:
            return m.group(1)

    return clean_url


class FacebookPublisher:
    """
    Automated Facebook Page Publisher via Meta Graph API v21.0.
    Supports photo posts with rich formatted captions, master-studio CDN image delivery,
    local file uploads, and feed link posts.
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
            if page_id is not None
            else (getattr(settings, "FACEBOOK_PAGE_ID", None) or os.getenv("FACEBOOK_PAGE_ID", ""))
        )
        self.access_token = (
            access_token
            if access_token is not None
            else (getattr(settings, "FACEBOOK_PAGE_ACCESS_TOKEN", None) or os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN", ""))
        )
        self.app_id = (
            app_id
            if app_id is not None
            else (getattr(settings, "FACEBOOK_APP_ID", None) or os.getenv("FACEBOOK_APP_ID", ""))
        )
        self.app_secret = (
            app_secret
            if app_secret is not None
            else (getattr(settings, "FACEBOOK_APP_SECRET", None) or os.getenv("FACEBOOK_APP_SECRET", ""))
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

        # 2. Convert <code> tags to standout uppercase brackets
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
        image_path: Optional[Any] = None,
        image_bytes: Optional[bytes] = None,
        price: Optional[float] = None,
        title: Optional[str] = None
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Publishes a deal post to the Facebook Page:
        - Prioritizes pristine studio AliExpress master image directly from CDN (via url parameter)
          so Facebook downloads the uncompressed 1000x1000+ photo with zero blur and full-bleed display.
        - Falls back to local image bytes or file upload if remote URL is unavailable.
        - Falls back to feed text post if image delivery fails.

        Returns: (success: bool, post_id: Optional[str], error_message: Optional[str])
        """
        if not self.is_configured():
            return False, None, "Facebook Publisher is not configured (missing Page ID or Page Access Token)."

        fb_message = self.format_caption_for_facebook(caption, deal_link=deal_link, price=price)
        photo_url = f"{self.GRAPH_URL}/{self.page_id}/photos"

        # 1. Clean and prioritize high-res studio AliExpress CDN URL
        clean_img_url = get_high_res_aliexpress_image(image_url) if image_url else None

        async with httpx.AsyncClient(timeout=30.0) as client:
            # Step 1: Remote High-Resolution Master Studio Image URL
            if clean_img_url and str(clean_img_url).startswith("http"):
                payload = {
                    "url": clean_img_url,
                    "caption": fb_message,
                    "access_token": self.access_token
                }
                try:
                    resp = await client.post(photo_url, data=payload)
                    data = resp.json()

                    if resp.status_code in (200, 201) and ("id" in data or "post_id" in data):
                        post_id = data.get("post_id") or data.get("id")
                        logger.info(f"[FACEBOOK] Published high-res studio photo ({clean_img_url}) successfully! Post ID: {post_id}")
                        try:
                            await record_system_log("INFO", "facebook", f"Published high-res studio photo to Facebook Page (Photo ID: {post_id})")
                        except Exception:
                            pass
                        return True, str(post_id), None
                    else:
                        err_data = data.get("error", {})
                        err_msg = err_data.get("message", f"HTTP {resp.status_code}: {resp.text}")
                        logger.warning(f"[FACEBOOK] High-res URL photo upload failed: {err_msg}. Falling back to bytes/file...")
                except Exception as e:
                    logger.warning(f"[FACEBOOK] Exception during high-res URL photo upload ({e}), falling back to bytes/file...")

            # Step 2: Local image bytes fallback
            if image_bytes:
                try:
                    files = {"source": ("deal.jpg", image_bytes, "image/jpeg")}
                    data = {"caption": fb_message, "access_token": self.access_token}
                    resp = await client.post(photo_url, data=data, files=files)
                    res = resp.json()
                    if resp.status_code in (200, 201) and ("id" in res or "post_id" in res):
                        post_id = res.get("post_id") or res.get("id")
                        logger.info(f"[FACEBOOK] Published photo (bytes) deal successfully! Post ID: {post_id}")
                        try:
                            await record_system_log("INFO", "facebook", f"Published deal to Facebook Page (Photo ID: {post_id})")
                        except Exception:
                            pass
                        return True, str(post_id), None
                    else:
                        logger.warning(f"[FACEBOOK] Photo upload (bytes) failed: {res}. Falling back...")
                except Exception as e:
                    logger.warning(f"[FACEBOOK] Exception during photo bytes upload: {e}")

            # Step 3: Local image file path fallback
            if image_path:
                try:
                    p = Path(image_path) if not isinstance(image_path, Path) else image_path
                    if p.exists() and p.is_file():
                        file_bytes = p.read_bytes()
                        files = {"source": (p.name or "deal.jpg", file_bytes, "image/jpeg")}
                        data = {"caption": fb_message, "access_token": self.access_token}
                        resp = await client.post(photo_url, data=data, files=files)
                        res = resp.json()
                        if resp.status_code in (200, 201) and ("id" in res or "post_id" in res):
                            post_id = res.get("post_id") or res.get("id")
                            logger.info(f"[FACEBOOK] Published photo (file) deal successfully! Post ID: {post_id}")
                            try:
                                await record_system_log("INFO", "facebook", f"Published deal to Facebook Page (Photo ID: {post_id})")
                            except Exception:
                                pass
                            return True, str(post_id), None
                        else:
                            logger.warning(f"[FACEBOOK] Photo upload (file) failed: {res}. Falling back...")
                except Exception as e:
                    logger.warning(f"[FACEBOOK] Exception during photo file upload: {e}")

            # Step 4: Feed post fallback (Text + Link)
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
                    try:
                        await record_system_log("INFO", "facebook", f"Published deal to Facebook Page (Feed ID: {post_id})")
                    except Exception:
                        pass
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
