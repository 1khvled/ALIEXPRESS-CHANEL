from pathlib import Path
from typing import Optional, List, Dict
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

    def render_coupon_bulletin_card(
        self,
        coupon_list: List[Dict[str, str]],
        promo_title: str = "Party Ready Sale"
    ) -> Path:
        """
        Renders a high-definition 1080x1080 promotional coupon card.
        Guarantees coupon bulletin posts always have a professional graphic attached.
        """
        import hashlib
        w, h = 1080, 1080
        card = Image.new("RGB", (w, h), (18, 20, 32))
        draw = ImageDraw.Draw(card)

        # 1. Header Gradient: AliExpress Coral Red (#FF3B30 to #D31D1D)
        for y in range(230):
            r = int(240 - (y / 230.0) * 45)
            g = int(45 - (y / 230.0) * 20)
            b = int(55 - (y / 230.0) * 15)
            draw.line([(0, y), (w, y)], fill=(r, g, b))

        try:
            font_title = ImageFont.truetype("arialbd.ttf", 46)
            font_sub = ImageFont.truetype("arialbd.ttf", 26)
            font_tier = ImageFont.truetype("arialbd.ttf", 28)
            font_code = ImageFont.truetype("consola.ttf", 32)
            font_footer = ImageFont.truetype("arialbd.ttf", 22)
        except Exception:
            font_title = font_sub = font_tier = font_code = font_footer = ImageFont.load_default()

        # Title and Header text
        header_title = f"ALIEXPRESS {promo_title.upper()}" if promo_title else "ALIEXPRESS SPECIAL SALE"
        draw.text((w // 2, 65), header_title, fill=(255, 255, 255), font=font_title, anchor="mm")
        draw.text((w // 2, 125), "OFFICIAL PROMO CODES • SAVE UP TO $55", fill=(254, 240, 138), font=font_sub, anchor="mm")
        draw.text((w // 2, 175), "Valid Oct 1 - Oct 7 • Limited Quantities", fill=(255, 255, 255), font=font_footer, anchor="mm")

        # Circular Logo top right in header
        if self.logo_path.exists():
            try:
                with Image.open(self.logo_path) as logo_raw:
                    logo = logo_raw.convert("RGBA").resize((90, 90), Image.Resampling.LANCZOS)
                    card.paste(logo, (w - 120, 25), logo)
            except Exception:
                pass

        # Coupon Rows
        start_y = 250
        num_coupons = min(len(coupon_list), 7)
        row_h = max(68, min(88, (720 - (num_coupons * 12)) // max(1, num_coupons)))
        pad = 12
        card_w = 980
        card_x = (w - card_w) // 2

        for i, c in enumerate(coupon_list[:num_coupons]):
            tier_raw = str(c.get("tier", "")).strip().replace("$", "")
            code_raw = str(c.get("code", "")).strip().upper()
            tier_label = f"DISCOUNT ${tier_raw}" if tier_raw else "DISCOUNT"

            cy = start_y + i * (row_h + pad)
            # Row Background container
            draw.rounded_rectangle(
                (card_x, cy, card_x + card_w, cy + row_h),
                radius=14,
                fill=(28, 32, 48),
                outline=(255, 75, 75, 120),
                width=2
            )

            # Left Badge: Tier
            tier_badge_w = 340
            draw.rounded_rectangle(
                (card_x + 10, cy + 8, card_x + tier_badge_w, cy + row_h - 8),
                radius=10,
                fill=(239, 68, 68)
            )
            draw.text(
                (card_x + 10 + tier_badge_w // 2, cy + row_h // 2),
                tier_label,
                fill=(255, 255, 255),
                font=font_tier,
                anchor="mm"
            )

            # Center Label
            draw.text(
                (card_x + tier_badge_w + 120, cy + row_h // 2),
                "CODE:",
                fill=(156, 163, 175),
                font=font_sub,
                anchor="mm"
            )

            # Right Badge: Code
            code_box_x = card_x + card_w - 380
            draw.rounded_rectangle(
                (code_box_x, cy + 8, card_x + card_w - 12, cy + row_h - 8),
                radius=10,
                fill=(17, 24, 39),
                outline=(245, 158, 11),
                width=2
            )
            draw.text(
                ((code_box_x + card_x + card_w - 12) // 2, cy + row_h // 2),
                code_raw,
                fill=(251, 191, 36),
                font=font_code,
                anchor="mm"
            )

        # Footer
        draw.text(
            (w // 2, 1035),
            "Telegram: @DzAliexpress0   •   Coin Bot: @Alilo07BOT",
            fill=(156, 163, 175),
            font=font_footer,
            anchor="mm"
        )

        h_sig = hashlib.sha256(str(coupon_list).encode()).hexdigest()[:8]
        out_file = self.output_dir / f"coupons_card_{h_sig}.jpg"
        card.save(out_file, "JPEG", quality=95)
        return out_file

media_renderer = MediaRenderer()
