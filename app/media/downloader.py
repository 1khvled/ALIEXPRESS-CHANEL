import hashlib
from pathlib import Path
from typing import Optional
import httpx
from PIL import Image
from app.config.settings import settings
from app.utils.logger import logger

class MediaDownloader:
    def __init__(self, storage_dir: Optional[Path] = None):
        self.storage_dir = storage_dir or settings.DOWNLOADS_DIR
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    async def download_image(self, image_url: str, identifier: Optional[str] = None) -> Optional[Path]:
        """
        Downloads an image from URL and verifies it with PIL.
        Returns local Path if successful, None otherwise.
        """
        if not image_url:
            return None

        # Build filename
        if identifier:
            filename = f"product_{identifier}.jpg"
        else:
            url_hash = hashlib.sha256(image_url.encode("utf-8")).hexdigest()[:16]
            filename = f"img_{url_hash}.jpg"

        file_path = self.storage_dir / filename

        # If already cached and valid, return existing
        if file_path.exists() and file_path.stat().st_size > 1024:
            return file_path

        try:
            async with httpx.AsyncClient(timeout=12.0, follow_redirects=True, verify=False) as client:
                resp = await client.get(
                    image_url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                    }
                )
                if resp.status_code == 200 and len(resp.content) > 1024:
                    with open(file_path, "wb") as f:
                        f.write(resp.content)

                    # Validate with PIL
                    with Image.open(file_path) as img:
                        img.verify()

                    return file_path
                else:
                    logger.warning(f"Failed image download for {image_url} (HTTP {resp.status_code})")
        except Exception as e:
            logger.warning(f"Error downloading image from {image_url}: {e}")
            if file_path.exists():
                file_path.unlink(missing_ok=True)

        return None

media_downloader = MediaDownloader()
