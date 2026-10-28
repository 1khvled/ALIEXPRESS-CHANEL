import sys
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

import arabic_reshaper
from bidi.algorithm import get_display

def ar(text: str) -> str:
    if not text:
        return ""
    return get_display(arabic_reshaper.reshape(text))

def get_font(names, size):
    dirs = [
        "C:/Windows/Fonts",
        "C:/WINNT/Fonts",
        str(Path(__file__).resolve().parent.parent / "assets" / "fonts")
    ]
    for d in dirs:
        for name in names:
            p = os.path.join(d, name)
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, size)
                except Exception:
                    pass
    return ImageFont.load_default()

def render_stores_showcase_card(output_path: Path) -> Path:
    w, h = 1200, 1200
    card = Image.new("RGB", (w, h), (15, 23, 42))  # Slate 900
    draw = ImageDraw.Draw(card)

    # 1. Header Gradient: Vibrant AliExpress Crimson to Burgundy (#E11D48 -> #9F1239 -> #0F172A)
    header_h = 290
    for y in range(header_h):
        prog = y / float(header_h)
        r = int(225 * (1 - prog) + 15 * prog)
        g = int(29 * (1 - prog) + 23 * prog)
        b = int(72 * (1 - prog) + 42 * prog)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # Accent glow line under header
    draw.line([(50, header_h), (w - 50, header_h)], fill=(245, 158, 11), width=2)

    font_badge = get_font(["segoeuib.ttf", "arialbd.ttf"], 20)
    font_main_title = get_font(["arialbd.ttf", "segoeuib.ttf"], 44)
    font_ar_title = get_font(["traditional arabic bold.ttf", "arialbd.ttf", "segoeuib.ttf"], 36)
    font_banner = get_font(["segoeuib.ttf", "arialbd.ttf"], 22)
    font_cat_title = get_font(["segoeuib.ttf", "arialbd.ttf"], 24)
    font_cat_ar = get_font(["segoeuib.ttf", "arialbd.ttf"], 18)
    font_chip = get_font(["arialbd.ttf", "segoeuib.ttf"], 20)
    font_footer = get_font(["segoeuib.ttf", "arialbd.ttf"], 22)

    # 2. Top Event Pill Badge
    badge_text = "•  11.11 GLOBAL SHOPPING FESTIVAL • WARM-UP ÉCHAUFFEMENT  •"
    bbox = font_badge.getbbox(badge_text)
    bw = (bbox[2] - bbox[0]) + 50
    bx = (w - bw) // 2
    draw.rounded_rectangle((bx, 28, bx + bw, 70), radius=21, fill=(254, 240, 138), outline=(245, 158, 11), width=2)
    draw.text((w // 2, 49), badge_text, fill=(146, 64, 14), font=font_badge, anchor="mm")

    # 3. Main Title & Arabic Subtitle
    draw.text((w // 2, 115), "OFFICIAL BRAND STORES DIRECTORY", fill=(255, 255, 255), font=font_main_title, anchor="mm")
    ar_title_reshaped = ar("دليل المتاجر الرسمية المعتمدة (تخفيضات 11.11 الكبرى)")
    draw.text((w // 2, 170), ar_title_reshaped, fill=(253, 224, 71), font=font_ar_title, anchor="mm")

    # 4. Action Banner Pill (Store coupons reminder)
    banner_w = 1100
    banner_h = 56
    banner_x = (w - banner_w) // 2
    banner_y = 212
    draw.rounded_rectangle((banner_x, banner_y, banner_x + banner_w, banner_y + banner_h), radius=16, fill=(30, 41, 59), outline=(225, 29, 72), width=2)
    banner_txt = ar("🛒 احجز قسائم المتجر (Store Coupons) وعَمّر سلّتك الآن لتثبيت السعر!")
    draw.text((w // 2, banner_y + banner_h // 2), banner_txt, fill=(255, 255, 255), font=font_banner, anchor="mm")

    # 5. Categories Grid (4 Sleek Cards)
    categories = [
        {
            "en_title": "GAMING & MECHANICAL KEYBOARDS",
            "ar_title": ar("عتاد القيمنق والكيبوردات الميكانيكية"),
            "color": (245, 158, 11),  # Amber
            "bg_accent": (40, 30, 20),
            "stores": ["AJAZZ", "ATTACK SHARK", "AULA", "MACHENIKE", "MCHOSE", "GAMESIR", "FLYDIGI"],
            "y": 320,
            "h": 175
        },
        {
            "en_title": "AUDIOPHILE & WIRELESS AUDIO",
            "ar_title": ar("سماعات الصوت والموسيقى الاحترافية"),
            "color": (16, 185, 129),  # Emerald
            "bg_accent": (20, 38, 30),
            "stores": ["ANKER SOUNDCORE", "QCY OFFICIAL", "KZ ACOUSTICS", "TANGZU AUDIO"],
            "y": 515,
            "h": 160
        },
        {
            "en_title": "FAST CHARGERS & TECH ESSENTIALS",
            "ar_title": ar("الشواحن وملحقات الطاقة السريعة GaN"),
            "color": (59, 130, 246),  # Blue
            "bg_accent": (20, 30, 45),
            "stores": ["BASEUS", "UGREEN", "ESSAGER", "TOOCKI"],
            "y": 695,
            "h": 160
        },
        {
            "en_title": "SMARTPHONES & SMARTWEAR",
            "ar_title": ar("الهواتف الذكية والساعات الاقتصادية"),
            "color": (168, 85, 247),  # Purple
            "bg_accent": (35, 22, 45),
            "stores": ["POCO OFFICIAL", "XIAOMI MI GLOBAL", "ZEBLAZE", "COLMI"],
            "y": 875,
            "h": 160
        }
    ]

    card_margin_x = 50
    card_w = w - (card_margin_x * 2)

    for cat in categories:
        cy = cat["y"]
        ch = cat["h"]
        c_color = cat["color"]
        c_bg = cat["bg_accent"]

        # Card container
        draw.rounded_rectangle(
            (card_margin_x, cy, card_margin_x + card_w, cy + ch),
            radius=18,
            fill=(23, 32, 51),
            outline=c_color,
            width=2
        )

        # Header bar inside category
        draw.text((card_margin_x + 25, cy + 28), f"▶  {cat['en_title']}", fill=c_color, font=font_cat_title, anchor="lm")
        draw.text((card_margin_x + card_w - 25, cy + 28), cat["ar_title"], fill=(203, 213, 225), font=font_cat_ar, anchor="rm")

        # Divider line
        draw.line([(card_margin_x + 25, cy + 50), (card_margin_x + card_w - 25, cy + 50)], fill=(51, 65, 85), width=1)

        # Brand chips
        chips = cat["stores"]
        chip_y = cy + 70
        chip_x = card_margin_x + 25
        row_y = chip_y

        for chip in chips:
            cbbox = font_chip.getbbox(chip)
            chip_tw = cbbox[2] - cbbox[0]
            chip_width = chip_tw + 32
            chip_height = 42

            # Wrap to second row if needed
            if chip_x + chip_width > (card_margin_x + card_w - 25):
                chip_x = card_margin_x + 25
                row_y += 48

            # Chip capsule
            draw.rounded_rectangle(
                (chip_x, row_y, chip_x + chip_width, row_y + chip_height),
                radius=12,
                fill=(15, 23, 42),
                outline=(71, 85, 105),
                width=1
            )
            # Chip text
            draw.text((chip_x + chip_width // 2, row_y + chip_height // 2), chip, fill=(255, 255, 255), font=font_chip, anchor="mm")
            chip_x += chip_width + 14

    # 6. Sleek Modern Footer Bar
    footer_y = 1060
    draw.line([(50, footer_y), (w - 50, footer_y)], fill=(51, 65, 85), width=1)

    # Logo
    logo_path = Path(__file__).resolve().parent.parent / "assets" / "logo_circular.png"
    if logo_path.exists():
        try:
            with Image.open(logo_path) as logo_raw:
                logo = logo_raw.convert("RGBA")
                lsize = 80
                logo = logo.resize((lsize, lsize), Image.Resampling.LANCZOS)
                card.paste(logo, (60, footer_y + 25), logo)
        except Exception:
            pass

    draw.text((155, footer_y + 45), "DEALSCOUT DZ • OFFICIAL 11.11 HUB", fill=(255, 255, 255), font=font_footer, anchor="lm")
    draw.text((155, footer_y + 80), "@DzAliexpress0 | @francedealsdz", fill=(245, 158, 11), font=font_cat_ar, anchor="lm")

    web_text = "dealscoutgreen.vercel.app"
    draw.text((w - 60, footer_y + 65), web_text, fill=(56, 189, 248), font=font_footer, anchor="rm")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    card.save(output_path, "JPEG", quality=95)
    print(f"Generated brand stores card successfully -> {output_path}")
    return output_path

if __name__ == "__main__":
    out_dir = Path(__file__).resolve().parent.parent / "storage" / "generated"
    card_file = out_dir / "official_brand_stores_11_11.jpg"
    render_stores_showcase_card(card_file)
