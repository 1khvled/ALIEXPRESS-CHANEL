from app.aliexpress.parser import extract_coupon_list, extract_clean_title

text = """
هاتف جديد من شركة POCO 
✅ POCO X8 5G (6/128GB)
💰 السعر : 230$ 
⚙️ يجي بمواصفات تقنية قوية 
🔥 Cpu : Snapdragon 6s Gen4
🔋 Battery: 8340mAh + 67W 
📷 50 Main Camera PDAF, OIS
📱 6.83" Amoled, 3500nits, 120Hz
🎫 قسيمة البائع 96$ ANIS96
🎟️ كوبـــون 30/269$ : BDQT30
"""

print("Coupon list:", extract_coupon_list(text))
print("Clean title:", extract_clean_title(text))
