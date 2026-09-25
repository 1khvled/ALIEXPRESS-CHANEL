import httpx
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import io

def create_deal_image(
    product_img: Image.Image,
    logo_path: Path,
    price_usd: float = 15.30,
    price_eur: float = 14.08,
    output_path: Path = Path("test_mixed_deal.jpg")
):
    # Standardize to 1200x1200 high-res square
    canvas_size = (1200, 1200)
    base = Image.new("RGB", canvas_size, (255, 255, 255))
    
    # Fit product image proportionally inside canvas
    prod = product_img.convert("RGBA")
    prod.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
    
    # Paste centered
    x_offset = (canvas_size[0] - prod.width) // 2
    y_offset = (canvas_size[1] - prod.height) // 2
    base.paste(prod, (x_offset, y_offset), prod if prod.mode == 'RGBA' else None)
    
    # Create an RGBA overlay for watermark & badges
    overlay = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # 1. TOP-RIGHT: Circular DealScout Logo with soft drop shadow & white ring
    if logo_path.exists():
        with Image.open(logo_path) as logo_raw:
            logo = logo_raw.convert("RGBA")
            logo_size = 130
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            
            # Position
            margin = 35
            lx = canvas_size[0] - logo_size - margin
            ly = margin
            
            # Draw soft shadow behind logo
            shadow = Image.new("RGBA", (logo_size + 20, logo_size + 20), (0, 0, 0, 0))
            sdraw = ImageDraw.Draw(shadow)
            sdraw.ellipse((6, 6, logo_size + 14, logo_size + 14), fill=(0, 0, 0, 80))
            shadow = shadow.filter(ImageFilter.GaussianBlur(8))
            overlay.paste(shadow, (lx - 10, ly - 10), shadow)
            
            # Draw white circular background/border ring
            draw.ellipse((lx - 3, ly - 3, lx + logo_size + 3, ly + logo_size + 3), fill=(255, 255, 255, 255))
            
            # Mask logo to circle
            lmask = Image.new("L", (logo_size, logo_size), 0)
            ldraw = ImageDraw.Draw(lmask)
            ldraw.ellipse((0, 0, logo_size, logo_size), fill=255)
            overlay.paste(logo, (lx, ly), lmask)

    # 2. BOTTOM-RIGHT or BOTTOM-LEFT: Sleek Modern Price Pill Badge
    # A dark glassmorphic rounded pill with vibrant gold/orange price tag
    price_text = f"${price_usd:.2f}"
    pill_h = 74
    pill_w = 210
    px = 35
    py = canvas_size[1] - pill_h - 35
    
    # Soft shadow behind pill
    pshadow = Image.new("RGBA", (pill_w + 30, pill_h + 30), (0, 0, 0, 0))
    psdraw = ImageDraw.Draw(pshadow)
    psdraw.rounded_rectangle((10, 10, pill_w + 20, pill_h + 20), radius=37, fill=(0, 0, 0, 90))
    pshadow = pshadow.filter(ImageFilter.GaussianBlur(7))
    overlay.paste(pshadow, (px - 15, py - 15), pshadow)
    
    # Pill background (deep dark slate #111827 with subtle transparency)
    draw.rounded_rectangle((px, py, px + pill_w, py + pill_h), radius=37, fill=(17, 24, 39, 235), outline=(255, 255, 255, 60), width=2)
    
    # Text inside pill
    try:
        font_price = ImageFont.truetype("arialbd.ttf", 38)
    except Exception:
        font_price = ImageFont.load_default()
        
    # Draw Price Text centered inside pill
    bbox = draw.textbbox((0, 0), price_text, font=font_price)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = px + (pill_w - tw) // 2
    ty = py + (pill_h - th) // 2 - 3
    
    # Subtle glowing price in vibrant gold/yellow (#FBBF24)
    draw.text((tx, ty), price_text, fill=(251, 191, 36, 255), font=font_price)
    
    # Composite
    final_img = Image.alpha_composite(base.convert("RGBA"), overlay)
    final_rgb = final_img.convert("RGB")
    final_rgb.save(output_path, "JPEG", quality=95)
    print(f"Rendered mixed deal card to {output_path}")

if __name__ == "__main__":
    url = "https://ae-pic-a1.aliexpress-media.com/kf/Sfbae0feba74e4820b4b8e130abb8d2beC.jpg"
    r = httpx.get(url)
    prod_img = Image.open(io.BytesIO(r.content))
    logo_path = Path("assets/logo_circular.png")
    create_deal_image(prod_img, logo_path)
