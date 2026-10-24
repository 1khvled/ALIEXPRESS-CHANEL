import sqlite3
import sys
import re
import json
import os

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r"D:\Projects\TELEGRAM_REPO")

from app.aliexpress.parser import extract_multi_coupons, extract_country_instruction

db_path = r"D:\Projects\TELEGRAM_REPO\deals.db"
con = sqlite3.connect(db_path)
cur = con.cursor()

query = """
SELECT d.id, d.product_id, d.title, d.coupon_code, sm.raw_text, gp.id, gp.title, gp.caption
FROM deals d
JOIN source_messages sm ON d.source_message_id = sm.id
LEFT JOIN generated_posts gp ON gp.deal_id = d.id
"""

rows = cur.execute(query).fetchall()
print(f"Total deals in deals.db: {len(rows)}")

COUNTRY_NAMES = {
    "السعودية 🇸🇦": "السعوديـــــة 🇸🇦",
    "الإمارات 🇦🇪": "الإمـــــارات 🇦🇪",
    "قطر 🇶🇦": "قطـــــر 🇶🇦",
    "الكويت 🇰🇼": "الكويـــــت 🇰🇼",
    "البحرين 🇧🇭": "البحريـــــن 🇧🇭",
    "عمان 🇴🇲": "عمـــــان 🇴🇲",
    "أوكرانيا 🇺🇦": "أوكرانيـــــا 🇺🇦",
    "أستراليا 🇦🇺": "أستراليـــــا 🇦🇺",
    "فرنسا 🇫🇷": "فرنســـــا 🇫🇷",
    "إسبانيا 🇪🇸": "إسبانيـــــا 🇪🇸",
    "كوريا 🇰🇷": "كــــــوريا 🇰🇷",
    "الجزائر 🇩🇿": "الجزائـــــر 🇩🇿",
    "كندا 🇨🇦": "كــــــندا 🇨🇦",
}

repaired_coupons = []
repaired_countries = []

for deal_id, product_id, deal_title, old_coupon, raw_text, gp_id, gp_title, gp_caption in rows:
    raw_text = raw_text or ""
    gp_caption = gp_caption or ""
    deal_title = deal_title or ""
    
    # --- 1. REPAIR COUPONS ---
    multi = extract_multi_coupons(raw_text)
    primary_code = multi.get("coupon_code")
    all_codes = multi.get("coupons", [])
    
    if primary_code and primary_code != old_coupon:
        cur.execute("UPDATE deals SET coupon_code = ? WHERE id = ?", (primary_code, deal_id))
        repaired_coupons.append({
            "deal_id": deal_id,
            "product_id": product_id,
            "old_coupon": old_coupon,
            "new_coupon": primary_code,
            "all_codes": all_codes
        })
        
        # If gp_caption had no coupon line, add it
        if gp_id and gp_caption:
            if not ("كـوبون" in gp_caption or "كوبون" in gp_caption or "كود" in gp_caption):
                coupon_line = f"\n🎟️ <b>كـوبون الخصم :</b> <code>{primary_code}</code>"
                if "🛒" in gp_caption:
                    new_cap = gp_caption.replace("🛒", f"{coupon_line}\n\n🛒", 1)
                else:
                    new_cap = gp_caption + f"\n{coupon_line}"
                cur.execute("UPDATE generated_posts SET caption = ? WHERE id = ?", (new_cap, gp_id))
                gp_caption = new_cap
                
    # --- 2. REPAIR COUNTRY HALLUCINATION ---
    expected_country = extract_country_instruction(raw_text, title=deal_title)
    has_explicit_country_in_raw = any(
        k in raw_text.lower() for k in [
            "أوكرانيا", "اوكرانيا", "اكرانيا", "🇺🇦", "ukraine",
            "استراليا", "أستراليا", "🇦🇺", "australia",
            "فرنسا", "🇫🇷", "france", "livraison france",
            "كوريا", "🇰🇷", "korea",
            "سعودية", "السعودية", "🇸🇦", "saudi", "ksa",
            "إمارات", "الامارات", "🇦🇪", "uae",
            "إسبانيا", "اسبانيا", "🇪🇸", "spain",
            "الجزائر", "🇩🇿", "algeria"
        ]
    )
    
    if gp_id and gp_caption and has_explicit_country_in_raw and expected_country:
        clean_country_name = COUNTRY_NAMES.get(expected_country, expected_country)
        
        # Check if caption contains Canada hallucination when raw text had another country
        if ("كندا" in gp_caption or "🇨🇦" in gp_caption) and not ("كندا" in raw_text or "🇨🇦" in raw_text or "canada" in raw_text.lower()):
            old_cap = gp_caption
            # Match with or without blockquote
            def replace_country(match):
                full_m = match.group(0)
                if full_m.startswith("<blockquote>"):
                    return f"<blockquote>📍 خلي البلـــد <b>{clean_country_name}</b></blockquote>"
                else:
                    return f"📍 خلي البلـــد <b>{clean_country_name}</b>"
                    
            new_cap = re.sub(
                r'(?:<blockquote>\s*)?📍\s*خلي\s*البل[ـ\s]*د\s*<b>[^<]+</b>(?:\s*</blockquote>)?',
                replace_country,
                gp_caption
            )
            if new_cap != old_cap:
                cur.execute("UPDATE generated_posts SET caption = ? WHERE id = ?", (new_cap, gp_id))
                repaired_countries.append({
                    "deal_id": deal_id,
                    "product_id": product_id,
                    "old_country": "كندا 🇨🇦",
                    "new_country": expected_country,
                    "title": deal_title
                })
        # Check if caption had NO country line when raw text explicitly specified one
        elif expected_country in ["أستراليا 🇦🇺", "أوكرانيا 🇺🇦", "السعودية 🇸🇦", "الإمارات 🇦🇪", "فرنسا 🇫🇷"]:
            if not ("خلي البلد" in gp_caption or "📍" in gp_caption):
                target_line = f"<blockquote>📍 خلي البلـــد <b>{clean_country_name}</b></blockquote>"
                m_header = re.search(r'</blockquote>', gp_caption)
                if m_header:
                    idx = m_header.end()
                    new_cap = gp_caption[:idx] + f"\n{target_line}" + gp_caption[idx:]
                else:
                    new_cap = f"{target_line}\n\n" + gp_caption
                cur.execute("UPDATE generated_posts SET caption = ? WHERE id = ?", (new_cap, gp_id))
                repaired_countries.append({
                    "deal_id": deal_id,
                    "product_id": product_id,
                    "old_country": "None",
                    "new_country": expected_country,
                    "title": deal_title
                })

con.commit()
con.close()

print(f"\n================ MIGRATION REPORT ================")
print(f"Total Products with Repaired Coupons: {len(repaired_coupons)}")
for rc in repaired_coupons:
    print(f"  - Deal #{rc['deal_id']} (Prod: {rc['product_id']}): '{rc['old_coupon']}' -> '{rc['new_coupon']}' | All codes: {rc['all_codes']}")

print(f"\nTotal Products with Repaired Countries: {len(repaired_countries)}")
for rc in repaired_countries:
    print(f"  - Deal #{rc['deal_id']} (Prod: {rc['product_id']}): '{rc['old_country']}' -> '{rc['new_country']}' | {rc['title']}")
