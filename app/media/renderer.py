from pathlib import Path
from typing import Optional
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from app.config.settings import settings
from app.utils.logger import logger

class MediaRenderer:
    def __init__(self, output_dir: Optional[Path] = None, logo_path: Optional[Path] = None):
        self.output_dir = output_dir or settings.GENERATED_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        circ_path = settings.BASE_DIR / "assets" / "logo_circular.png"
        default_logo = circ_path if circ_path.exists() else (settings.BASE_DIR / "assets" / "logo.png")
        self.logo_path = logo_path or default_logo

    def _render_deal_card(
        self,
        base_img: Image.Image,
        usd_price: Optional[float] = None
    ) -> Image.Image:
        """
        Renders a sleek Option A+B mixed card on the native product image:
        - Full natural product photo (no artificial white bars)
        - DealScout circular logo with subtle shadow and white ring border (top-right)
        - Modern glassmorphic dark-slate price pill with glowing gold text (bottom-left)
        """
        prod = base_img.convert("RGBA")
        max_dim = 1280
        if max(prod.size) > max_dim:
            prod.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)

        w, h = prod.size
        overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # 1. TOP-RIGHT: Circular DealScout Logo with soft shadow & white border
        if self.logo_path.exists():
            try:
                with Image.open(self.logo_path) as logo_raw:
                    logo = logo_raw.convert("RGBA")
                    logo_size = max(70, min(130, int(w * 0.11)))
                    logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
                    margin = max(18, int(w * 0.03))
                    lx = w - logo_size - margin
                    ly = margin

                    # Soft drop shadow
                    shadow = Image.new("RGBA", (logo_size + 24, logo_size + 24), (0, 0, 0, 0))
                    sdraw = ImageDraw.Draw(shadow)
                    sdraw.ellipse((6, 6, logo_size + 18, logo_size + 18), fill=(0, 0, 0, 80))
                    shadow = shadow.filter(ImageFilter.GaussianBlur(8))
                    overlay.paste(shadow, (lx - 12, ly - 12), shadow)

                    # White circular background / ring
                    draw.ellipse((lx - 3, ly - 3, lx + logo_size + 3, ly + logo_size + 3), fill=(255, 255, 255, 255))

                    # Paste circular logo
                    mask = Image.new("L", (logo_size, logo_size), 0)
                    draw_m = ImageDraw.Draw(mask)
                    draw_m.ellipse((0, 0, logo_size, logo_size), fill=255)
                    overlay.paste(logo, (lx, ly), mask)
            except Exception as e:
                logger.warning(f"Failed rendering logo badge: {e}")

        # 2. BOTTOM-LEFT: Modern Sleek Price Pill Badge
        if usd_price and usd_price > 0:
            try:
                price_text = f"${usd_price:.2f}"
                font_size = max(24, min(42, int(w * 0.035)))
                try:
                    font_price = ImageFont.truetype("arialbd.ttf", font_size)
                except Exception:
                    font_price = ImageFont.load_default()

                bbox = draw.textbbox((0, 0), price_text, font=font_price)
                tw = bbox[2] - bbox[0]
                th = bbox[3] - bbox[1]

                pill_h = max(52, th + 30)
                pill_w = max(140, tw + 46)
                margin = max(20, int(w * 0.03))
                px = margin
                py = h - pill_h - margin
                radius = pill_h // 2

                # Soft shadow behind pill
                pshadow = Image.new("RGBA", (pill_w + 30, pill_h + 30), (0, 0, 0, 0))
                psdraw = ImageDraw.Draw(pshadow)
                psdraw.rounded_rectangle((10, 10, pill_w + 20, pill_h + 20), radius=radius, fill=(0, 0, 0, 85))
                pshadow = pshadow.filter(ImageFilter.GaussianBlur(7))
                overlay.paste(pshadow, (px - 15, py - 15), pshadow)

                # Pill background (deep dark slate #111827 with subtle transparency)
                draw.rounded_rectangle(
                    (px, py, px + pill_w, py + pill_h),
                    radius=radius,
                    fill=(17, 24, 39, 235),
                    outline=(255, 255, 255, 60),
                    width=2
                )

                # Price Text in glowing gold (#FBBF24)
                tx = px + (pill_w - tw) // 2
                ty = py + (pill_h - th) // 2 - 2
                draw.text((tx, ty), price_text, fill=(251, 191, 36, 255), font=font_price)
            except Exception as e:
                logger.warning(f"Failed rendering price pill: {e}")

        final_composite = Image.alpha_composite(prod, overlay)
        return final_composite.convert("RGB")

    def prepare_post_image(
        self,
        image_path: Optional[Path],
        product_id: Optional[str] = None,
        title: Optional[str] = None,
        usd_price: Optional[float] = None
    ) -> Optional[Path]:
        """
        Processes product image with Option A+B mixed styling.
        """
        pid = product_id or "deal"
        out_file = self.output_dir / f"ready_{pid}.jpg"

        if image_path and image_path.exists():
            try:
                with Image.open(image_path) as img:
                    branded = self._render_deal_card(img, usd_price=usd_price)
                    branded.save(out_file, "JPEG", quality=95)
                    return out_file
            except Exception as e:
                logger.warning(f"Failed processing image {image_path}: {e}")

        return None

media_renderer = MediaRenderer()
