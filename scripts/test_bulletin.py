from app.aliexpress.parser import extract_prices, extract_coupon_list

text_lody = """كوبونات حدث Brand Day
و التي تستمر منذ اليوم 21 سبتمبر الى غاية 24 سبتمبر
كوبون 4/35$: BDQT04
كوبون 6/59$: BDQT06
كوبون 10/99$: BDQT10
كوبون 15/139$: BDQT15
كوبون 30/269$: BDQT30
طريقة حجز الكوبونات
https://s.click.aliexpress.com/e/_c3akXRah
"""

print("Price:", extract_prices(text_lody))
print("Coupons count:", len(extract_coupon_list(text_lody)))
