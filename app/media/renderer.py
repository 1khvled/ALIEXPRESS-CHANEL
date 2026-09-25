from pathlib import Path
from typing import Optional
from PIL import Image, ImageDraw, ImageFont
from app.config.settings import settings
from app.utils.logger import logger

class MediaRenderer:
    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or settings.GENERATED_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def prepare_post_image(
        self,
        image_path: Optional[Path],
        product_id: Optional[str] = None,
        title: Optional[str] = None
    ) -> Optional[Path]:
        """
        Processes the image into optimal format for Telegram.
        If image_path is valid, normalizes size and RGB format.
        If no image is available, generates a clean graphic deal card.
        """
        pid = product_id or "deal"
        out_file = self.output_dir / f"ready_{pid}.jpg"

        if image_path and image_path.exists():
            try:
                with Image.open(image_path) as img:
                    img = img.convert("RGB")
                    # Resize proportionally if too large
                    max_dim = 1200
                    if max(img.size) > max_dim:
                        img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
                    img.save(out_file, "JPEG", quality=90)
                    return out_file
            except Exception as e:
                logger.warning(f"Failed processing image {image_path}: {e}")

        # Fallback: Generate clean branded card
        return self._generate_fallback_card(title or "AliExpress Deal", out_file)

    def _generate_fallback_card(self, title: str, out_file: Path) -> Path:
        width, height = 800, 800
        # Dark clean gradient background
        img = Image.new("RGB", (width, height), color=(24, 28, 36))
        draw = ImageDraw.Draw(img)

        # Draw red accent badge at top
        draw.rectangle([(50, 60), (320, 120)], fill=(225, 29, 72))
        draw.text((70, 75), "ALIEXPRESS DEAL", fill=(255, 255, 255))

        # Title snippet
        wrapped_title = title[:60] + "..." if len(title) > 60 else title
        draw.text((50, 200), wrapped_title, fill=(240, 240, 240))

        # Footer CTA
        draw.line([(50, 700), (750, 700)], fill=(60, 65, 80), width=2)
        draw.text((50, 720), "TELEGRAM DEALS CHANNEL", fill=(160, 165, 180))

        img.save(out_file, "JPEG", quality=85)
        return out_file

media_renderer = MediaRenderer()
